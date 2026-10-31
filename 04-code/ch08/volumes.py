"""Volumes, latency and cost for the signed scope, each number with its basis (deterministic stand-in).

Inputs come from the scope's own claims (V-01 to V-05) and the Chapter 6 readout. The peak-hour share is an
assumption, printed as one; the claims core's write limit is read from a 2016 specification nobody has load-tested.
"""
from caldwell_scope import signed, PATH_VOLUME

doc = signed()
inside, total = doc.coverage()
BUSINESS_DAYS = 21.7             # assumed: Caldwell's business days a month (calendar, 2026)
MONDAY = 1.6                     # measured: mailroom log, 12 weeks (V-01)
PEAK_HOUR_SHARE = 0.22           # assumed: share of a day's arrivals in the busiest hour (overnight mail and fax)
CORE_WRITES_PER_MIN = 20         # assumed: claims-core interface specification, 2016 (V-04), never load-tested
MANUAL = 7.31                    # measured: Anne's intake budget over system counts (V-03)
MODEL_EST, MODEL_CEILING = 0.21, 0.40   # estimated (cost model v2, V-05); target (C-07)

day = inside / BUSINESS_DAYS
monday = day * MONDAY
peak_min = monday * PEAK_HOUR_SHARE / 60
writes = peak_min * 3            # a draft record, an attachment link and an audit note per document (proposed design)
rows = [
    ("in-scope documents a month", f"{inside:,}", "estimated", "S-02, path mix from shadowing"),
    ("mean business day", f"{day:,.0f}", "estimated", "over 21.7 business days (assumed)"),
    ("Monday", f"{monday:,.0f}", "estimated", "1.6 x mean, mailroom log (measured)"),
    ("busiest Monday minute, documents", f"{peak_min:.1f}", "assumed", "22% of the day in one hour"),
    ("claims-core writes needed a minute", f"{writes:.1f}", "assumed", "3 writes a document (proposed)"),
    ("claims-core writes allowed a minute", f"{CORE_WRITES_PER_MIN}", "assumed", "2016 specification, untested"),
    ("manual cost, in-scope documents", f"${inside * MANUAL:,.0f}/mo", "measured", "$7.31 a document"),
    ("model and compute, estimate", f"${inside * MODEL_EST:,.0f}/mo", "estimated", "$0.21 a document (vendor)"),
    ("model and compute, ceiling", f"${inside * MODEL_CEILING:,.0f}/mo", "target", "C-07, $0.40 a document"),
]
print(f"VOLUMES, LATENCY, COST  {doc.customer} scope {doc.version}")
print(f"{'line':<38}{'value':>12}  {'basis':<10} source")
for a, b, c, d in rows:
    print(f"{a:<38}{b:>12}  {c:<10} {d}")
head = CORE_WRITES_PER_MIN / writes
print(f"headroom at the busiest minute: {head:.1f}x, resting on two assumptions -> load test before Build Complete")
print("savings: not claimed in the scope; the measured cost is a baseline, not a promise")
