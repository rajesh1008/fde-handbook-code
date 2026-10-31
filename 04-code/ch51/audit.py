"""Audit the four engagements against the catalog (v1 linter) for the Scoreboard. Deterministic stand-in."""
import _paths  # noqa: F401
from linter import lint, counts
from world import AUDIT, EXPOSED


def main(brief=False):
    grid = {}
    for name, m in AUDIT.items():
        res = lint(m, gated=True)
        grid[name] = res
        c = counts(res)
        print(f"== {name} ({m['phase']}): " + ", ".join(f"{k} {v}" for k, v in c.items()))
        for rid, s, d in res:
            if not brief or s not in ("PASS",):
                print(f"   {rid} {s:5} {d}")
        print(f"   exposed during the engagement and closed: {len(EXPOSED[name])} ({', '.join(EXPOSED[name]) or 'none'})")
    print("\nGRID " + " ".join(f"R{i:02d}" for i in range(1, 16)))
    for name, res in grid.items():
        print(f"{name[:4]} " + " ".join(f"{s:>3}"[:3] for _, s, _ in res))
    flags = sum(s == "FLAG" for res in grid.values() for _, s, _ in res)
    print(f"open FLAG findings across four engagements: {flags}")
    v0 = sum(s == "FLAG" for m in AUDIT.values() for _, s, _ in lint(m, gated=False))
    print(f"open FLAG findings with linter v0: {v0}")


if __name__ == "__main__":
    import sys
    main(brief="--brief" in sys.argv)
