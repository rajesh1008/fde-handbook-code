"""Try It Yourself a, b, c (deterministic stand-in)."""
import sys
from agent import STEPS, Doc, Release, Gateway, run
from state import ClaimStateStore, Value, ScopeViolation
from walkthrough import EMILY

part = sys.argv[1] if len(sys.argv) > 1 else "abc"
if "a" in part:
    print("a. porting the agent to a second insurer: what each step needs")
    plan = {"C01": "reuse (re-measure legibility on their scanners)", "C02": "re-derive (their fax header layout)",
            "C03": "re-derive (their policy pattern and check digit)", "C04": "re-derive (their policy system read)",
            "C05": "re-derive (their claim match rule)", "C06": "re-sign label set, re-train on their documents",
            "C07": "re-sign code list with their owner", "C08": "re-derive (their forms)",
            "C09": "re-sign: rules need their named owner", "C10": "re-sign: rules need their named owner",
            "C11": "reuse model, re-run gold set", "C12": "re-derive write path and boundary"}
    for s in STEPS:
        print(f"  {s.n} {s.name:<52}{plan[s.n]}")
    print("  router thresholds: not ported; re-fit on their gold set (0.95 / 0.47 are Caldwell's)")
if "b" in part:
    print("\nb. an example store shared across claims")
    other = Doc("E-147-052", 147, "email", "T3", "IK-147-0052", truth=dict(EMILY.truth, claimant_name="CL-0417 (synthetic)",
                policy_number="HO-5520318-1", other_party=""))
    leaked = Value("neighbor at 14 Alder Ct, unit above (from IK-142-0017)", "IK-142-0017", "E-142-017 p1")
    tr, out = run(other, Release(examples_from_other_claims=True), Gateway(), ClaimStateStore(), example=leaked)
    print("  " + "\n  ".join(f"{s:<7}{r}" for s, _, _, r in tr[-2:]))
    st = ClaimStateStore(); st.open(other.key, "shadow", 147)
    try:
        st.put(other.key, "other_party", leaked, 147)
    except ScopeViolation as e:
        print(f"  store: {e}")
if "c" in part:
    print("\nc. a legal hold arrives before an erasure request")
    st = ClaimStateStore(); run(EMILY, Release(), Gateway(), st)
    st.hold(EMILY.key, 158, "Caldwell legal", "matter CM-L-0102 (synthetic)")
    print(f"  erase on day 160: {st.erase(EMILY.key, 160, 'PR-0049 (synthetic)')['status']}")
    print(f"  retention on day 240: {st.retention(240)}")
    del st.holds[EMILY.key]; st._log(250, "Caldwell legal", "hold released", EMILY.key)
    print(f"  hold released day 250, retention on day 251: {st.retention(251)}")
