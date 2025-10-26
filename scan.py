#!/usr/bin/env python
#
# scan.py
#
# provide simple interface to sslyze to start a scan in put result in a database
#
#

import configparser
from email.mime import message
import sqlite3
import argparse
from datetime import datetime
import json

CONFIGFILE = "config.ini"
DEFAULT_DB = "data/sslyze_report.db"
DEFAULT_ERROR_LOG = "data/error.log"


from sslyze import (
    Scanner,
    ServerScanRequest,
    SslyzeOutputAsJson,
    ServerNetworkLocation,
    ScanCommandAttemptStatusEnum,
    ServerScanStatusEnum,
    ServerScanResultAsJson,
    ServerScanResult,
)
from sslyze.errors import ServerHostnameCouldNotBeResolved
from sslyze.scanner.scan_command_attempt import ScanCommandAttempt

from datetime import datetime

from utils.ScanError import ScanError
from utils.TlsAnalyser import TlsResult, TlsAnalyser
from utils.CertAnalyser import CertResult, CertAnalyser
from utils.HostAnalyser import HostResult, HostAnalyser
from utils.MozillaTlsChecker import MozillaTlsChecker, MozillaTlsResult


def result_to_json(
    result: ServerScanResult,
    date_scans_started: datetime,
    date_scans_completed: datetime,
) -> str:
    """Convert a ServerScanResult to its JSON representation."""
    json_output = SslyzeOutputAsJson(
        # server_scan_results=ServerScanResultAsJson.model_validate(result),
        server_scan_results=(result),
        invalid_server_strings=[],  # Not needed here - specific to the CLI interface
        date_scans_started=date_scans_started,
        date_scans_completed=date_scans_completed,
    )
    return json_output.model_dump_json()


