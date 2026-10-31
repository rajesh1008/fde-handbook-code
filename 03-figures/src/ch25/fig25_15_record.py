"""Figure 25.15: the action record: four groups of fields, written for denials and compensations too."""
from _common import S, save, blank
fig, ax = S.figure(height=4.2)
blank(ax, (0, 10), (0, 6))
groups = [("what", "intent, operation,\nrequest hash", "model"), ("who", "identity, approver,\nenvironment", "system"),
          ("why", "authorizer stage,\nreasons", "evidence"), ("what happened", "state, claim number,\nraw response, links", "approval")]
for i, (h, body, role) in enumerate(groups):
    x, y = (0.2 + (i % 2) * 5.0), (3.3 - (i // 2) * 2.6)
    S.box(ax, x, y, 4.6, 2.2, f"{h}\n\n{body}", role=role, fs=10)
save(fig, 15, kind="diagram", data="04-code/fieldkit/fieldkit/actions.py (ActionRecord)")
