"""Listing 3.1: score the day-two demo against Anne Kessler's corrections.

Run:  python day2_demo_score.py
The extractor is the DEMO MODEL STAND-IN (deterministic; no model called): see demo_extract.py.
"""
from collections import Counter, defaultdict

from caldwell_docs import FIELDS, caldwell_docs, demo_docs
from demo_extract import STAND_IN_LABEL, extract
from scoring import score


def pct(n, d):
    return f"{100 * n / d:.0f}%"


def main():
    demo = score(demo_docs(), extract)
    cald = score(caldwell_docs(), extract)
    print(f"extractor: {STAND_IN_LABEL}")
    print("scorer: Anne Kessler, Head of Claims, Caldwell Mutual (her corrections, day 2)")
    print("documents: Northlight demo set (10, typed forms) vs Caldwell (10, one week's intake)\n")

    print(f"{'field':<19}{'demo set':>9}{'Caldwell':>10}")
    for f in FIELDS:
        a = sum(r["ok"] for r in demo if r["field"] == f)
        b = sum(r["ok"] for r in cald if r["field"] == f)
        print(f"{f:<19}{a:>6}/10{b:>7}/10")
    a, b = sum(r["ok"] for r in demo), sum(r["ok"] for r in cald)
    print(f"{'ALL FIELDS':<19}{pct(a, len(demo)):>9}{pct(b, len(cald)):>10}   ({a}/100 vs {b}/100)\n")

    print("Caldwell by intake channel")
    by = defaultdict(list)
    for r in cald:
        by[r["channel"]].append(r["ok"])
    for ch in ("email", "fax", "mail"):
        v = by[ch]
        print(f"  {ch:<6} {len(v) // 10} docs  {sum(v):>2}/{len(v)}  {pct(sum(v), len(v))}")

    print("\nCaldwell by document (fields right out of 10)")
    docs = defaultdict(int)
    for r in cald:
        docs[r["doc"]] += r["ok"]
    print("  " + "  ".join(f"{k}:{v}" for k, v in docs.items()))
    print(f"  documents with all ten fields right: {sum(v == 10 for v in docs.values())}")

    misses = [r for r in cald if not r["ok"]]
    print(f"\nWhy the {len(misses)} corrections happened (first reading, checked with Anne)")
    for c, n in Counter(r["cause"] for r in misses).most_common():
        print(f"  {n:>2}  {c}")


if __name__ == "__main__":
    main()
