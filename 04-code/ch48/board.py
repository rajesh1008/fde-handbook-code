"""The quarterly board scoreboard: four production quarters per customer, each measure scored by the customer's own
scorer on its own documents, with a 95% Wilson upper bound. v0 is the blended Northlight board line (one accuracy
across all three, weighted by sample), which this book does not allow; it is printed to show what it hides.
Writes output/data.json for the figures. Deterministic stand-in."""
import json
import _paths
from fieldkit.evals import wilson
from world import CUSTOMERS, MONTHLY, span


SCORER_NOTES = {"Pennant": "days 344-427 Dana Whitaker on leave; weeks of days 344-353 read late by Rosa Delgado; "
                           "from day 354 scored by Tasha Greene, named deputy"}


def quarters(c):
    d, m = CUSTOMERS[c], MONTHLY[c]
    rows = []
    for q in range(4):
        ms = range(3 * q, 3 * q + 3)
        k = sum(m["errors"][i] for i in ms); n = d["sample"] * 3
        over = [i + 1 for i in ms if m["errors"][i] >= d["line"]]
        near = [i + 1 for i in ms if d["line"] - 1 == m["errors"][i]]
        rows.append(dict(q=q + 1, days=f"{span(c, 3 * q + 1)[0]}-{span(c, 3 * q + 3)[1]}", errors=k, n=n,
                         rate=round(k / n, 4), upper=round(wilson(k, n)[1], 4), over=over, near=near,
                         readiness=m["readiness"][3 * q + 2], hours=sum(m["hours"][i] for i in ms),
                         volume=round(sum(m["volume"][i] for i in ms) / 3)))
    return rows


def blended():
    out = []
    for q in range(4):
        k = n = 0
        for c in CUSTOMERS:
            r = quarters(c)[q]; k += r["errors"]; n += r["n"]
        out.append(round(100 * (1 - k / n), 1))
    return out


def main():
    print("QUARTERLY BOARD SCOREBOARD  per customer, customer-scored  (deterministic stand-in)")
    print(f"v0 blended Northlight line (not allowed in this book): accuracy by quarter {blended()} %")
    data = {"blended": blended(), "customers": {}}
    for c, d in CUSTOMERS.items():
        print(f"\n{c}: {d['measure']} a month, scored by {d['scorer']}; line {d['line']} a month; decides "
              f"{d['decider']}")
        print(f"  {'quarter':<8}{'days':<10}{'errors':>8}{'rate':>8}{'upper':>8}{'over line':>11}{'readiness':>11}"
              f"{'NL hours':>10}")
        qs = quarters(c)
        for r in qs:
            print(f"  Q{r['q']:<7}{r['days']:<10}{str(r['errors']) + '/' + str(r['n']):>8}{r['rate']:>8.2%}"
                  f"{r['upper']:>8.2%}{str(r['over'] or '-'):>11}{r['readiness']:>11.3f}{r['hours']:>10}")
        near = [i + 1 for i, e in enumerate(MONTHLY[c]["errors"]) if e == CUSTOMERS[c]["line"] - 1]
        print(f"  months one error under the line: {near or 'none'}")
        if c in SCORER_NOTES:
            print(f"  scorer note: {SCORER_NOTES[c]}")
        if MONTHLY[c]["proceed"]:
            print(f"  proceed share by month: {MONTHLY[c]['proceed']}")
        data["customers"][c] = dict(monthly=MONTHLY[c], quarters=qs, line=d["line"], sample=d["sample"],
                                    go_live=d["go_live"])
    ys = {c: sum(MONTHLY[c]["hours"]) for c in CUSTOMERS}
    print(f"\nNorthlight hours, twelve production months: {ys}")
    print("months at or over the customer's line: " + "; ".join(
        f"{c} {[i + 1 for i, e in enumerate(MONTHLY[c]['errors']) if e >= CUSTOMERS[c]['line']] or 'none'}"
        for c in CUSTOMERS))
    (_paths.OUT / "data.json").write_text(json.dumps(data, indent=1))
    return data


if __name__ == "__main__":
    main()
