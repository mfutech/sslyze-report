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
        self.supported_ciphers_str = []
        self.weak_ciphers = []
        self.uses_weak_algorithm = True

    def ssl2_accepted_ciphers_str(self):
        return ", ".join(self.ssl2_accepted_ciphers)

    def ssl3_accepted_ciphers_str(self):
        return ", ".join(self.ssl3_accepted_ciphers)

    def tls1_0_accepted_ciphers_str(self):
        return ", ".join(self.tls1_0_accepted_ciphers)

    def tls1_1_accepted_ciphers_str(self):
        return ", ".join(self.tls1_1_accepted_ciphers)

    def tls1_2_accepted_ciphers_str(self):
        return ", ".join(self.tls1_2_accepted_ciphers)

    def tls1_3_accepted_ciphers_str(self):
        return ", ".join(self.tls1_3_accepted_ciphers)


class TlsAnalyser:
    def __init__(self, server_scan_result = None):
        self.tls_result = None
        if (server_scan_result is not None):
            self.analyze_results(server_scan_result)

    def analyze_results(self, server_scan_result):
        self.server_scan_result = server_scan_result
        self.tls_result = TlsResult()

        self.tls_result.ssl2_enabled, self.tls_result.ssl2_accepted_ciphers = (
            self._generic_get_results(
                server_scan_result.scan_result.ssl_2_0_cipher_suites
            )
        )
        self.tls_result.ssl3_enabled, self.tls_result.ssl3_accepted_ciphers = (
            self._generic_get_results(
                server_scan_result.scan_result.ssl_3_0_cipher_suites
            )
        )
        self.tls_result.tls1_0_enabled, self.tls1_0_accepted_ciphers = (
            self._generic_get_results(
                server_scan_result.scan_result.tls_1_0_cipher_suites
            )
        )
        self.tls_result.tls1_1_enabled, self.tls_result.tls1_1_accepted_ciphers = (
            self._generic_get_results(
                server_scan_result.scan_result.tls_1_1_cipher_suites
            )
        )
        self.tls_result.tls1_2_enabled, self.tls_result.tls1_2_accepted_ciphers = (
            self._generic_get_results(
                server_scan_result.scan_result.tls_1_2_cipher_suites
            )
        )
        self.tls_result.tls1_3_enabled, self.tls_result.tls1_3_accepted_ciphers = (
            self._generic_get_results(
                server_scan_result.scan_result.tls_1_3_cipher_suites
            )
        )

        return self.tls_result

    def _generic_get_results(self, scan_result):

        if scan_result.status == ScanCommandAttemptStatusEnum.ERROR:
            # An error happened when this scan command was run
            return (None, None)

        elif scan_result.status == ScanCommandAttemptStatusEnum.COMPLETED:
            # This scan command was run successfully
            cypher_result = []
            for accepted_cipher_suite in scan_result.result.accepted_cipher_suites:
                cypher_result.append(accepted_cipher_suite.cipher_suite.name)
            return (scan_result.result.is_tls_version_supported, cypher_result)
