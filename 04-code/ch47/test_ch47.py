"""Chapter 47 lab tests: the numbers the chapter quotes."""
import subprocess, sys, pathlib, _paths  # noqa: F401
from fieldkit.playbooks import recurrence, lint_playbook, Registry, lint_engagement, check_preconditions
import world
HERE = pathlib.Path(__file__).parent


def run(*a):
    return subprocess.run([sys.executable, *a], cwd=HERE, capture_output=True, text=True, check=True).stdout


def test_twenty_engagements_and_named_customers():
    assert len(world.ENGAGEMENTS) == 20 and world.name("N03") == "Pennant"
    assert sorted(world.by(lambda v: v[3] == "none")) == ["N07", "N13", "N17"]


def test_connectors_repeat_by_name_not_shape():
    r = {x["component"]: x for x in recurrence(world.INSTANCES)}
    c = r["connector to the system of record"]
    assert (c["n"], c["variants"], c["by_name"], c["by_shape"]) == (20, 17, "platform", "bespoke")
    assert r["upfront document quality gate"]["by_shape"] == "platform"
    assert sum(1 for x in r.values() if x["by_name"] != x["by_shape"]) == 4


def test_failure_injection_passes_form_lint_fails_at_n17():
    pb = world.PB1("1.3", False)
    assert lint_playbook(pb, probe=False) == []
    assert check_preconditions(pb, world.ESTATE["N17"]) == []
    assert [f[0] for f in lint_playbook(pb)] == ["P5"]
    fixed = world.PB1("1.4", True)
    assert check_preconditions(fixed, world.ESTATE["N17"])[0][:2] == ("PB-1.S4", "gateway")
    assert check_preconditions(fixed, dict(world.ESTATE["N17"], gateway="fieldkit-direct")) == []
    assert "FAILED" in run("registry_run.py", "n17")


def test_lint_month_15_and_18():
    assert "17 findings at 14 of 20" in run("lint_run.py", "15")
    out = run("lint_run.py", "18")
    assert "0 findings" in out and "registered deviations: 6" in out


def test_loop_and_capacity():
    assert "FDE hours saved 808" in run("loop.py", "ship")
    assert "820 h (0.98 of capacity)" in run("absorb.py", "cap")
    assert "N17 includes 9 days" in run("absorb.py", "ttp")
    assert "0 below" in run("rotation.py").split("months 16 to 18")[1]


def test_pod_loop_fk_n1_moved_its_own_stop():
    import pod_loops as p
    rows, edits = p.replay()
    assert len(rows) == 19 and all(r["reported"] == "green" for r in rows)
    assert max(r["passed"] for r in rows) < 46 and [e[0] for e in edits] == [1, 3, 3]
    assert round(sum(r["usd"] for r in rows), 2) == 626.60
    assert len({x for x, _ in p.check(p.FK_V0)}) == 4 and p.check(p.FK_V1) == []


def test_stop_registry_flags_and_prerun_hash():
    import pod_loops as p
    flags = [r["loop"] for r in p.REGISTRY if r["identity"] in p.BEFORE[r["loop"]]]
    assert flags == ["FK-N1", "BG-1"]
    assert all(r["identity"] not in r["writers"] for r in p.REGISTRY)
    edited = dict(p.STOP_V1, done="43 of 46 adapter contract tests, run by nl-platform-ci")
    assert p.prerun(p.REGISTRY[0], edited).startswith("STOP") and p.prerun(p.REGISTRY[0], p.STOP_V1) == "run"
