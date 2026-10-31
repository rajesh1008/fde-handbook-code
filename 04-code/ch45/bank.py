"""Count the book's interview bank by round and competency, and print a ten-day study plan.
Reads 02-manuscript/interview-bank.md as it stands when run."""
import collections, pathlib, re
import _paths  # noqa: F401
from fieldkit.hiring import normalize_round

p = pathlib.Path(__file__).resolve().parents[2] / "02-manuscript" / "interview-bank.md"
rows = [[c.strip() for c in l.split("|")[1:-1]] for l in p.read_text().splitlines() if re.match(r"\| Q\d+\.\d+ ", l)]
raw = collections.Counter(r[5].lower() for r in rows)
rounds = collections.Counter(normalize_round(r[5]) for r in rows)
comps = collections.Counter(r[4].lower() for r in rows)
chapters = len({r[1] for r in rows})
print(f"bank snapshot: {len(rows)} questions from {chapters} chapters; {len(raw)} distinct round tags before normalizing")
print("by round: " + ", ".join(f"{k} {v}" for k, v in rounds.most_common()))
print("top competencies: " + ", ".join(f"{k} {v}" for k, v in comps.most_common(8)))
byround = collections.defaultdict(list)
for r in rows:
    byround[normalize_round(r[5])].append(r)
plan = ["screen", "technical", "technical", "scenario", "on-site", "on-site", "hiring manager", "customer panel",
        "principal level", "scenario"]
for d, rnd in enumerate(plan, 1):
    pool = byround[rnd]
    qs = [pool[(d * 7 + k) % len(pool)] for k in range(3)] if pool else []
    print(f"day {d:>2} {rnd:<15} " + " ".join(q[0] for q in qs))
