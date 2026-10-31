"""Chapter 35 failure injection: scan the provider's stored-request log export for Greystone's sandbox week.
Usage: pii_scan.py before | after"""
import sys

import _paths  # noqa: F401
from fieldkit.privacy import pii_scan
from world import known_values, provider_log, referrals

mode = sys.argv[1] if len(sys.argv) > 1 else "before"
refs = referrals()
if mode == "before":
    log = provider_log(refs)
    pat = pii_scan(log)
    full = pii_scan(log, known=known_values(refs))
    print("Provider stored-request export, Greystone deployment, days 115-119 (deterministic stand-in)")
    print("patterns only")
    print(pat.summary())
    print("patterns + known values (Greystone's roster of the 200 sandbox-week patients)")
    print(full.summary())
    print(f"  referrals with at least one fragment retained: {sum(1 for r in refs if r['scanned'] or r['narrative_name'])} of {len(refs)}")
    print("  masked examples:")
    for e in full.examples:
        print("   ", e)
    print("verdict: PHI retained by the provider outside GA-06; stop PHI traffic, open privacy finding P-01")
else:
    log = provider_log(refs, fixed=True)
    rep = pii_scan(log * 3, known=known_values(refs))
    print("Day 124 rescan: provider export, gateway diagnostics and trace export after the fix (metadata only)")
    print(rep.summary())
    print(f"verdict: {'clean' if rep.clean else 'NOT CLEAN'}")
