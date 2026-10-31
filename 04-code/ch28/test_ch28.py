"""Chapter 28 lab tests: the numbers the chapter quotes."""
import subprocess, sys, pathlib
import _paths  # noqa: F401
from rules import CARDS
from pipeline import suite, run
from world import injected, make_draft
from loop import agent
from fieldkit.guardrails import Budget, CircuitBreaker
import random


def test_sixty_rules_lint_clean():
    assert len(CARDS) == 60 and [p for c in CARDS for p in c.lint()] == []
    assert sorted(c.rid for c in CARDS if c.status == "VERIFY") == ["I-06", "O-03"]


def test_every_live_rule_has_a_check():
    assert suite("v3").missing() == []


def test_injected_referral_drafts_under_v1_and_routes_under_v2():
    r = injected(); d = make_draft(r, random.Random(5))
    a = [dict(op="queue.write", target="coordinator_queue", identity="svc-greystone-sandbox-read", intent="x", args={})]
    assert run(suite("v1"), r, d, a)["disp"] == "queued"
    assert run(suite("v2"), r, d, a)["fired"] == ["I-04"]


def test_breaker_stops_the_loop_at_three_calls():
    g = agent(Budget(), CircuitBreaker(3))
    assert g["calls"] == 3 and g["stop"].startswith("breaker open")
    assert agent()["calls"] == 50


def test_red_team_v3_zero_escapes():
    out = subprocess.run([sys.executable, "redteam.py"], capture_output=True, text=True, cwd=pathlib.Path(__file__).parent).stdout
    assert "v3: escapes 0 of 140" in out and "v2: escapes 23 of 140" in out
