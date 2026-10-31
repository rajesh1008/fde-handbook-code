"""Chapter 33 lab tests: the numbers the chapter quotes."""
import subprocess, sys, pathlib
import _paths  # noqa: F401
from world import M, DESIGNS, CALDWELL, HARBOURLINE, METRICS_V1, METRICS_V2, VENDOR_IDS, REQUEST
from pack import build

HERE = pathlib.Path(__file__).parent


def test_registers_by_day():
    c = {d: M.counts(M.classify_all(CALDWELL, DESIGNS[d])) for d in (82, 132, 153)}
    assert c[82].get(M.FULL, 0) == 0 and c[132][M.FULL] == 1 and c[153][M.FULL] == 2
    assert c[153][M.REGISTERED] == 4 and c[153][M.NOT_MODEL] == 9


def test_pack_v1_lint_clean_but_two_metrics_need_northlight():
    p = build("v1")
    assert p.items() == 71 and p.lint() == []
    bad = [m.mid for m, b in M.computability(METRICS_V1, "Caldwell", VENDOR_IDS) if b]
    assert bad == ["M4", "M6"]
    assert all(not b for _, b in M.computability(METRICS_V2, "Caldwell", VENDOR_IDS))


def test_validator_map():
    assert sum(q.answer_type == M.BOUNDARY for *_, q in REQUEST) == 3
    assert sum(t == M.BOUNDARY for _, _, t, _ in REQUEST) == 6
    assert [p for *_, q in REQUEST for p in q.problems()] == []


def test_harbourline_reading_moves_vendor_models_into_full_scope():
    hb = M.counts(M.classify_all(HARBOURLINE, DESIGNS[153]))
    assert hb[M.FULL] == 6


def test_pyramid_catches_injection_at_layer_three():
    out = subprocess.run([sys.executable, "pyramid_run.py"], capture_output=True, text=True, cwd=HERE).stdout
    assert "caught at layer: 3" in out and "caught at layer: none" in out
