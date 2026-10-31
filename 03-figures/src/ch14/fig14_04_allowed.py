"""Figure 14.4: what Michael Hart allowed, allowed as drafts only, and refused (diagram)."""
from _common import S, save, plt, blank
import pipeline as pl
from decision_tree import classify, CLASSES

allowed = sum(1 for s in pl.ELECTRONIC if s.michael == "allowed")
draft = sum(1 for s in pl.ELECTRONIC if s.michael == "draft only")
fig, ax = S.figure(4.0)
blank(ax, (0, 10), (0, 6.6))
S.box(ax, 0.1, 3.2, 3.1, 2.8, f"runs as built\n{allowed} steps\n\nlookups, rules,\nqueue writes", role="system", fs=10)
S.box(ax, 3.45, 3.2, 3.1, 2.8, f"draft only\n{draft} model steps\n\ncoordinator or\nclinician decides", role="approval", fs=10)
S.box(ax, 6.8, 3.2, 3.1, 2.8, f"refused\n{len(pl.REFUSED)} actions\n\nsubmit, set urgency,\nmessage patients", role="blocker", fs=10)
S.box(ax, 0.1, 0.4, 9.8, 1.6, "red flags always route to a clinician", role="evidence", fs=10.5)
S.arrow(ax, 1.65, 3.2, 1.65, 2.0); S.arrow(ax, 5.0, 3.2, 5.0, 2.0)
save(fig, 4, kind="diagram")
