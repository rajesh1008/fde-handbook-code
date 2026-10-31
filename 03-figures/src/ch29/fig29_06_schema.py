"""Figure 29.6: one golden-set record, grouped by what each field is for (Listing 29.5)."""
from _common import S, save, blank
fig, ax = S.figure(height=4.0)
blank(ax, (0, 10), (0, 6.4))
groups = [(0.2, 3.4, "identity", "system", "case_id\nlayer\nstratum"),
          (5.1, 3.4, "inputs", "data", "source_refs\nprovenance\ncontract_version"),
          (0.2, 0.3, "oracle", "evidence", "expected\ncritical_fields\nrubric_version"),
          (5.1, 0.3, "people and time", "approval", "labeled_by\nadjudicated_by\nready_after_day")]
for x, y, title, role, body in groups:
    S.box(ax, x, y, 4.7, 2.7, "", role=role)
    S.label(ax, x + 0.2, y + 2.3, title, fs=10.5, weight="bold")
    S.label(ax, x + 0.3, y + 1.15, body, fs=10, family="monospace", va="center",
            bbox=dict(boxstyle="square,pad=0.2", fc="white", ec="none"))
S.label(ax, 5, 6.25, "a record missing any field is not gate evidence", ha="center", fs=10, weight="bold")
save(fig, 6, kind="diagram", data="04-code/ch29/scenarios.py REQUIRED")
