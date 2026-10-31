"""Chapter 29 lab: every number the chapter prints, re-run."""
import common as C
import world as W
from fieldkit.pyramid import select_layers

P = C.build()


def test_main_branch_passes_every_layer():
    assert all(r.verdict == "pass" for r in P.run(C.BASE, stop_on_fail=False))


def test_p9_lifts_aggregate_and_is_caught_at_layer_two():
    _, layers = select_layers(["prompts/extract_p9.txt"], C.PATH_RULES)
    res = P.run(dict(C.BASE, prompt="p9"), layers=layers)
    d = C.gate_owner().decide(res)
    assert d["decision"] == "block" and d["caught_at"] == 2
    ext = next(r for r in res if r.check == "extractor slices").metrics
    assert ext["agg"][1] > ext["agg"][0]
    assert C.aggregate_gate(ext["before"], ext["after"])[0] == "pass"


def test_date_library_bump_caught_at_layer_one():
    v, detail, sec, usd, m = C.chk_rules(dict(C.BASE, datelib=4.0))
    assert v == "fail" and sec < 30 and usd == 0


def test_docs_change_runs_nothing_unknown_runs_code():
    assert select_layers(["docs/runbook.md"], C.PATH_RULES)[1] == []
    assert select_layers(["somewhere/new.py"], C.PATH_RULES)[1] == [1, 3]
