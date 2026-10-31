"""fieldkit v2.4 (Chapter 19): connectors for systems with no API."""
from fieldkit.connectors import (Surface, inventory_report, FileDrop, Message, MailQueue, ScreenSpec,
                                 ScreenConnector, ScreenChanged, Rule, WriteBack, reconcile, parse_x12, edi_status)
import pytest


def test_surface_score_falls_with_unknowns():
    a = Surface("s", "x", "file_export", "read", "Ann", True, "oncall", "notes")
    b = Surface("s", "y", "file_export", "read")
    assert a.score() > b.score() and b.gaps() == ["owner", "sample", "failure_contact", "change_notice"]
    assert inventory_report([a, b])[0][2] == "x"


def test_file_drop_refuses_drift_volume_and_duplicates():
    fd = FileDrop("t", ["a", "b"], 200)
    good = lambda n: ("a,b\n" + "\n".join("1,2" for _ in range(n))).encode()
    for n in (100, 101, 102, 103, 104):
        assert fd.check(f"f{n}", good(n), 100).status == "accepted"
    assert fd.check("dup", good(100), 100).status == "duplicate"
    assert "schema drift" in fd.check("d", b"a,c\n1,2", 100).reasons[0]
    assert fd.check("v", good(40), 100).status == "refused"
    assert fd.missing(False, 201) and not fd.missing(True, 201)


def test_mail_queue_needs_both_keys():
    m = Message("<1@x>", "s", "t", [("a.pdf", b"123")])
    fwd = Message("<2@x>", "s", "FW: t", [("a.pdf", b"123")])
    q = MailQueue(("msg_id",)); [q.accept(x) for x in (m, m, fwd)]
    assert len(q.store) == 2
    q = MailQueue(); [q.accept(x) for x in (m, m, fwd)]
    assert len(q.store) == 1 and len(q.duplicates) == 2


class App:
    def __init__(self, labels): self.l, self.rows, self.n = labels, {}, 0
    def labels(self, name): return self.l
    def read(self, name, key): return self.rows[key]
    def submit(self, name, values, key): self.rows[key] = values; return True, key, None


def test_screen_connector_fails_closed_on_changed_screen():
    spec = ScreenSpec("S", ["Name", "Date"], {"name": "Name"})
    ScreenConnector(App(["Name", "Date"]), [spec]).submit("S", {"name": "x"}, "k")
    with pytest.raises(ScreenChanged):
        ScreenConnector(App(["Name", "New", "Date"]), [spec]).submit("S", {"name": "x"}, "k")


class Target:
    def __init__(self, reject=(), timeout=()):
        self.db, self.reject, self.timeout, self.voided = {}, set(reject), set(timeout), []
    def find(self, key): return key if self.db.get(key, {}).get("ok") else None
    def write(self, r, key):
        self.db[key] = dict(r, ok=key not in self.reject)
        if key in self.reject: return False, key, "R-1"
        if key in self.timeout: self.timeout.discard(key); raise TimeoutError
        return True, key, None
    def readback(self, k): return self.db[k]
    def void(self, k): self.voided.append(k); self.db.pop(k)


def test_writeback_preflight_compensation_and_unknown_outcome():
    t = Target(reject={"b"}, timeout={"c"})
    wb = WriteBack(t, [Rule("P-1", "x>0", lambda r: r["x"] > 0)], ["x"])
    assert wb.submit("a", {"x": 1}).state == "verified"
    assert wb.submit("b", {"x": 1}).state == "held" and t.voided == ["b"]
    assert wb.submit("z", {"x": 0}).reasons == ["preflight P-1"]
    assert wb.submit("c", {"x": 1}).state == "unknown"
    assert wb.submit("c", {"x": 1}).state == "verified" and len(t.db) == 2


def test_reconcile_buckets_every_key_once():
    exp = {"a": {"v": 1}, "b": {"v": 2}, "c": {"v": 3}, "d": {"v": 4}, "e": {"v": 5}}
    act = {"a": {"v": 1}, "b": {"v": 9}, "e": {"v": 5, "shell": 1}, "x": {"v": 0}}
    r = reconcile(exp, act, ["v"], held={"d"}, orphan=lambda r: r.get("shell"))
    assert r.counts() == {"matched": 1, "held": 1, "missing": 2, "extra": 2, "mismatched": 1}


def test_x12_envelope_and_status():
    ok = "ISA*00*a*00*b*ZZ*c*ZZ*d*1*2*U*1*000000001*0*P*>~ST*214*0001~B10*S1*S1*X~L11*2*LG~AT7*D1*NS***20260930*1000~SE*5*0001~IEA*1*000000001"
    sets, errs = parse_x12(ok)
    assert not errs and edi_status(sets[0]) == ("S1", "2", "delivered", "202609301000")
    bad = ok.replace("SE*5", "SE*6")
    assert parse_x12(bad)[1][0][1].startswith("SE01")
