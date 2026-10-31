"""Replay against rerun: rerunning the model is a consistency check, not reconstruction. Also per-day prompt texts
and the token-count gap the gateway trace exposed."""
import random
import _paths  # noqa: F401
import world as W

recs = W.records(W.LIVE, W.FIX - 1)
print("CALLS PER DAY BY PROMPT TEXT ACTUALLY SENT (v0 records name text A for all)")
for d in range(W.LIVE, W.FIX):
    day = [r for r in recs if r["day"] == d]
    a = sum(r["sent_prompt"] == W.PROMPT_A for r in day)
    print(f"  day {d}: text A {a:>3}  text B {len(day) - a:>3}")
print()
print("TOKEN GAP: gateway trace input tokens minus rebuilt (commit text + document), every 25th decision")
gaps = {}
for r in recs[::25]:
    g = r["trace_input_tokens"] - (W.tokens(W.PROMPT_A) + r["doc"]["doc_tokens"])
    gaps.setdefault(r["day"], set()).add(g)
for d in sorted(gaps):
    print(f"  day {d}: gaps {sorted(gaps[d])}")
print()
pre = [r for r in recs if (r["day"], r["minute"]) < (W.HOTFIX_DAY, W.HOTFIX_MIN)]
post = [r for r in recs if (r["day"], r["minute"]) >= (W.HOTFIX_DAY, W.HOTFIX_MIN)]
rng = random.Random(9)
print("RERUN AGREEMENT ON loss_location (400 decisions each, seeded rerun wobble 1.5%)")
for name, pool, text in (("before hotfix, rerun with text A", pre, W.PROMPT_A), ("after hotfix, rerun with text A", post, W.PROMPT_A),
                         ("after hotfix, rerun with text B", post, W.PROMPT_B)):
    s = rng.sample(pool, 400)
    agree = sum(W.model(r["doc"], text, rerun_seed=("rerun", r["id"]))["loss_location"] == r["fields"]["loss_location"] for r in s)
    both = sum(r["doc"]["both"] for r in s)
    print(f"  {name:<34} agree {agree} of 400 ({agree / 4:.1f}%); both addresses present {both}")
