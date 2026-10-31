import subprocess, sys, pathlib
HERE = pathlib.Path(__file__).parent

def run(*a):
    return subprocess.run([sys.executable, *a], cwd=HERE, capture_output=True, text=True, check=True).stdout

def test_hybrid_leads_but_not_for_clerks():
    out = run("options.py")
    assert "C  79.2" in out and "lead of C over best other (A): 2.8" in out and "intake clerks  A" in out

def test_sequential_fanout_breaks_budget_parallel_holds():
    out = run("fanout.py")
    assert "over 4 s 500/500" in out and "timeout 2500" in out and "over 4 s   0/500" in out

def test_one_call_per_turn_and_identity_and_rollback():
    assert "calls across the boundary: 3 for 3 turns" in run("split.py")
    ident = run("identity.py")
    assert "600/600 turns refused" in ident and "0 results the adjuster may not read" in ident
    assert "flag enforced in brain" in run("rollback.py")
