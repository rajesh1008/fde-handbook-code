"""Chapter 16 lab tests: the numbers the chapter prints, and the failure injection."""
import _paths  # noqa: F401
from claimsgen import generate, V1
from standin_sample import sample
from extract_standin import extract
from features import features
from profile_v2 import profile_from_sample
from score import score
from fieldkit.synthetic import RepresentativenessReport
from runs import SYN_SEED, SYN_N, V2_SEED

REAL = sample()
SYN = generate(V1, SYN_N, SYN_SEED)


def acc(docs, v="v1"):
    return score(docs, [extract(d, v) for d in docs])["accuracy"]


def test_sample_matches_day47_manifest():
    assert len(REAL) == 200
    assert sum("faded scan" in d["tags"] for d in REAL) == 47


def test_synthetic_v1_has_no_exceptions_and_scores_94():
    assert not any(d["tags"] for d in SYN)
    assert round(acc(SYN) * 100) == 94


def test_failure_injection_collapse_to_71():
    assert round(acc(REAL) * 100) == 71


def test_report_fails_v1_and_passes_v2():
    def rep(docs):
        return RepresentativenessReport([features(d) for d in docs], [features(d) for d in REAL],
                                        [d["tags"] for d in docs], [d["tags"] for d in REAL]).run()
    assert rep(SYN).verdict.startswith("NOT")
    v2 = generate(profile_from_sample(REAL), SYN_N, V2_SEED)
    assert not rep(v2).verdict.startswith("NOT")
    assert abs(acc(v2) - acc(REAL)) * 100 <= 5


def test_generator_is_deterministic():
    assert [d["text"] for d in generate(V1, 20, 3)] == [d["text"] for d in generate(V1, 20, 3)]
