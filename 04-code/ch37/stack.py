"""Five-gate stack across the four customers and who is accountable in each."""
import _paths  # noqa: F401
import world

t = world.caldwell("terms")
rows = []
for g, st, day, note in t.effective():
    rows.append(("conditional" if "conditions" in st else "passed" if st.startswith("passed") else
                 "not started" if st == "not started" else "in review", day))
print("FIVE-GATE STACK  as of Caldwell day 157 (each customer's own engagement days)")
print(f"{'customer':12} " + " | ".join(("AR", "BC", "SX", "MRA", "LS")))
for name, cells in world.others():
    cells = cells or rows
    print(f"{name:12} " + " | ".join(f"{s}{(' d' + str(d)) if d else ''}" for s, d in cells))
print()
print("WHO IS ACCOUNTABLE")
for cust, kind, exe, gov, scope in world.ACCOUNTABLE:
    print(f"  {cust:18} {kind:15} executive: {exe:42} governance: {gov}")
    print(f"  {'':34} scope: {scope}")
