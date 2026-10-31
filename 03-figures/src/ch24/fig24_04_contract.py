"""Figure 24.4: the one call per turn, request and response fields (split.py, fieldkit.surface TurnRequest/TurnResponse)."""
from _common import S, save, blank, text
assert "calls across the boundary: 3 for 3 turns" in text("split")
fig, ax = S.figure(height=4.2)
blank(ax, (0, 10), (0, 6))
S.box(ax, 0.2, 0.4, 3.9, 4.6, "", role="system")
S.box(ax, 5.9, 0.4, 3.9, 4.6, "", role="evidence")
S.label(ax, 2.15, 5.3, "surface sends", fs=11, ha="center", weight="bold")
S.label(ax, 7.85, 5.3, "brain returns", fs=11, ha="center", weight="bold")
req = ["turn_id", "conversation_id", "surface_version", "text", "assertion: aud nl-brain"]
res = ["mode", "answer or none", "citations", "partial sources", "verification", "audit_id"]
for i, f in enumerate(req):
    S.label(ax, 0.45, 4.4 - i * 0.8, f, fs=10, family="monospace", bbox=dict(boxstyle="square,pad=0.15", fc="white", ec="none"))
for i, f in enumerate(res):
    S.label(ax, 6.15, 4.5 - i * 0.7, f, fs=10, family="monospace", bbox=dict(boxstyle="square,pad=0.15", fc="white", ec="none"))
S.arrow(ax, 4.2, 3.6, 5.8, 3.6, weight="emphasis"); S.arrow(ax, 5.8, 1.6, 4.2, 1.6, weight="emphasis")
S.label(ax, 5.0, 3.85, "1 call", fs=10, ha="center", weight="bold")
save(fig, 4, kind="diagram", data="04-code/ch24/output/split.txt")
