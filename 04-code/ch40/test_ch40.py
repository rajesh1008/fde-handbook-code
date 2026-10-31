"""Chapter 40 lab: the numbers the chapter quotes."""
import random
import _paths  # noqa: F401
import world as W, pack as P


def test_disputed_claim_v0_fails_and_rebuild_holds():
    recs = W.records(W.LIVE, W.DISPUTE)
    r = W.disputed(recs)
    assert r["day"] == 169 and r["doc"]["both"] and r["band"] == "review"
    st, _, _ = P.build(r, W.REHEARSAL)
    assert st["prompt and model"] == "contradicted" and not P.complete(st)
    st2, _, text = P.build(r, W.BACKFILL, use_history=True)
    assert st2["prompt and model"] == "reconstructed" and P.complete(st2) and text == W.PROMPT_B
    assert W.model(r["doc"], W.PROMPT_A)["loss_location"] != r["fields"]["loss_location"]


def test_months_later_v0_is_silent():
    v0 = W.records(W.LIVE, W.DISPUTE - 1)
    s = random.Random(40).sample(v0, 40)
    late = [P.build(r, 340)[0]["prompt and model"] for r in s]
    assert late.count("contradicted") == 0 and late.count("inferred") == 40


def test_v1_pinned_verifies_and_tamper_detected():
    recs = W.records(W.FIX, W.FIX + 1)
    assert all(P.build(r, W.FIX + 2)[0]["prompt and model"] == "verified" for r in recs[:200])
    r = recs[5]; r["fields"]["loss_location"] = "x"
    assert P.build(r, W.FIX + 2)[0]["decision"] == "contradicted"


def test_router_bands_match_ch27_shape():
    recs = W.records(W.LIVE, W.LIVE + 9)
    share = sum(r["band"] == "proceed" for r in recs) / len(recs)
    assert 0.59 < share < 0.65
