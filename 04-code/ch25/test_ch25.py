"""Chapter 25 lab: the numbers the chapter prints are the numbers the code produces."""
import subprocess, sys, pathlib
HERE = pathlib.Path(__file__).parent


def out(s, *a):
    return subprocess.run([sys.executable, s, *a], cwd=HERE, capture_output=True, text=True, check=True).stdout


def test_boundaries_deny_production_write_and_refusals():
    o = out("boundaries.py")
    assert "create_claim       prod     -> DENY" in o and "submit_prior_auth  sandbox  -> DENY" in o


def test_failure_injection_makes_duplicates_and_guesses():
    o = out("day109_retry.py")
    assert "business-key duplicates (policy, loss date, claimant): 11" in o
    assert "guessed cause code: 5" in o and "mentioning a retry or duplicate: 0" in o


def test_executor_fixes_the_day():
    o = out("day109_fixed.py")
    assert "duplicates 0" in o and "'verified': 225" in o and "finality" in o


def test_compensation_voids_untouched_and_routes_touched():
    o = out("compensate.py")
    assert "compensated 8  routed to the claims data team 3" in o and "guessed cause code 5" in o


def test_three_records_beat_one():
    o = out("three_records.py")
    assert "accepted unchanged but final record differs: 30" in o and "1155 of 1155 (100.0%)" in o


def test_review_capacity_has_a_best_rate():
    o = out("review_surface.py")
    assert "    50%" in o and "11.0" in o and "33.8" in o


def test_greystone_is_drafts_only():
    o = out("greystone_drafts.py")
    assert "duplicate drafts 0" in o and "submit_prior_auth  boundary" in o


def test_tryit_runs():
    assert "key-per-intent 0" in out("tryit.py", "a")
    assert "allowed=False" in out("tryit.py", "c")
