import subprocess, sys, pathlib
import _paths  # noqa: F401
from fieldkit.security import evidence_check, link_check
import world as W
from residual import REGISTER, Residual

HERE = pathlib.Path(__file__).parent


def test_pass1_matches_chapter_32():
    out = subprocess.run([sys.executable, "passes.py"], cwd=HERE, capture_output=True, text=True).stdout
    assert "pass 1 day 103: asked 41, passed 29, findings raised to date 12, open 12" in out
    assert "pass 2 day 121: asked 41, passed 37" in out
    assert "pass 3 day 129: asked 41, passed 41, findings raised to date 23, open 0, accepted 2 -> passed" in out


def test_morning_expiry_then_rerun():
    assert sum(v.passed for v in evidence_check(W.morning(), W.EVIDENCE, 129, W.SCOPE)) == 39
    assert all(v.passed for v in evidence_check(W.answers(3), W.EVIDENCE, 129, W.SCOPE))
    assert all(v.passed for v in link_check(W.morning()))


def test_change_detector_and_injection():
    out = subprocess.run([sys.executable, "changes.py"], cwd=HERE, capture_output=True, text=True).stdout
    assert "8 approved answers changed" in out and "truth changed: SQ-03" in out
    inj = subprocess.run([sys.executable, "changes.py", "--inject"], cwd=HERE, capture_output=True, text=True).stdout
    assert "9 approved answers changed" in inj and "SQ-28" in inj.split("words or claim changed:")[1].splitlines()[0]


def test_residual_register():
    assert all(not r.lint() for r in REGISTER)
    bad = Residual("X", "F", "r", (3, 4), (3, 4), ["one"], ["Northlight security team"], "Callum Reid", None, [])
    assert len(bad.lint()) == 5


def test_gates_ready_only_after_signoff():
    from fieldkit.security import GateStack
    assert not GateStack("G", W.stack(129)).ready()
    assert GateStack("G", W.stack(130)).ready()
