"""Tests for the Chapter 6 lab (run: /workspace/books/.venv/bin/python -m pytest -q test_ch06.py)."""
import pytest
import caldwell_discovery as cd
from discovery import DiscoveryLog, Note, NoteRejected, naive_coverage, permission_gaps, Step


def test_eleven_paths_three_documented():
    r = cd.build_log().coverage(26)
    assert len(r.rows) == 11 and sum(x.documented for x in r.rows) == 3


def test_day26_coverage():
    r = cd.build_log().coverage(26)
    assert sum(x.covered for x in r.rows) == 9
    assert round(100 * r.covered_volume / r.total_volume, 1) == 98.2
    assert {x.path for x in r.rows if not x.covered} == {"P09", "P11"}


def test_interviews_alone_cover_nothing():
    talk = cd.build_log(shadow=False, tracers=False, resolve=False)
    assert "3 of 3" in naive_coverage(talk, 11)
    assert sum(x.covered for x in talk.coverage(11).rows) == 0


def test_contradiction_blocks_until_resolved():
    log = cd.build_log(tracers=False, resolve=False)
    row = [x for x in log.coverage(12).rows if x.path == "P01"][0]
    assert row.contradicted and not row.covered
    log.resolve("P01", "lag_days", "Anne Kessler", 14, "accepted")
    assert [x for x in log.coverage(14).rows if x.path == "P01"][0].covered


def test_resolution_needs_a_person():
    with pytest.raises(ValueError):
        cd.build_log().resolve("P01", "lag_days", "", 14, "x")


def test_observation_needs_a_count():
    with pytest.raises(NoteRejected):
        Note(12, "shadow", "Tom Whitfield", "P01", "arrive", "seen", n=0)


def test_identifier_rejected():
    with pytest.raises(NoteRejected):
        Note(12, "shadow", "Tom Whitfield", "P01", "arrive", "policy HP612048 on the envelope", n=1)


def test_artifact_answers_counts_not_decisions():
    log = DiscoveryLog("x")
    log.add(Note(1, "artifact", "report", "A", "arrive", "count", attribute="monthly_volume", value=10.0),
            Note(1, "artifact", "report", "A", "decide", "rule"))
    assert log.mark("A", "arrive") == "O" and log.mark("A", "decide") == "a"


def test_permission_gaps():
    roles = {"clerk": ("read",), "desk": ("read", "search")}
    gaps = permission_gaps([Step("find", "all", ("search",), "desk")], roles, "clerk")
    assert gaps and gaps[0][2] == ["desk"]


def test_deterministic():
    a = [(d.token, d.work_min, d.lag_days) for d in cd.watched_documents()]
    assert a == [(d.token, d.work_min, d.lag_days) for d in cd.watched_documents()] and len(a) == 202
