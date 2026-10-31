import pytest

import pipeline as pl
import projection as pj
import question_bank as qb
import scoping_doc as sd
from decision_tree import CLASSES, Step, classify, share, split
from day_five import fdes_to_hold


def test_electronic_split_is_64_percent():
    assert split(pl.ELECTRONIC) == {CLASSES[0]: 16, CLASSES[1]: 4, CLASSES[2]: 3, CLASSES[3]: 2}
    assert share(pl.ELECTRONIC) == pytest.approx(0.64)


def test_fax_path_doubles_steps_and_drops_share():
    both = pl.ELECTRONIC + pl.FAX
    assert len(both) == 2 * len(pl.ELECTRONIC)
    assert share(both) == pytest.approx(0.48)


def test_rules_need_an_owner():
    with pytest.raises(ValueError):
        classify(Step("X", "habit", False, True, False))


def test_every_model_step_is_draft_only():
    assert all(s.michael == "draft only" for s in pl.ELECTRONIC if classify(s) in CLASSES[2:])


def test_projection_is_day_140_and_data_bound():
    p = pj.project(pl.ELECTRONIC)
    assert (p["data"], p["pilot"], p["critical"]) == (112, 140, "data")


def test_missing_board_cutoff_costs_nine_days():
    assert pj.project(pl.ELECTRONIC, pj.with_(board_submission_day=66))["pilot"] == 149


def test_absorbing_fax_breaks_date_and_eats_cap():
    p = pj.project(pl.ELECTRONIC + pl.FAX)
    assert p["pilot"] > 250 and p["headroom"] < 50_000
    assert fdes_to_hold(pl.ELECTRONIC + pl.FAX) == 5


def test_draft_fails_and_signed_passes_lint():
    assert len(sd.lint(sd.draft_v03())) == 10
    p = pj.project(pl.ELECTRONIC)
    inv = dict(electronic=412, fax=253, steps_e=25, steps_f=25, det_e=16, model_e=5)
    assert sd.lint(sd.signed_v10(p, inv)) == []


def test_lint_catches_refused_autonomy_and_unbounded_scope():
    doc = [sd.Claim("autonomy", "The system submits to payers.", "proposed design"),
           sd.Claim("scope", "Covers every referral.", "proposed design")]
    kinds = {x.split()[0] for x in sd.lint(doc)}
    assert {"AUTONOMY-REFUSED", "UNBOUNDED-SCOPE"} <= kinds


def test_question_bank_has_four_parts():
    assert qb.lint(qb.BANK) == []
    assert len(qb.lint(qb.DRAFT_DEFECTS)) == 11
    assert qb.tally(qb.BANK, 19)["blocking_open"] == 0
