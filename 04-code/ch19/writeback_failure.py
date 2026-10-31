"""Listing 19.5 (failure injection): the first-notice write-back, built and tested in claims-core UAT, then
run unchanged in pre-production, which carries the production rule table. Deterministic stand-in data."""
import _paths  # noqa: F401
from adapter import ClaimsCoreTarget, naive_write
from sim import ClaimsCore, caldwell_sample

fn = [d for d in caldwell_sample() if d["kind"] == "fnol"]
for env in ("uat", "preprod"):
    app = ClaimsCore(env, lose_response=[d["doc"] for d in fn if d["timeout"]])
    t = ClaimsCoreTarget(app)
    rej = {}
    for d in fn:
        ok, cid, why = naive_write(t, d["doc"], d)
        if not ok:
            rej[why] = rej.get(why, 0) + 1
    st = {}
    for c in app.claims.values():
        st[c["status"]] = st.get(c["status"], 0) + 1
    refs = [c["Agent Ref"] for c in app.claims.values() if c["status"] == "OPEN"]
    dup = len(refs) - len(set(refs))
    trunc = sum(1 for c in app.claims.values() if c["status"] == "OPEN" and
                c["Claimant"] != next(d["claimant"] for d in fn if d["doc"] == c["Agent Ref"]))
    print(f"{env:8} writes {len(fn)}  accepted {len(fn) - sum(rej.values()):3}  rejected {sum(rej.values()):2} {rej or ''}")
    print(f"{'':8} claims in system {len(app.claims)}  by status {dict(sorted(st.items()))}  "
          f"duplicate claims {dup}  silently truncated names {trunc}")
