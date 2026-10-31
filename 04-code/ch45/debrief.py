"""Debrief from independent scores. Usage: python debrief.py c214|c231|c236|c214-v0"""
import sys, statistics as st
import _paths  # noqa: F401
import world as W
from fieldkit.hiring import debrief, render_debrief, Score

cid = sys.argv[1]
if cid == "c214-v0":
    vals = [v for _, _, v in W.V0_SCORES]
    print(f"old practice on loop v0: mean of observed scores {st.mean(vals):.2f}, rule 'mean of 3 or more' -> hire")
    sc = [Score("panel", r, c, v, "observed in the round and written down at the time") for r, c, v in W.V0_SCORES]
    print(render_debrief(debrief(W.LOOP_V0, "c214 replayed on loop v0", sc)))
else:
    print(render_debrief(debrief(W.LOOP_V1, cid, W.scores(cid))))
