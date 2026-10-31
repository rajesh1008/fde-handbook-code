"""After the award: the bid's commitments become the open-decision register, and two of them are renegotiated."""
import _path  # noqa: F401
from fieldkit.bid import extract, lint, to_register
from fieldkit.cadence import Register
from harbourline import RESPONSE_V10, clarifications, OWNER_FOR, DUE_FOR

claims = extract(RESPONSE_V10)
lint(claims, clarifications())
flags = {c.key: c.flags for c in claims}
reg = Register("Harbourline")
moved = to_register(claims, reg, OWNER_FOR, DUE_FOR)
by = {s: sum(r.evidence.endswith(f"[{s}]") for r in moved) for s in "PDV"}
print(f"{len(claims)} claims in the submitted response; {len(moved)} moved to the register "
      f"(P {by['P']}, D {by['D']}, V with a number {by['V']})")
siem = next(r for r in moved if "SIEM within 5 minutes" in r.question)
memos = next(r for r in moved if "score 400" in r.question)
size = next(r for r in moved if "sample size" in r.question)
reg.decide(siem.key, "hourly batch into the SIEM, as the bank ingests third-party sources; a 90-day buffer in the "
           "Canadian tenant; alerts through the bank's alert hook within 5 minutes", 33,
           evidence="Martin Shaw, architecture pre-read, day 33", impact="H-06 renegotiated; no fee change")
reg.decide(memos.key, "600 scored memos before Shadow Exit", 45, evidence="Helen Marsh, model risk letter, day 45",
           impact="F-02 renegotiated; about 83 more credit-officer hours at 25 minutes a memo")
reg.decide(size.key, "600, under the model risk standard", 45, evidence="Helen Marsh, model risk letter, day 45")
for r in (siem, memos):
    print(f"{r.key} {r.evidence.split(',')[0]} \"{r.question}\"")
    print(f"   at submission: {', '.join(flags[r.key]) or 'no flag'}")
    print(f"   decided day {r.decided_day}: {r.decision}")
    print(f"   impact: {r.impact}")
held = 0
for r in moved:
    if r.status == "open" and r.due_day is not None and r.due_day <= 40:
        reg.decide(r.key, "held as written", r.due_day, evidence="evidence attached by the due day")
        held += 1
print(f"held as written by their due day: {held}")
print(reg.status(today=46))
