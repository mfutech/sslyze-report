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
from sslyze.mozilla_tls_profile.tls_config_checker import (
    MozillaTlsConfiguration,
    check_server_against_tls_configuration,
    TlsConfigurationEnum,
)

from utils.ScanError import ScanError
from utils.CertAnalyser import CertAnalyser, CertResult
from utils.TlsAnalyser import TlsAnalyser, TlsResult
from utils.MozillaTlsChecker import MozillaTlsChecker, MozillaTlsResult

from pprint import pprint as pp


class HostResult:
    def __init__(self, scan_result=None):
        self.hostname = None
        self.port = None
        self.tls = TlsResult()
        self.cert = CertResult()
        self.cert_deployment = []
        self.moz_tls_modern = None
        self.moz_tls_intermediate = None
        self.moz_tls_old = None

        if scan_result is not None:
            self.analyze_results(scan_result)

    def analyze_results(self, scan_result):
        self.hostname = scan_result.server_location.hostname
        self.port = scan_result.server_location.port
        # Analyze TLS results
        tls_analyser = TlsAnalyser()
        tls_analyser.analyze_results(scan_result)
        self.tls = tls_analyser.tls_result
        # Analyze Certificate results
        cert_analyser = CertAnalyser()
        cert_analyser.analyze_results(scan_result)
        self.cert_deployment = cert_analyser.cert_results
        # Analyze Mozilla TLS compliance
        moz_tls_checker = MozillaTlsChecker()
        moz_tls_checker.analyze_results(scan_result)
        self.moz_tls_modern = moz_tls_checker.modern
        self.moz_tls_intermediate = moz_tls_checker.intermediate
        self.moz_tls_old = moz_tls_checker.old


class HostAnalyser:
    def __init__(
        self,
        scan_result=None,
    ):
        self.host = HostResult()
        self.certs = []
        if scan_result is not None:
            self.analyze_results(scan_result)

    def analyze_results(self, scan_result):
        # a server scan shall hold only one host, but can have multiple certificates
        self.host = HostResult(scan_result)

        # Process the result of the certificate info scan command
        certinfo_attempt = scan_result.scan_result.certificate_info
        if certinfo_attempt.status == ScanCommandAttemptStatusEnum.ERROR:
            self.certs.append(CertResult())

        elif certinfo_attempt.status == ScanCommandAttemptStatusEnum.COMPLETED:
            certinfo_result = certinfo_attempt.result
            assert certinfo_result
            for cert_deployment in certinfo_result.certificate_deployments:
                self.certs.append(CertResult(cert_deployment))

        # although store in the scanner, return it.
        return (self.host, self.certs)
