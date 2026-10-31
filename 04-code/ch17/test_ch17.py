"""Chapter 17 lab checks: the printed claims in the chapter hold when the scripts run."""
import subprocess, sys, pathlib
HERE = pathlib.Path(__file__).resolve().parent


def run(*a):
    return subprocess.run([sys.executable, *a], cwd=HERE, capture_output=True, text=True, check=True).stdout


def test_day64_denials_are_logged_and_nothing_left():
    out = run("day64_deploy.py")
    assert "internet gateways 0, NAT gateways 0" in out
    assert "api.model-provider.example:443" in out and "bytes that left the account: 0" in out
    assert "denied in run 2: 0" in out and "0 breaks" in out


def test_on_behalf_of_recheck_leaks_nothing():
    out = run("obo_recheck.py")
    assert "may not read: 0" in out
    a = int(out.split("results the adjuster may not read: ")[1].split()[0])
    assert f"withheld {a}," in out


def test_three_questions():
    out = run("env_doc.py")
    assert "v2, day 63: 6 answers, 0 findings" in out
    assert "v1, day 57: 4 answers, 0 findings" not in out


def test_keys_and_greystone():
    assert "main.tf.json: 0 literal secret(s)" in run("keys.py")
    assert "CHANGES REQUIRED (4)" in run("greystone_review.py")
