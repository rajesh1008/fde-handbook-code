"""Figure 44.7: four versions of the hiring loop run through the pyramid, and the layer that caught each."""
from _common import S, save, text, blank
L = text("pyramid_run").splitlines()
loops = [l for l in L if not l.startswith("  ")]
fig, ax = S.figure(height=4.0); blank(ax, (0, 10), (0, 6))
lay = ["L1\ncoverage", "L2\nknown cases", "L3\ncalibration", "L4\npool"]
for j, t in enumerate(lay):
    S.label(ax, 4.3 + j * 1.55, 5.4, t, fs=9, ha="center")
short = ["old loop", "new, no floors", "new, unanchored", "new loop"]
for i, (l, s) in enumerate(zip(loops, short)):
    y = 4.5 - i * 1.15
    S.label(ax, 1.6, y + 0.3, s, fs=9)
    idx = L.index(l)
    for j in range(4):
        v = L[idx + 1 + j].split()[3] if L[idx + 1 + j].split()[1] == "known" else L[idx + 1 + j].split()[2]
        r = {"pass": "approval", "fail": "blocker", "skipped": "evidence"}[v]
        S.box(ax, 3.65 + j * 1.55, y, 1.3, 0.6, v, role=r, fs=9)
save(fig, 7, kind="diagram", data="04-code/ch44/output/pyramid_run.txt")
