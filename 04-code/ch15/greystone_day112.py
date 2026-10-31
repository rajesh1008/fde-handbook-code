"""Chapter 15, second customer: Greystone Health, replayed on days 40, 61, 104 and 112."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "fieldkit"))
from fieldkit.histories import greystone_history, greystone_policy, greystone_fields, greystone_sample, rung_reached_days
from fieldkit.escalation import customer_days

h, pol = greystone_history(), greystone_policy()
for day in (40, 61):
    t = h.replay(day)
    print(t.status_report(day))
    esc, ours, quiet = pol.review(t, day)
    for line in ours + quiet:
        print(line)
    for e in esc:
        print(e.note())
    print()
print("AUDIT of escalations already sent:")
for f in pol.audit(h.replay(61)):
    print("  " + f)
print()
reg = greystone_fields()
print("day 104 delivery:")
print(reg.assess("greystone-referral-sample", greystone_sample(drop_key=True), 99, 104).summary())
print()
print("day 112 redelivery:")
print(reg.assess("greystone-referral-sample", greystone_sample(), 107, 112).summary().split("\nFIELDS")[0])
print()
t = h.replay(112)
print(t.status_report(112))
az = t.requests["azure-subscription"]
print(f"azure-subscription: {az.days_open(112)} days open, {customer_days(az, 112)} on Greystone's side")
print("rungs reached:", rung_reached_days(t))
