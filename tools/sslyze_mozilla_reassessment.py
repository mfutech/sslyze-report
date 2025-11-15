#!/usr/bin/env python3
import argparse
import csv
import sys
from typing import List

# -------- Robust imports across SSLyze 6.1/6.2 --------
try:
    # Newer style
    from sslyze.json.json_output import SslyzeOutputAsJson, ServerScanResultAsJson
except Exception:  # pragma: no cover
    try:
        # Older style
        from sslyze.json_output import SslyzeOutputAsJson, ServerScanResultAsJson  # type: ignore
    except Exception as e:
        print("Failed to import SSLyze JSON models. Is sslyze installed? Error:", e, file=sys.stderr)
        sys.exit(2)

# Mozilla checker (names changed a bit between versions)
ConfigEnum = None
CheckerCls = None
for mod_name, enum_name, cls_name in [
    ("sslyze.mozilla_tls_profile.mozilla_config_checker", "MozillaTlsConfigurationEnum", "MozillaTlsConfigurationChecker"),
    ("sslyze.mozilla_tls_profile.mozilla_config_checker", "MozillaTlsConfigurationEnum", "MozillaTlsConfigChecker"),
    ("sslyze.mozilla_tls_profile.tls_config_checker", "MozillaTlsConfigurationEnum", "MozillaTlsConfigurationChecker"),
]:
    try:
        mod = __import__(mod_name, fromlist=[enum_name, cls_name])
        ConfigEnum = getattr(mod, enum_name)
        CheckerCls = getattr(mod, cls_name)
        break
    except Exception:
        continue

if ConfigEnum is None or CheckerCls is None:
    print("Could not import Mozilla TLS config checker from sslyze. "
          "Make sure you're using sslyze>=5. Try: pip install --upgrade sslyze",
          file=sys.stderr)
    sys.exit(3)

def profile_to_enum(name: str):
    name = name.strip().lower()
    mapping = {
        "modern": getattr(ConfigEnum, "MODERN", None),
        "intermediate": getattr(ConfigEnum, "INTERMEDIATE", None),
        "old": getattr(ConfigEnum, "OLD", None),
    }
    if name not in mapping or mapping[name] is None:
        raise SystemExit(f"Unknown profile '{name}'. Use modern|intermediate|old.")
    return mapping[name]

def main():
    ap = argparse.ArgumentParser(description="Reassess SSLyze JSON using Mozilla TLS config checker (built into sslyze).")
    ap.add_argument("--in", dest="inp", required=True, help="Path to previous SSLyze JSON (--json_out)")
    ap.add_argument("--out", dest="out", default="mozilla_reassessment.csv", help="CSV output path")
    ap.add_argument("--profile", dest="profile", default="intermediate", help="modern|intermediate|old (default: intermediate)")
    args = ap.parse_args()

    try:
        raw = open(args.inp, "r", encoding="utf-8").read()
        results = SslyzeOutputAsJson.model_validate_json(raw)
    except Exception as e:
        print("Failed to parse the SSLyze JSON file:", e, file=sys.stderr)
        sys.exit(4)

    enum_val = profile_to_enum(args.profile)
    checker = CheckerCls(enum_val)

    rows: List[dict] = []
    for srv in results.server_scan_results:
        host = srv.server_info.server_location.hostname
        port = srv.server_info.server_location.port
        ip = srv.server_info.server_location.ip_address or ""

        compliant = True
        violations: List[str] = []

        try:
            # Some versions want a pydantic object, so ensure type matches
            validated_srv = ServerScanResultAsJson.model_validate(srv.model_dump())
            # Method name differences: try common options
            res = None
            for m in ("check_server_scan_result", "validate_server_scan_result_against_configuration"):
                if hasattr(checker, m):
                    res = getattr(checker, m)(validated_srv)
                    break
            if res is not None:
                # Try to collect reasons from the result object if available
                for attr in ("errors", "violations", "reasons", "non_compliance_reasons"):
                    v = getattr(res, attr, None)
                    if v:
                        violations.extend([str(x) for x in v])
                        compliant = compliant and (len(v) == 0)
        except Exception as e:
            compliant = False
            violations.append(str(e))

        rows.append({
            "host": host,
            "port": port,
            "ip": ip,
            "profile": args.profile,
            "compliant": "YES" if compliant else "NO",
            "violations": " | ".join(violations) if violations else "",
        })

    with open(args.out, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["host","port","ip","profile","compliant","violations"])
        w.writeheader()
        for r in rows:
            w.writerow(r)

    total = len(rows)
    ok = sum(1 for r in rows if r["compliant"] == "YES")
    fail = total - ok
    print(f"Wrote {args.out}. Profile={args.profile}. Compliant: {ok}/{total}, Non-compliant: {fail}.")

if __name__ == "__main__":
    main()
