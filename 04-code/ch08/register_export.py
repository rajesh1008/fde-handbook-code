"""The open-decision register: export the scope's open decisions into the engagement decision register
(fieldkit.cadence, Chapter 13) and read it on day 28 and on day 37 if nothing moves. Deterministic stand-in."""
from caldwell_scope import signed

doc = signed()
reg = doc.to_register()
print(reg.status(28))
print()
print("DAY 37, if nobody decides anything")
for key, code, msg in reg.alerts(37):
    print(f"  {key:<6}{code:<9}{msg}")
