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
from utils.MozillaTlsChecker import MozillaTlsChecker, MozillaTlsResult
from utils.HostAnalyser import HostAnalyser, HostResult

from pprint import pprint as pp


host = "www.unil.ch"
port = 443

scan_request = ServerScanRequest(
    server_location=ServerNetworkLocation(hostname=host, port=port)
)
scanner = Scanner()
scanner.queue_scans([scan_request])
results = [x for x in scanner.get_results()]
scan_result = results[0]

TlsAnalyser_instance = TlsAnalyser()

tls_result = TlsAnalyser_instance.analyze_results(scan_result)
pp(tls_result.__dict__)

CertAnalyser_instance = CertAnalyser()
cert_results = CertAnalyser_instance.analyze_results(scan_result)
for cert_result in cert_results:
    pp(cert_result.__dict__)

moz_tls_checker = MozillaTlsChecker(None)
moz_tls_checker.analyze_results(scan_result)
pp("Mozilla TLS Compliance:")
pp("Modern:")
pp(moz_tls_checker.modern.__dict__)
pp("Intermediate:")
pp(moz_tls_checker.intermediate.__dict__)
pp("Old:")
pp(moz_tls_checker.old.__dict__)

host_analyser = HostAnalyser(scan_result)
pp("Host Analysis:")
pp(host_analyser.host.__dict__)

for cert in host_analyser.certs:
    pp("Certificate:")
    pp(cert.__dict__)
