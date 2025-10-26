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

from sslyze.mozilla_tls_profile.tls_config_checker import (
    MozillaTlsConfiguration,
    check_server_against_tls_configuration,
    TlsConfigurationEnum,
    ServerNotCompliantWithTlsConfiguration,
    ServerScanResultIncomplete,
)

from pprint import pprint as pp

# "ssl_2_0_cipher_suites", "ssl_3_0_cipher_suites", "tls_1_0_cipher_suites", "tls_1_1_cipher_suites", "tls_1_2_cipher_suites", "tls_1_3_cipher_suites",


class MozillaTlsResult:
    def __init__(self, server_scan_result=None, moz_config=None):
        self.success = False
        self.feedback = "untested"
        self.issues = {}
        if server_scan_result is not None and moz_config is not None:
            self.analyze_results(server_scan_result, moz_config)

    def analyze_results(self, server_scan_result, moz_config):
        try:
            check_server_against_tls_configuration(server_scan_result, moz_config)
            self.success = True
            self.feedback = "Server meets Mozilla TLS configuration."
        except ServerNotCompliantWithTlsConfiguration as e:
            self.success = False
            self.feedback = "Server does not meet Mozilla TLS configuration."
            self.issues = e.issues
        except ServerScanResultIncomplete as e:
            self.success = False
            self.feedback = f"Scan result incomplete"
            self.issues = e.issues


class MozillaTlsChecker:
    def __init__(self, db_log_err=None):
        self.db_log_err = db_log_err
        self.modern = MozillaTlsResult()
        self.intermediate = MozillaTlsResult()
        self.old = MozillaTlsResult()

    def analyze_results(self, server_scan_result):

        # Check against Mozilla Intermediate profile
        self.intermediate = MozillaTlsResult(
            server_scan_result=server_scan_result,
            moz_config=MozillaTlsConfiguration().get(
                TlsConfigurationEnum("intermediate")
            ),
        )
        # Check against Mozilla Modern profile
        self.modern = MozillaTlsResult(
            server_scan_result=server_scan_result,
            moz_config=MozillaTlsConfiguration().get(TlsConfigurationEnum("modern")),
        )
        # Check against Mozilla Old profile
        self.old = MozillaTlsResult(
            server_scan_result=server_scan_result,
            moz_config=MozillaTlsConfiguration().get(TlsConfigurationEnum("old")),
        )
        return self.modern, self.intermediate, self.old
