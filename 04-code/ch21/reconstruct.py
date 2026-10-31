"""Listing 21.6: reconstructing one number for an examiner, with and without the chain."""
import _paths  # noqa: F401
import lineage_break as lb
from fieldkit.lineage import LineageStore, RefTables

WITHOUT = [  # (step, system, assumed minutes, recoverable?)
    ("find the report and the run that produced it", "report archive", 15, True),
    ("find the code version that ran on day 66", "git log + deploy notes", 25, True),
    ("find the invoice that fed the line", "mailbox (30-day retention)", 30, True),
    ("find what the extractor read from it", "OCR output folder", 40, True),
    ("find the contracted rate", "rate-card share", 20, True),
    ("find the EUR/USD rate used that morning", "fx_rates.csv, overwritten daily", 90, False),
    ("recompute and compare", "spreadsheet", 20, True),
]
WITH = [("explain(release) prints the chain", "lineage store", 1.5, True),
        ("verify(): hashes, versions, recompute", "lineage store + ref tables", 0.5, True),
        ("open the cited page to show the examiner", "document store", 2.0, True)]

if __name__ == "__main__":
    for name, steps in (("without lineage", WITHOUT), ("with lineage", WITH)):
        mins = sum(s[2] for s in steps)
        lost = [s[0] for s in steps if not s[3]]
        print(f"{name}: {len(steps)} steps, {len({s[1] for s in steps})} systems, about {mins:.0f} min (assumed per-step times)"
              + (f"; cannot answer: {lost[0]}" if lost else "; answer reproduced exactly"))
    refs = RefTables()
    st = LineageStore(refs)
    rel = lb.build(st, refs.register("fx_rates", lb.FX[66], "day 66 07:00", "Marisol Vega (treasury)"))
    print("explain(release):")
    for line in st.explain(rel):
        print("  " + line)
