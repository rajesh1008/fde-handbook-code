import _path  # noqa: F401
from fieldkit.bid import extract, lint, triage, crosswalk
import harbourline as H


def test_triage_counts_and_misroutes():
    counts, _, mis = triage(H.questions())
    assert sum(counts.values()) == 200 and counts["engineering"] == 85 and counts["joint"] == 55
    assert {m[0] for m in mis} == {"C-07", "G-03", "H-04"}


def test_crosswalk_v06_blocks_and_v10_clean():
    assert len(crosswalk(H.standards("v0.6"))[1]) == 2
    counts, problems = crosswalk(H.standards())
    assert problems == [] and sum(counts.values()) == 47 and counts["deviation requested"] == 3


def test_injected_contradiction_is_caught():
    issues = lint(extract(H.RESPONSE_V09), H.clarifications())
    assert any(code == "CONTRADICTED" and "CL-17" in msg for _, _, code, msg in issues)
    assert any(code == "ESTATE CLAIM WITH VENDOR STATUS" for _, _, code, _ in issues)


def test_submitted_response_has_no_errors():
    issues = lint(extract(H.RESPONSE_V10), H.clarifications())
    assert not [i for i in issues if i[1] == "ERROR"]
