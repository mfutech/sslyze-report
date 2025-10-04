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
)
from sslyze.errors import ServerHostnameCouldNotBeResolved
from sslyze.scanner.scan_command_attempt import ScanCommandAttempt
from utils.ScanError import ScanError
from utils.TlsAnalyser import TlsResult, TlsAnalyser
from utils.CertAnalyser import CertResult, CertAnalyser


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
        scanner.queue_scans([scan_request])

        # And retrieve and process the results for each server
        for server_scan_result in scanner.get_results():
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

            # Process the result of the certificate info scan command
            cert_scanner = CertAnalyser(db_log_err)
            for cert_result in cert_scanner.analyze_results(server_scan_result):
                db.execute(
                    "INSERT INTO certificates (hostname, port, serial_number, subject, public_key_type, not_after, sslv2, sslv3, tls1_0, tls1_1, tls1_2, tls1_3)  VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    (
                        server_scan_result.server_location.hostname,
                        server_scan_result.server_location.port,
                        f"{cert_result.serial_number}",
                        cert_result.subject,
                        cert_result.public_key_type,
                        cert_result.not_valid_after,
                        ", ".join(tls_result.ssl2_accepted_ciphers),
                        ", ".join(tls_result.ssl3_accepted_ciphers),
                        ", ".join(tls_result.tls1_0_accepted_ciphers),
                        ", ".join(tls_result.tls1_1_accepted_ciphers),
                        ", ".join(tls_result.tls1_2_accepted_ciphers),
                        ", ".join(tls_result.tls1_3_accepted_ciphers),
                    ),
                )
                db.commit()

    error_log.close()
    db.close()


if __name__ == "__main__":
    main()
