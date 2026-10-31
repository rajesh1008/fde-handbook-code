"""Figure 16.2: how claimsgen.py builds a document: the gold record is drawn first, the text is rendered from it."""
from _common import S, save, blank
fig, ax = S.figure(height=3.9)
blank(ax, (0, 10), (0, 6))
steps = [("profile\nfrom discovery", "evidence"), ("gold record\n(the answers)", "data"),
         ("rendered text\n(phrasings)", "model"), ("OCR noise\n(scan quality)", "blocker")]
for i, (t, role) in enumerate(steps):
    x = 0.1 + i * 2.5
    S.box(ax, x, 3.2, 2.1, 1.4, t, role=role, fs=10)
    if i < 3:
        S.arrow(ax, x + 2.1, 3.9, x + 2.5, 3.9)
S.box(ax, 2.6, 0.6, 4.8, 1.2, "document + its gold record", role="system", fs=10.5)
S.arrow(ax, 8.65, 3.2, 6.5, 1.8)
S.arrow(ax, 3.65, 3.2, 4.2, 1.8, ls="--", weight="data")
S.label(ax, 0.1, 5.3, "the answer exists before the text does", fs=10, color=S.PAL["slate"])
save(fig, 2, kind="diagram", data="04-code/ch16/claimsgen.py")
