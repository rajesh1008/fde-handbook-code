import _paths  # noqa: F401
import caldwell_docs as C
from fieldkit.retrieval import evaluate, Audience

ix, recs, acl, versions = C.build(day=88)
C.apply_register(ix, C.lifecycle_register(versions))
restricted = {p["pid"] for p in recs if p["acl"] != ["claims-all"]}

def test_scoreboard_recall_at_ten():
    assert round(evaluate(ix, C.questions(recs), C.who_for, k=10)["recall"], 2) == 0.86

def test_prefilter_never_leaks():
    tom = C.PEOPLE["tom"]
    for q in C.questions(recs):
        assert not any(p.pid in restricted for p, _ in ix.search(q.text, tom, k=10))

def test_live_claim_gets_current_rule():
    p, _ = ix.search("water loss supply line cause code blank desk adjuster before field inspection", C.PEOPLE["tom"], k=1)[0]
    assert p.doc_id == "CM-WL-07-v3"

def test_draft_never_returned():
    assert not any(p.doc_id == "CM-WL-07-v4" for p, _ in ix.search("water loss cause code first notice of loss", C.PEOPLE["anne"], k=50))

def test_audience_is_intersection():
    both = Audience((C.PEOPLE["tom"], C.PEOPLE["siu"]))
    assert not any(p.pid in restricted for p, _ in ix.search("siu referral prior loss history", both, k=10))
