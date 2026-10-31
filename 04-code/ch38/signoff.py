"""Sam Oakley's sign-off and the gate stack the pilot waited on (Signature 13 data, Greystone row)."""
import _paths  # noqa: F401
from fieldkit.security import GateStack
import world as W
from residual import REGISTER

for d in (103, 121, 129, W.SIGNOFF_DAY):
    gs = GateStack("Greystone", W.stack(d))
    print(f"day {d:>3}: " + " | ".join(f"{g.name} {g.status}" + (f" d{g.day}" if g.day else "") for g in gs.gates))
    print(f"         blocking: {', '.join(gs.blocking()) or 'none'}; lint: {'; '.join(gs.lint()) or 'clean'}; ready: {gs.ready()}")
gs = GateStack("Greystone", W.stack(W.SIGNOFF_DAY))
print("conditions carried by the gates:")
for g in gs.gates:
    for t, o, due in g.conditions:
        print(f"   {g.name}: {t} ({o}, day {due})")
print(f"residual risks attached: {', '.join(r.id for r in REGISTER)} (review day {min(r.review_day for r in REGISTER)})")
print(f"model risk evidence: recall at five 0.95 on 120 questions from the day-112 sample, bar 0.90 (Michael Hart's reviewers)")
print(f"pilot: day {W.PILOT_DAY}, draft-only, two clinics; Exhibit A acceptance window opens day {W.PILOT_DAY}")
print("projection made at scope sign-off (day 19) against actual:")
for m, plan, act in W.MILESTONES:
    print(f"   {m:<26} planned day {plan:>3}  actual day {act:>3}  ({act - plan:+d})")
print(f"   board-slip scenario for the pilot: day {W.BOARD_SLIP_PILOT}")
