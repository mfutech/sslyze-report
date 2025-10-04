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

from pprint import pprint as pp


# "ssl_2_0_cipher_suites", "ssl_3_0_cipher_suites", "tls_1_0_cipher_suites", "tls_1_1_cipher_suites", "tls_1_2_cipher_suites", "tls_1_3_cipher_suites",


class CertResult:
    def __init__(self, cert_deployment=None):
        self.cert_subject = None
        self.cert_issuer = None
        self.cert_serial_number = None
        self.cert_public_key_type = None
        self.not_valid_after = None
        if cert_deployment is not None:
            self.analyze_results(cert_deployment)

    def analyze_results(self, cert_deployment):
        leaf_cert = cert_deployment.received_certificate_chain[0]
        self.subject = leaf_cert.subject.rfc4514_string()
        self.issuer = leaf_cert.issuer.rfc4514_string()
        self.serial_number = f"{leaf_cert.serial_number}"
        self.public_key_type = leaf_cert.public_key().__class__.__name__
        self.not_valid_after = leaf_cert.not_valid_after_utc


class CertAnalyser:

    def __init__(
        self,
        db_log_err,
    ):
        self.db_log_err = db_log_err
        self.cert_results = []

    def analyze_results(self, server_scan_result):
        # Process the result of the certificate info scan command
        certinfo_attempt = server_scan_result.scan_result.certificate_info
        if certinfo_attempt.status == ScanCommandAttemptStatusEnum.ERROR:
            # An error happened when this scan command was run
            self.db_log_err.log(
                "Error: Certificate info scan command failed",
                server_scan_result.server_location.hostname,
                server_scan_result.server_location.port,
            )
            self.cert_results.append(CertResult())

        elif certinfo_attempt.status == ScanCommandAttemptStatusEnum.COMPLETED:
            certinfo_result = certinfo_attempt.result
            assert certinfo_result
            for cert_deployment in certinfo_result.certificate_deployments:
                self.cert_results.append(CertResult(cert_deployment))
        return self.cert_results
