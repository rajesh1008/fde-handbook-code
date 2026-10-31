"""Listings 52.4 and 52.5: the behavior change no layer scores, then the check that would have caught it."""
import _paths  # noqa: F401
from fieldkit.pyramid import MergeGate, caught_at, LAYER_NAMES
import world as W, suite as S

n2_cal = S.calibrator(W.N2, W.CAL_DOCS[0::2])
print(f"intake summaries on the 34 test documents that contain a dispute statement")
print(f"{'version':<16}{'kept':>6}{'dropped':>9}{'summary tokens':>16}")
for v in W.VERSIONS:
    kept = sum(W.summary_keeps_dispute(v, d) for d in W.DISPUTE_DOCS)
    print(f"{v:<16}{kept:>6}{34 - kept:>9}{W.SUMMARY_TOKENS[v]:>16}")
res = S.pyramid().run({"version": W.N2, "signed_off": S.lost_critical(W.N2), "calibrator": n2_cal}, stop_on_fail=False)
print(f"suite on gm-n2 with router v1.2: {MergeGate('Anne Kessler').decide(res)['decision']} "
      f"({sum(r.verdict == 'pass' for r in res)} of {len(res)} checks pass; none reads the summary)")
print()


def dispute_kept(sys):
    lost = [d for d in W.DISPUTE_DOCS if W.summary_keeps_dispute(W.PIN, d) and not W.summary_keeps_dispute(sys["version"], d)]
    return f"dispute statement dropped in {len(lost)} of 34 summaries ({', '.join(lost[:4])}, ...)" if lost else ""


res = S.pyramid().run({"version": W.N2, "signed_off": S.lost_critical(W.N2), "calibrator": n2_cal, "extra_checks": (dispute_kept,)}, stop_on_fail=False)
d = MergeGate("Anne Kessler").decide(res); at = caught_at(res)
print(f"with the dispute-statement slice added to layer 2: decision {d['decision']}, caught at layer {at} ({LAYER_NAMES[at]})")
for r in d["reasons"]:
    print("  " + r)
