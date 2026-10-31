"""Listing 6.7, failure injection: the interview says one thing, the shadowing log another (deterministic stand-in).

Step 1 builds the log from the written procedure and the interviews alone, as a team does when it never sits
at the desk. Step 2 adds the day-12 shadowing session. Step 3 records the resolution on day 14.
"""
from caldwell_discovery import build_log
from discovery import naive_coverage

talk = build_log(shadow=False, tracers=False, resolve=False)
print("--- step 1: procedure and interviews only, day 11")
print(naive_coverage(talk, 11))
r = talk.coverage(11)
print(f"fieldkit: {sum(x.covered for x in r.rows)} of {len(r.rows)} paths covered; "
      f"answers stated but not observed: {sum(m == 's' for x in r.rows for m in x.marks.values())}")

seen = build_log(tracers=False, resolve=False)
print("--- step 2: add the day-12 shadowing session at the intake desk")
r = seen.coverage(12)
print(f"paths known: {len(r.rows)}; covered: {', '.join(x.path for x in r.rows if x.covered)}")
for c in r.contradictions:
    print(c.render())

print("--- step 3: Anne Kessler reviews the log with Tom Whitfield on day 14")
seen.resolve("P01", "lag_days", "Anne Kessler", 14,
             "procedure assumes two scan batches; the afternoon batch stopped in 2019")
r = seen.coverage(14)
print(f"P01: {'covered' if [x for x in r.rows if x.path == 'P01'][0].covered else 'not covered'}")
for c in r.contradictions:
    print(c.render())
