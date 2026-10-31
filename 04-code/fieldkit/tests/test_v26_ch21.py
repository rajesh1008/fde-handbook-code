"""fieldkit v2.6 (Chapter 21): quality scorer and lineage chain."""
import pytest
from fieldkit.quality import Check, QualityScorer, summarize, request_for, SourceSpec, SourceRegister
from fieldkit.lineage import LineageStore, RefTables, KINDS


def scorer():
    return QualityScorer([
        Check("has currency", "completeness", lambda d: None if d.get("currency") else "currency missing"),
        Check("legible", "legibility", lambda d: None if d["conf"] >= 0.65 else f"confidence {d['conf']:.2f}"),
        Check("sums", "consistency", lambda d: None if d["total"] == sum(d["lines"]) else "lines do not sum"),
    ], "qs-test")


def test_accept_request_reject():
    s = scorer()
    ok = dict(doc_id="a", currency="EUR", conf=0.9, total=3, lines=[1, 2])
    assert s.score(ok).decision == "accept"
    assert s.score(dict(ok, doc_id="b", currency=None)).decision == "request"
    assert s.score(dict(ok, doc_id="c", conf=0.4, currency=None)).decision == "reject"


def test_weakest_dimension_not_mean():
    v = scorer().score(dict(doc_id="b", currency=None, conf=0.9, total=3, lines=[1, 2]))
    assert v.score == 0.0 and v.mean > 0.6


def test_summary_and_request_text():
    s = scorer()
    vs = s.run([dict(doc_id=str(i), currency=None if i < 2 else "USD", conf=0.9, total=1, lines=[1]) for i in range(10)])
    assert summarize(vs)["held_share"] == 0.2
    msg = request_for(vs[0], "carrier@example.com", {"currency": "ISO currency of the invoice total"})
    assert "will not estimate" in msg and "ISO currency" in msg


def test_register_findings_and_valid_for():
    r = SourceRegister([SourceSpec("fx", None, {"rate": "EUR/USD close"}, "read", None, (), versioned=False)])
    assert len(r.findings("fx")) == 4
    assert r.check_use("fx", ["rate", "spread"], 30, "audit")[0].endswith("spread")


def build(ref):
    st = LineageStore(RefTables())
    s = st.add("source", uri="mail/1.pdf", sha256="aa")
    p = st.add("page", [s], page=1)
    e = st.add("extraction", [p], method="template", fields={"eur": 100.0})
    c = st.add("calculation", [e], function="usd", refs={"fx": ref}, value=110.0)
    cl = st.add("claim", [c], text="USD 110.00", value=110.0)
    r = st.add("release", [cl], report="weekly", approved_by="reviewer")
    return st, r


def test_chain_covers_six_kinds_and_flags_path_reference():
    st, r = build("file:/shared/fx.csv")
    assert st.kinds_covered(r) == list(KINDS)
    probs = st.verify(r, sources={"mail/1.pdf": "aa"})
    assert len(probs) == 1 and "by path" in probs[0]


def test_versioned_reference_recomputes_and_detects_edits():
    refs = RefTables()
    vid = refs.register("fx", {"EUR/USD": 1.1}, "day 1", "treasury")
    st, r = build(vid)
    st.refs = refs
    def rc(n, store):
        return 100.0 * store.refs.get(n.attrs["refs"]["fx"])["EUR/USD"]
    assert st.verify(r, sources={"mail/1.pdf": "aa"}, recompute=rc) == []
    assert "changed" in st.verify(r, sources={"mail/1.pdf": "bb"})[0]
    with pytest.raises(ValueError):
        st.add("page", [r], page=2)
