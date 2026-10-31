"""Listing 2.1 driver: the hours ledger. Caldwell's first 47 days, rebuilt from calendars, tickets and
commits because nobody logged them, then compared with the deal sheet's assumed mix."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "fieldkit"))
from fieldkit.fixtures import caldwell_tracker
from contracts import DEAL_SHEET

BUCKETS = ("discovery", "access", "model", "integration", "gates", "handover", "blocked")
# (week, bucket, hours) reconstructed for two engineers; deterministic fixture
LEDGER = [
    (1, "discovery", 46), (1, "access", 22), (1, "model", 8),
    (2, "discovery", 30), (2, "access", 28), (2, "model", 14), (2, "blocked", 10),
    (3, "discovery", 12), (3, "access", 30), (3, "model", 26), (3, "integration", 8), (3, "blocked", 12),
    (4, "access", 24), (4, "model", 30), (4, "integration", 16), (4, "gates", 6), (4, "blocked", 14),
    (5, "access", 18), (5, "model", 22), (5, "integration", 24), (5, "gates", 10), (5, "blocked", 18),
    (6, "access", 16), (6, "model", 20), (6, "integration", 26), (6, "gates", 14), (6, "blocked", 16),
    (7, "access", 20), (7, "model", 18), (7, "integration", 22), (7, "gates", 16), (7, "blocked", 14),
]


def totals(ledger=LEDGER):
    out = {b: 0 for b in BUCKETS}
    for _, b, h in ledger:
        if b not in out:
            raise ValueError(f"unknown bucket {b!r}: every hour goes in one of {BUCKETS}")
        out[b] += h
    return out


def main(today=47):
    t = totals()
    total = sum(t.values())
    plan = DEAL_SHEET["caldwell"]
    sheet = dict(discovery=plan.discovery_h, access=plan.access_h, model=plan.model_h,
                 integration=plan.integration_h, gates=plan.gates_h, handover=plan.handover_h, blocked=0)
    sheet_total = sum(sheet.values())
    print(f"HOURS LEDGER  Caldwell Mutual  days 1-{today}  (reconstructed, not logged)")
    print(f"{'bucket':<13}{'hours':>6}{'share':>8}{'deal sheet share':>18}")
    for b in BUCKETS:
        print(f"{b:<13}{t[b]:>6}{t[b]/total:>8.0%}{sheet[b]/sheet_total:>18.0%}")
    print(f"{'total':<13}{total:>6}")
    print(f"integration tax to date: {t['integration']/t['model']:.2f} hours per model hour "
          f"(deal sheet {plan.integration_tax:.2f})")
    print(f"model work share: {t['model']/total:.0%} of hours (deal sheet {plan.model_h/sheet_total:.0%})")
    tr = caldwell_tracker()
    w = tr.waiting(today)
    print("blocked hours trace to: " + "; ".join(f"{r.key} ({r.days_open(today)} days, {r.owner})" for r in w if r.blocks))


if __name__ == "__main__":
    main()
