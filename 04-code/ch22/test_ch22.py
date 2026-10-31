"""Chapter 22 lab tests: the week, the thumb, the step classes and the lineage."""
import _paths  # noqa: F401
from collections import Counter
from shadow_week import week
from thumb import thumb_doc, trace
from pipeline import door, link, index, recompute
from week import feed, fx_registry


def test_week_shape_and_matched_rate():
    docs, bk, res, g, store, refs, fx = week()
    assert len(docs) == 2100
    assert res[0] and refs.meta(fx)["owner"] == "Marisol Vega" and fx.startswith("fx_rates@")
    m = Counter(g)["matched"] / len(docs)
    assert 0.825 <= m < 0.835


def test_thumb_is_silent_on_v1_and_held_on_v2():
    docs, bk = feed()
    d, s = thumb_doc(bk)
    dec, _, seen = door(d, bk, "pennant-qs-1.0")
    linked, how = link(seen, index(bk), "first key")
    assert dec == "accept" and linked == s + 1          # the sibling: wrong, and nothing disagrees
    assert door(d, bk, "pennant-qs-1.1")[0] != "accept"
    assert link(seen, index(bk), "two keys")[0] is None


def test_no_silent_wrong_after_fix_and_every_wrong_was_occluded():
    _, _, _, g1, *_ = week()
    docs, _, _, g2, *_ = week("pennant-qs-1.1", "two keys")
    assert all("occluded" in d["_truth"] for d, x in zip(docs, g1) if x == "silently wrong")
    assert Counter(g2)["silently wrong"] == 0


def test_lineage_verifies_with_versioned_fx():
    docs, bk, res, g, store, refs, fx = week()
    claims = [r["claim"] for r in res if r.get("claim")]
    assert claims and all(not store.verify(c, recompute=recompute) for c in claims[:300])


def test_design_split_holds():
    import steps
    from fieldkit.autonomy import split
    assert list(split(steps.P.PENNANT).values()) == [9, 3, 2, 1]
