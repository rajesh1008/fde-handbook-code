"""fieldkit v3.2 (Chapter 25): release boundaries, per-call authorization, three records, executor."""
from fieldkit.actions import (Grant, ReleaseBoundary, Authorizer, Proposal, ActionLedger, Executor, Recommendation,
                              Response, Outcome, intent_key, render_review)
from fieldkit.connectors import WriteBack, Rule


class Target:
    def __init__(self, timeout_keys=(), reject=()):
        self.rows, self.timeout_keys, self.reject, self.n = {}, set(timeout_keys), set(reject), 0

    def find(self, key):
        return next((i for i, r in self.rows.items() if r["key"] == key and r["status"] == "OPEN"), None)

    def write(self, rec, key):
        self.n += 1
        cid = f"C{self.n}"
        if rec["doc"] in self.reject:
            self.rows[cid] = dict(rec, key=key, status="SHELL")
            return False, cid, "V-118"
        self.rows[cid] = dict(rec, key=key, status="OPEN")
        if key in self.timeout_keys:
            self.timeout_keys.discard(key)
            raise TimeoutError
        return True, cid, ""

    def readback(self, cid):
        return self.rows[cid]

    def void(self, cid):
        self.rows[cid]["status"] = "VOID"
        return True


def boundary():
    return ReleaseBoundary("test", [Grant("read", ("prod",), ("read",), "cto", 1),
                                    Grant("write", ("preprod",), ("create_claim",), "cto", 2)],
                           refused={"set_reserve": "head of claims"})


def setup(**kw):
    t = Target(**kw)
    az = Authorizer(boundary(), protected=("status", "reserve"), rules=[Rule("R1", "has doc", lambda a: "doc" in a)],
                    key_prefix="T")
    led = ActionLedger()
    return t, az, led, Executor(WriteBack(t, verify_fields=("doc",)), az, led, "svc-test", "preprod")


def prop(doc, op="create_claim", env="preprod", **extra):
    return Proposal(intent_key("T", doc, op), op, env, dict(doc=doc, **extra), doc)


def test_boundary_denies_by_default_and_refusals_are_named():
    _, az, _, _ = setup()
    assert az.authorize(prop("d1", env="prod")).stage == "boundary"
    d = az.authorize(prop("d1", op="set_reserve"))
    assert not d.allowed and "head of claims" in d.reasons[0]


def test_protected_fields_and_values():
    _, az, _, _ = setup()
    assert az.authorize(prop("d1", status="CLOSED")).stage == "protected"
    p = prop("d1"); p.args = {}
    assert az.authorize(p).stage in ("values", "key")


def test_write_needs_a_person():
    _, _, led, ex = setup()
    assert ex.run(prop("d1")).state == "awaiting"
    assert ex.run(prop("d1"), approved_by="adjuster").state == "verified"


def test_retry_with_intent_key_does_not_duplicate():
    p = prop("d2")
    t, _, _, ex = setup(timeout_keys={p.intent})
    assert ex.run(p, approved_by="a").state == "unknown"
    assert ex.run(p, approved_by="a").state == "verified"
    assert sum(1 for r in t.rows.values() if r["status"] == "OPEN") == 1


def test_rejection_is_final_for_the_intent():
    p = prop("d3")
    t, az, _, ex = setup(reject={"d3"})
    assert ex.run(p, approved_by="a").state == "held"
    p2 = prop("d3"); p2.args["cause"] = "guessed"
    assert az.authorize(p2).stage == "finality"


def test_compensation_routes_touched_duplicates():
    t, _, led, ex = setup()
    ex.run(prop("d4"), approved_by="a")
    t.rows["C9"] = dict(doc="d4", key="other", status="OPEN")
    assert ex.compensate("C9", "C1").state == "compensated" and t.rows["C9"]["status"] == "VOID"
    assert ex.compensate("C1", "C0", touched_by="reviewer").state == "routed"


def test_three_records_join_and_stay_separate():
    led = ActionLedger()
    led.recommend(Recommendation("r1", "k1", {"a": 1}, "v1", 1))
    led.respond(Response("r1", "rev", "accepted", {"a": 1}, 40, 1))
    led.outcome(Outcome("k1", "extract", {"a": 2}, 2))
    s = led.scoreboard(["a"])
    assert s["accepted_but_outcome_differs"] == 1 and s["rec_matches_outcome"] == 0
    try:
        led.recommend(Recommendation("r1", "k1", {"a": 2}, "v1", 2))
        assert False
    except AssertionError as e:
        assert "never edited" in str(e)


def test_review_renders_payload_not_narrative():
    lines = render_review({"x": 2}, {"x": 1}, ["x"])
    assert lines[0].startswith("! ") and "will write=2" in lines[0]
