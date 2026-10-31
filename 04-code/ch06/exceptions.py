"""Listing 6.3: how much of the watched work was exceptions (deterministic stand-in, 202 documents watched)."""
from collections import Counter
from caldwell_discovery import watched_documents, PATHS

docs = watched_documents()
exc = [d for d in docs if d.exception]
mins = sum(d.work_min for d in docs)
emins = sum(d.work_min for d in exc)
print(f"documents watched: {len(docs)} in 6 sessions, days 12 to 22")
print(f"left the happy path: {len(exc)} ({100 * len(exc) / len(docs):.0f}%)")
print(f"share of hands-on minutes spent on them: {100 * emins / mins:.0f}%")
print("by path (watched)   docs  exceptions  minutes on exceptions")
for p in PATHS:
    ds = [d for d in docs if d.path == p.pid]
    if not ds:
        continue
    e = [d for d in ds if d.exception]
    m = sum(d.work_min for d in ds)
    print(f"  {p.pid} {'doc' if p.documented else 'new'}          {len(ds):>4}  {len(e):>10}  {100 * sum(d.work_min for d in e) / m:>20.0f}%")
print("exception kinds, most common first")
for k, n in Counter(d.exception for d in exc).most_common():
    print(f"  {n:>3}  {k}")
