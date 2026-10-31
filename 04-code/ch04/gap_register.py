"""Listing 4.1: the demo-claim audit. Every claim the sales cycle made, mapped to the dimension it
speaks to, set against the 25 proofs a deployment needs, with Caldwell's status on day 10."""
from collections import Counter
from deployment import DIMENSIONS
from checklists import caldwell, REQUIRED

# (claim as made, where it was made, dimension it speaks to, what kind of evidence stands behind it)
DEMO_CLAIMS = [
    ("extracts all ten intake fields", "demo, day 2", "capability", "demo set"),
    ("98 of 100 fields correct", "demo, day 2", "capability", "demo set"),
    ("accuracy above 95% on Caldwell's documents", "sales deck", "capability", "none"),
    ("reads email, fax and scanned mail", "sales deck", "capability", "demo set"),
    ("reads handwriting", "demo, day 2", "capability", "demo set"),
    ("returns a structured record in four seconds", "demo, day 2", "capability", "demo set"),
    ("works on any document Caldwell receives", "sales deck", "capability", "none"),
    ("runs on the latest model", "sales deck", "capability", "none"),
    ("no integration work on Caldwell's side", "sales deck", "workflow", "none"),
    ("live in production in under five months", "sales deck", "schedule", "none"),
    ("enterprise-grade security", "sales deck", "controls", "vendor certificate"),
]


def main():
    by_dim = Counter(d for _, _, d, _ in DEMO_CLAIMS)
    kinds = Counter(k for *_, k in DEMO_CLAIMS)
    print(f"DEMO CLAIM REGISTER  Caldwell Mutual  {len(DEMO_CLAIMS)} claims")
    for claim, where, dim, kind in DEMO_CLAIMS:
        print(f"  {claim:<45}{where:<13}{dim:<12}{kind}")
    print("evidence behind the claims: " + ", ".join(f"{k} {n}" for k, n in kinds.most_common()))
    print()
    c = caldwell(day=10)
    cp = c.customer_people
    print("GAP REGISTER  day 10  proofs a deployment needs, by dimension")
    print(f"  {'dimension':<20}{'claims':>7}{'proofs':>8}{'held':>6}{'partial':>9}{'missing':>9}{'must-pass open':>16}")
    totals = Counter()
    for d in DIMENSIONS:
        ps = [p for p in c.proofs.values() if p.dimension == d]
        st = Counter(p.counted(cp) for p in ps)
        must_open = sum(1 for p in ps if p.must_pass and p.counted(cp) != "held")
        totals.update(dict(claims=by_dim[d], proofs=len(ps), held=st["held"], partial=st["partial"],
                           missing=st["missing"], must=must_open))
        print(f"  {d:<20}{by_dim[d]:>7}{len(ps):>8}{st['held']:>6}{st['partial']:>9}{st['missing']:>9}{must_open:>16}")
    print(f"  {'schedule':<20}{by_dim['schedule']:>7}{'(a date is not a proof)':>40}")
    print(f"  {'total':<20}{totals['claims'] + by_dim['schedule']:>7}{totals['proofs']:>8}{totals['held']:>6}"
          f"{totals['partial']:>9}{totals['missing']:>9}{totals['must']:>16}")
    print(f"capability share of claims: {by_dim['capability'] / len(DEMO_CLAIMS):.0%}; "
          f"capability share of proofs: {5 / len(REQUIRED):.0%}")


if __name__ == "__main__":
    main()
