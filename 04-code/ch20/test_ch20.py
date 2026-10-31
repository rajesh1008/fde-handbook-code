"""Chapter 20 lab tests: the numbers the chapter quotes."""
import _paths  # noqa: F401
import pytest
from deploy import check_line, deploy
from estate_configs import CALDWELL, GREYSTONE, PENNANT_EU, with_
from fieldkit.estates import VersionUnavailable, resolve_pin
from iac_check import render, repair_loop, scan
from parity import TIMELINE
from sim_clouds import catalog


def test_all_three_reach_parity():
    for estate, (cfg, events) in TIMELINE.items():
        for _, _, change in events:
            cfg = with_(cfg, **change)
        assert check_line(cfg)[0] == 14, estate


def test_naive_latest_passes_on_another_model():
    ev, rep, _ = deploy(with_(PENNANT_EU, model="extract@latest"))
    assert rep["accuracy"] >= 0.85 and set(rep["served"]) == {"extract-2026-01"}


def test_pin_refused_in_eu_and_greystone_failover():
    with pytest.raises(VersionUnavailable):
        resolve_pin(PENNANT_EU["pin"], catalog("gcp"))
    assert resolve_pin(GREYSTONE["pin"], catalog("azure"))[0] == "westus3"


def test_partial_rescan_misses_the_regression():
    g0 = with_(GREYSTONE, public_access=True, tags_complete=False)
    naive, _ = repair_loop(render(g0), g0["allowed_regions"], False)
    full, trace = repair_loop(render(g0), g0["allowed_regions"], True)
    assert len(scan(naive, g0["allowed_regions"])) == 1 and not scan(full, g0["allowed_regions"]) and trace[-1][0] == 3


def test_adapters_are_small():
    import io, contextlib
    with contextlib.redirect_stdout(io.StringIO()) as out:
        import loc  # noqa: F401
    assert "largest single adapter 16 lines" in out.getvalue()
