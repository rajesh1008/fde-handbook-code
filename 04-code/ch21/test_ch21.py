import subprocess, sys, pathlib
HERE = pathlib.Path(__file__).parent

def run(*a):
    return subprocess.run([sys.executable, *a], cwd=HERE, capture_output=True, text=True, check=True).stdout

def test_feed_shape():
    out = run("variability.py")
    assert "layouts 41, kinds 5, countries 11" in out and "(76.0%)" in out

def test_scorer_holds_and_cuts_exceptions():
    out = run("scorer.py")
    assert "held at the door" in out and "change -" in out

def test_lineage_breaks_then_holds():
    assert "reference 'fx_rates' cited by path" in run("lineage_break.py")
    assert "chain holds" in run("lineage_break.py", "fixed")
