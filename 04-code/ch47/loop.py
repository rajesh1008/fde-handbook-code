"""Listings 47.7 and 47.8: field reports ranked by votes and by evidence; the two features and the loop metrics."""
import sys, _paths  # noqa: F401
from fieldkit.playbooks import FieldReport, rank_reports, evidence_score, loop_metrics
from world import REPORTS, SHIPPED, name
reps = [FieldReport(rid, t, o, list(e), [h] * len(e), v, a, art, fm) for rid, t, o, e, h, v, a, art, fm in REPORTS]
if sys.argv[1] == "rank":
    votes, ev = rank_reports(reps, "votes"), rank_reports(reps, "evidence")
    print(f"{'rank':4} {'by votes and contract size':44} {'by evidence (engagements x hours)':44}")
    for i, (a, b) in enumerate(zip(votes, ev), 1):
        sb = f"{b.rid} {b.title[:30]:30} {evidence_score(b):>5.0f}" if evidence_score(b) else f"{b.rid} needs artifact"
        print(f"{i:>4} {a.rid} {a.title[:30]:30} {a.votes:>2} v  {sb}")
    print("evidence score = engagements with bespoke work x median bespoke hours; 0 without working code and a test")
else:
    for s in SHIPPED:
        print(f"{s['rid']} {s['feature']}")
        print(f"   first field report month {s['first_month']}, triaged month {s['triaged_month']}, shipped month "
              f"{s['shipped_month']}; adopted at {len(s['adopted'])} engagements; FDE hours per engagement "
              f"{s['hours_before']} to {s['hours_after']}")
    m = loop_metrics(SHIPPED)
    tri = [s["shipped_month"] - s["triaged_month"] for s in SHIPPED]
    print(f"loop: {m['features']} features from the field; median months report to ship {m['median_lead_months']}; "
          f"triage to ship {tri}; adopting engagements {m['adopting_engagements']}; FDE hours saved {m['hours_saved']:,}")
