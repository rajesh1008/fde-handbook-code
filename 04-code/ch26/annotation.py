"""Listing 26.3: two adjusters, one rubric, one adjudicator. Agreement per field before and after clarification."""
import json
from world import gold_items, gold_docs, FIELDS, EXACT, u
from fieldkit.evals import calibration_report, Adjudicator

items = gold_items()
calib_docs = sorted([d[0] for d in gold_docs() if d[3] == "dev"], key=lambda d: u(d, "calib"))[:40]
R1 = dict(policy_number=.02, claimant_name=.05, loss_date=.03, date_received=.16, loss_type=.22, loss_location=.15,
          injury_reported=.12, police_report_ref=.03, other_party=.18, intake_channel=.01)
R2 = dict(policy_number=.01, claimant_name=.03, loss_date=.01, date_received=.03, loss_type=.03, loss_location=.05,
          injury_reported=.02, police_report_ref=.01, other_party=.09, intake_channel=.01)


def score(it, who, rnd):
    """An adjuster's pass/fail on the model's value: the truth, unless this reader reads the rubric differently."""
    r = (R1 if rnd == 1 else R2)[it.field]
    return it.anne_ok != (u(it.doc, it.field, who, rnd, "read") < r)


cal = [it for it in items if it.doc in calib_docs]
res = {}
for rnd in (1, 2):
    a = {f: [score(it, "TW", rnd) for it in cal if it.field == f] for f in FIELDS}
    b = {f: [score(it, "AB", rnd) for it in cal if it.field == f] for f in FIELDS}
    res[rnd] = calibration_report(a, b, EXACT, exact_line=0.8, judgment_line=0.6)
print("calibration on 40 development documents: Cohen's kappa between Whitfield and Ortiz")
print("  field               line   round 1   round 2   agreement round 2")
pa = {}
for f in FIELDS:
    k1, line, ok1 = res[1][f]
    k2, _, ok2 = res[2][f]
    a2 = [score(it, "TW", 2) for it in cal if it.field == f]
    b2 = [score(it, "AB", 2) for it in cal if it.field == f]
    pa[f] = sum(x == y for x, y in zip(a2, b2))
    print(f"  {f:<18}  {line:4.1f}   {k1:5.2f}{' ' if ok1 else '*'}    {k2:5.2f}{' ' if ok2 else '*'}    {pa[f]}/40, "
          f"{sum(a2)} and {sum(b2)} passed")
for rnd in (1, 2):
    print(f"  round {rnd}: {sum(v[2] for v in res[rnd].values())} of 10 fields at or above their line (* = below)")

# main labeling: every fifth document labeled twice, at round-2 reading rates; Anne decides every disagreement
overlap = [it for it in items if int(it.doc[1:]) % 5 == 0]
A = {it.key: score(it, "TW", 2) for it in overlap}
B = {it.key: score(it, "AB", 3) for it in overlap}
adj = Adjudicator("Anne Kessler")
ds = adj.compare(A, B)
truth = {it.key: it for it in overlap}
for d in ds:
    it = truth[(d.item, d.field)]
    r = u(d.item, d.field, "why")
    reason = ("rubric gap" if it.field in ("date_received", "loss_type", "loss_location", "injury_reported",
                                           "other_party") and r < .55 else "reading error" if r < .85
              else "document ambiguous")
    adj.decide(d, it.anne_ok, reason)
gold = adj.gold(A)
wrong_single = sum(A[k] != truth[k].anne_ok for k in A)
print(f"\nmain labeling: {len(overlap) // 10} documents labeled twice ({len(overlap)} fields)")
print(f"  disagreements: {len(ds)}  decided by {adj.owner}: {adj.reason_counts()}")
print(f"  fields where Whitfield's label alone would have gone into the gold set wrong: {wrong_single}")
print(f"  wrong after adjudication (both adjusters agreed and both misread): {sum(gold[k] != truth[k].anne_ok for k in gold)}")
json.dump(dict(r1={f: res[1][f][0] for f in FIELDS}, r2={f: res[2][f][0] for f in FIELDS},
               lines={f: res[1][f][1] for f in FIELDS}, disagreements=len(ds), reasons=adj.reason_counts()),
          open("output/annotation.json", "w"), indent=1)
