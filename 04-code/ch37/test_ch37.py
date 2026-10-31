import _paths  # noqa: F401
import world
from fieldkit.gates import pack, residual_lint


def test_aggregate_passes_per_class_blocks():
    assert world.caldwell("aggregate").records["Shadow Exit"].status(per_class=False) == "passed"
    assert world.caldwell("perclass").records["Shadow Exit"].status() == "blocked"


def test_terms_pass_with_conditions_and_model_risk_effective_day_157():
    t = world.caldwell("terms")
    eff = {g: (st, d) for g, st, d, _ in t.effective()}
    assert eff["Shadow Exit"] == ("passed with conditions", 157)
    assert eff["Model-Risk Approval"] == ("passed with conditions", 157)
    assert eff["Live Stable"][0] == "not started"


def test_model_risk_held_while_shadow_exit_blocked():
    assert world.caldwell("perclass").held_back() == ["Model-Risk Approval"]


def test_packs_and_residual():
    assert pack(world.pack_logs())["counts"] == {"present": 0, "partial": 4, "missing": 4}
    assert pack(world.pack_day157())["counts"] == {"present": 7, "partial": 1, "missing": 0}
    assert len(residual_lint(world.residual("v1"))) == 3 and residual_lint(world.residual("v2")) == []
