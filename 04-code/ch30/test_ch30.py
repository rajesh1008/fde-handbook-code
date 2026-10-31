"""Chapter 30 lab checks: the numbers the chapter prints."""
import _paths  # noqa: F401
import lab
import models as M


def test_failure_injection_numbers():
    S = lab.sets(); m = lab.ft1()
    assert lab.n_right(m.predict(S["test"]), S["test"], "label") > lab.n_right(M.frontier(S["test"]), S["test"], "label")
    assert lab.n_right(M.frontier(S["anne"]), S["anne"]) == 796
    assert lab.n_right(m.predict(S["legal"]), S["legal"]) < 10


def test_guard_fixes_absent_class_without_holding_in_scope():
    S = lab.sets(); m = lab.ft1()
    g = lab.guarded(m, S["anne"])
    assert lab.n_right(g, S["anne"]) == lab.n_right(m.predict(S["anne"]), S["anne"]) + 5
    assert lab.n_right(lab.guarded(m, S["legal"]), S["legal"]) == 60
    assert not any(p.startswith("hold") for p, d in zip(g, S["anne"]) if d.truth != "none")


def test_deterministic():
    assert [d.id for d in lab.sets()["anne"][:5]] == [d.id for d in __import__("world").anne()[:5]]
