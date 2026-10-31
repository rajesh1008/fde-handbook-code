"""Signature 13 data: the gate stack per customer."""
import _paths  # noqa: F401
from fieldkit.security import GATES, Gate
from world import stacks

for s in stacks():
    cells = []
    for g in s.gates:
        cells.append(f"{g.name}: {g.status}" + (f" d{g.day}" if g.day else ""))
    print(f"{s.customer:<12}" + " | ".join(cells))
    print(f"{'':<12}blocking: {', '.join(s.blocking()) or 'none'}; lint: {s.lint() or 'clean'}")
print()
bad = Gate("security", "conditional", "Priya Natarajan", 67, [("scan in Caldwell's pipeline", "architecture board", None)])
print("a condition written the way it was first minuted:", bad.lint())
