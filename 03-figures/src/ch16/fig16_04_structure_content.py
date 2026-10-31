"""Figure 16.4: what the generator takes from discovery and what it takes from a model."""
from _common import S, save, blank
fig, ax = S.figure(height=3.9)
blank(ax, (0, 10), (0, 6))
S.box(ax, 0.2, 0.6, 4.4, 4.2, "", role="evidence")
S.box(ax, 5.4, 0.6, 4.4, 4.2, "", role="model")
S.label(ax, 2.4, 5.1, "structure: from discovery", fs=10.5, ha="center", weight="bold")
S.label(ax, 7.6, 5.1, "content: from a model", fs=10.5, ha="center", weight="bold")
for i, t in enumerate(["document-type mix", "channel and scan quality", "exception rates", "field formats"]):
    S.box(ax, 0.5, 3.8 - i * 0.95, 3.8, 0.7, t, role="evidence", fs=10)
for i, t in enumerate(["sentence phrasings", "names and streets", "filler text"]):
    S.box(ax, 5.7, 3.8 - i * 0.95, 3.8, 0.7, t, role="model", fs=10)
save(fig, 4, kind="diagram", data="chapter text, 04-code/ch16/profile_v2.py")
