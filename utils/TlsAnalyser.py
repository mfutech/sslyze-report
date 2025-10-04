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


class TlsResult:
    def __init__(self):
        self.ssl2_enabled = False
        self.ssl3_enabled = False
        self.tls1_0_enabled = False
        self.tls1_1_enabled = False
        self.tls1_2_enabled = False
        self.tls1_3_enabled = False
        self.ssl2_accepted_ciphers = []
        self.ssl3_accepted_ciphers = []
        self.tls1_0_accepted_ciphers = []
        self.tls1_1_accepted_ciphers = []
        self.tls1_2_accepted_ciphers = []
        self.tls1_3_accepted_ciphers = []
        self.forbidden_ciphers = []
        self.weak_ciphers = []


class TlsAnalyser:
    def __init__(self, db_log_err):
        self.db_log_err = db_log_err
        self.server_scan_result = None

    def analyze_results(self, server_scan_result):
        self.server_scan_result = server_scan_result
        tls_result = TlsResult()

        tls_result.ssl2_enabled, self.ssl2_accepted_ciphers = self._generic_get_results(
            server_scan_result.scan_result.ssl_2_0_cipher_suites
        )
        tls_result.ssl3_enabled, self.ssl3_accepted_ciphers = self._generic_get_results(
            server_scan_result.scan_result.ssl_3_0_cipher_suites
        )
        tls_result.tls1_0_enabled, self.tls1_0_accepted_ciphers = (
            self._generic_get_results(
                server_scan_result.scan_result.tls_1_0_cipher_suites
            )
        )
        tls_result.tls1_1_enabled, self.tls1_1_accepted_ciphers = (
            self._generic_get_results(
                server_scan_result.scan_result.tls_1_1_cipher_suites
            )
        )
        tls_result.tls1_2_enabled, self.tls1_2_accepted_ciphers = (
            self._generic_get_results(
                server_scan_result.scan_result.tls_1_2_cipher_suites
            )
        )
        tls_result.tls1_3_enabled, self.tls1_3_accepted_ciphers = (
            self._generic_get_results(
                server_scan_result.scan_result.tls_1_3_cipher_suites
            )
        )

        return tls_result

    def _generic_get_results(self, scan_result):

        if scan_result.status == ScanCommandAttemptStatusEnum.ERROR:
            # An error happened when this scan command was run
            return (None, None)

        elif scan_result.status == ScanCommandAttemptStatusEnum.COMPLETED:
            # This scan command was run successfully
            cypher_result = []
            for accepted_cipher_suite in scan_result.result.accepted_cipher_suites:
                cypher_result.append(accepted_cipher_suite.cipher_suite.name)
            return (True, cypher_result)
