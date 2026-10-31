"""Figure 40.10: pinning at record time, from the hash-addressed registry to the chain head in Caldwell's account."""
from _common import S, save, blank
fig, ax = S.figure(height=4.9); blank(ax, (0, 10), (0, 8))
top = [("registry:\nname@hash", "data"), ("gateway checks\nsent hash", "system"), ("run record", "evidence")]
for i, (t, r) in enumerate(top):
    S.box(ax, 0.1 + i * 3.4, 5.5, 2.8, 1.8, t, role=r, fs=10)
    if i: S.arrow(ax, i * 3.4 - 0.5, 6.4, i * 3.4 + 0.1, 6.4)
S.box(ax, 6.9, 1.4, 2.8, 1.8, "daily\nchain head", role="evidence", fs=10)
S.box(ax, 0.1, 1.4, 4.6, 1.8, "Caldwell log account,\nobject lock", role="approval", fs=10)
S.arrow(ax, 8.3, 5.5, 8.3, 3.2); S.arrow(ax, 6.9, 2.3, 4.7, 2.3)
S.box(ax, 3.5, 3.6, 2.6, 1.3, "mismatch:\nblock", role="blocker", fs=9.5)
S.arrow(ax, 4.8, 5.5, 4.8, 4.9, ls="--")
save(fig, 10, kind="diagram", data="04-code/ch40/world.py (v1 record), pack.py (verify, chain_head)")
