import pytest
from fieldkit.retrieval import Index, Principal, Audience, Question, evaluate, context_header, acl_drift, CostMeter

def recs():
    base = dict(section="water loss", effective_from=20220101)
    return [dict(base, pid="a1", doc_id="A-v1", text="cause code optional blank", acl=["all"]),
            dict(base, pid="a2", doc_id="A-v2", text="cause code required before payment", acl=["all"], effective_from=20240901),
            dict(base, pid="s1", doc_id="S", text="cause code fraud indicator", acl=["siu"]),
            dict(base, pid="n1", doc_id="N", text="cause code orphan", acl=[])]

def ix():
    i = Index(); i.ingest(recs()); return i

def test_ingest_fails_closed_without_acl():
    i = ix(); assert "n1" not in i.passages and i.refused == [("n1", "no ACL on the source record")]

def test_duplicate_pid_refused():
    i = ix(); i.ingest([dict(pid="a1", doc_id="X", text="x", acl=["all"])])
    assert i.refused[-1] == ("a1", "duplicate passage id")

def test_prefilter_and_postfilter():
    i = ix(); u = Principal("u", frozenset({"all"}))
    assert all(p.pid != "s1" for p, _ in i.search("cause code fraud", u, mode="lexical"))
    assert any(p.pid == "s1" for p, _ in i.search("cause code fraud", u, mode="lexical", acl="none"))
    assert len(i.search("fraud", u, k=1, mode="lexical", acl="post")) == 0

def test_supersession_requires_successor_and_date():
    i = ix()
    with pytest.raises(ValueError):
        i.set_state("A-v1", "superseded")
    i.set_state("A-v1", "superseded", superseded_by="A-v2", on=20240901)
    u = Principal("u", frozenset({"all"}))
    assert [p.pid for p, _ in i.search("cause code optional blank", u, mode="lexical")] == ["a2"]
    p = i.search("cause code optional blank", u, mode="lexical", as_of=20230101)[0][0]
    assert p.pid == "a1" and "SUPERSEDED by A-v2" in context_header(p, 20250101)

def test_audience_intersection_and_drift():
    i = ix(); a = Audience((Principal("x", frozenset({"all", "siu"})), Principal("y", frozenset({"all"}))))
    assert not a.can_read(i.passages["s1"]) and a.can_read(i.passages["a2"])
    assert acl_drift(i, {"A-v2": ["siu"]}) == [("A-v2", "broader")]
    assert i.sync_acl({"A-v2": ["siu"]}, day=5) == ["A-v2"] and acl_drift(i, {"A-v2": ["siu"]}) == []

def test_evaluate_and_cost():
    i = ix(); u = Principal("u", frozenset({"all"}))
    e = evaluate(i, [Question("q", "required before payment", "lookup", ("a2",)), Question("n", "pets", "none")], u, mode="lexical")
    assert e["n"] == 1 and e["recall"] == 1.0 and e["mrr"] == 1.0
    m = CostMeter(); m.add("x", "Caldwell", "", "monthly", 1.0); m.add("y", "Caldwell", "CC", "monthly", 2.0)
    assert [l.item for l in m.unattributed()] == ["x"] and m.monthly_by_payer() == {"Caldwell": 3.0}
