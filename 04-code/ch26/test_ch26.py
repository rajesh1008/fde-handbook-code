import subprocess, sys, pathlib
HERE = pathlib.Path(__file__).parent

def run(*a):
    return subprocess.run([sys.executable, *a], cwd=HERE, capture_output=True, text=True, check=True).stdout

def test_vendor_number_falls_on_customer_documents():
    out = run("vendor_vs_customer.py")
    assert "90.8%" in out and "68.4%" in out

def test_injected_judge_failure_is_caught():
    out = run("judge_validation.py")
    assert "NOT VALID: TNR 0.45" in out and "VALID for Caldwell" in out

def test_gate_sends_critical_losses_to_owner():
    out = run("regression_gate.py")
    assert out.count("OWNER REVIEW") == 2 and "68.4% -> 76.7%" in out

def test_adjudication_leaves_no_open_items():
    out = run("annotation.py")
    assert "decided by Anne Kessler" in out and "round 2: 9 of 10" in out