def main() -> None:
    # read configuration file
    config = configparser.ConfigParser()
    config.read(CONFIGFILE)

    # connect to the database
    db_filename = config.get("sqlite", "db_path", fallback=DEFAULT_DB)
    db = sqlite3.connect(db_filename)
    db_log_err = ScanError(db)

    # open error log file
    error_log = open(
        config.get("logging", "error_log", fallback=DEFAULT_ERROR_LOG), "a"
    )

    # parse command line arguments
    parser = argparse.ArgumentParser(
        description="Run sslyze scans and store results in a database"
    )

    # define scan id & record it
    SCANID = "SCANID-" + datetime.now().strftime("%Y%m%d%-H%M%S")
    db.execute("INSERT INTO scans (scanid) VALUES (?)", (SCANID,))
    db.commit()

    # First create the scan requests for each server that we want to scan

    for host in config.options("hostlist"):
        port = config.getint("hostlist", host, fallback=443)
        try:
            scan_request = ServerScanRequest(
                server_location=ServerNetworkLocation(hostname=host, port=port)
            )
        except ServerHostnameCouldNotBeResolved:
            db_log_err.log("Error: Could not resolve hostname", host, port)
            error_log.write(f"Error: Could not resolve hostname {host}\n")
            continue

        # Then queue all the scans
        scanner = Scanner()
        scan_started = datetime.now()
        scanner.queue_scans([scan_request])

        # And retrieve and process the results for each server
        for server_scan_result in scanner.get_results():
            scan_completed = datetime.now()
            db_log_err.log(
                "Scan completed",
                server_scan_result.server_location.hostname,
                server_scan_result.server_location.port,
            )
            print(
                f"\n\n****Results for {server_scan_result.server_location.hostname}****"
            )

            # Were we able to connect to the server and run the scan?
            if (
                server_scan_result.scan_status
                == ServerScanStatusEnum.ERROR_NO_CONNECTIVITY
            ):
                # No we weren't
                db_log_err.log(
                    f"Error: Could not connect to server: {server_scan_result.connectivity_error_trace}",
                    server_scan_result.server_location.hostname,
                    server_scan_result.server_location.port,
                )

                error_log.write(
                    f"Error: Could not connect to {server_scan_result.server_location.hostname}:"
                    f" {server_scan_result.connectivity_error_trace}\n"
                )
                continue

            # Since we were able to run the scan, scan_result is populated
            assert server_scan_result.scan_result

            # Analyze TLS results
            tls_scanner = TlsAnalyser(db_log_err)
            tls_result = tls_scanner.analyze_results(server_scan_result)

            # create a json version of the result
            json_result = result_to_json(
                [server_scan_result], scan_started, scan_completed
            )

            ## store json result - we keep the complete result of the scan for possible reprocessing or diagnostics
            ## TODO - might need a cleanup process, to evaluate,
            db.execute(
                "INSERT INTO scan_details (host, port, scan_started, scan_completed , scan_result_json, scan_id) "
                + "VALUES                   (?,    ?,    ?,            ?,               ?,                ?      )",
                (
                    server_scan_result.server_location.hostname,
                    server_scan_result.server_location.port,
                    scan_started,
                    scan_completed,
                    json_result,
                    SCANID,
                ),
            )
            db.commit()

            host_analyser = HostAnalyser(db_log_err=db_log_err)
            host_info, certs_info = host_analyser.analyze_results(server_scan_result)
            cert_serial_numbers = [c.serial_number for c in certs_info]

            db.execute(
                """INSERT INTO hosts (host, port, sslv2, sslv3, tls1_0, tls1_1, tls1_2, tls1_3, 
                                             certificate_serial_number, scan_id, mozilla_old, 
                                             mozilla_intermediate, mozilla_modern) VALUES           (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (
                    host_info.hostname,
                    host_info.port,
                    json.dumps(
                        {
                            "enabled": host_info.tls.ssl2_enabled,
                            "accepted_ciphers": host_info.tls.ssl2_accepted_ciphers_str(),
                        }
                    ),
                    json.dumps(
                        {
                            "enabled": host_info.tls.ssl3_enabled,
                            "accepted_ciphers": host_info.tls.ssl3_accepted_ciphers_str(),
                        }
                    ),
                    json.dumps(
                        {
                            "enabled": host_info.tls.tls1_0_enabled,
                            "accepted_ciphers": host_info.tls.tls1_0_accepted_ciphers_str(),
                        }
                    ),
                    json.dumps(
                        {
                            "enabled": host_info.tls.tls1_1_enabled,
                            "accepted_ciphers": host_info.tls.tls1_1_accepted_ciphers_str(),
                        }
                    ),
                    json.dumps(
                        {
                            "enabled": host_info.tls.tls1_2_enabled,
                            "accepted_ciphers": host_info.tls.tls1_2_accepted_ciphers_str(),
                        }
                    ),
                    json.dumps(
                        {
                            "enabled": host_info.tls.tls1_3_enabled,
                            "accepted_ciphers": host_info.tls.tls1_3_accepted_ciphers_str(),
                        }
                    ),
                    json.dumps(cert_serial_numbers),
                    SCANID,
                    json.dumps(
                        {
                            "compliant": host_info.moz_tls_old.success,
                            "feedback": host_info.moz_tls_old.feedback,
                            "issues": host_info.moz_tls_old.issues,
                        }
                    ),
                    json.dumps(
                        {
                            "compliant": host_info.moz_tls_intermediate.success,
                            "feedback": host_info.moz_tls_intermediate.feedback,
                            "issues": host_info.moz_tls_intermediate.issues,
                        }
                    ),
                    json.dumps(
                        {
                            "compliant": host_info.moz_tls_modern.success,
                            "feedback": host_info.moz_tls_modern.feedback,
                            "issues": host_info.moz_tls_modern.issues,
                        }
                    ),
                ),
            )
            db.commit()

            # Process the result of the certificate info scan command
            cert_scanner = CertAnalyser(db_log_err)
            for cert_result in cert_scanner.analyze_results(server_scan_result):

                db.execute(
                    """INSERT INTO certificates 
                              (serial_number, subject, public_key_type, not_after, parent_certificate_serial_number, issuer, scan_id) 
                              VALUES 
                              (?            , ?      , ?              , ?        , ?                               , ?     , ?)""",
                    (
                        f"{cert_result.serial_number}",
                        cert_result.subject,
                        cert_result.public_key_type,
                        cert_result.not_valid_after,
                        f"{cert_result.issuer_serial}",
                        cert_result.issuer,
                        SCANID,
                    ),
                )
                db.commit()

    error_log.close()
    db.close()


if __name__ == "__main__":
    main()
