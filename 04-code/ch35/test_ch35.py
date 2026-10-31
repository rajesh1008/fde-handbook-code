"""Chapter 35 lab: the numbers the chapter quotes."""
import _paths  # noqa: F401
from fieldkit.privacy import diff, digest, erasure_trace, generate, lint, minimum_necessary, pii_scan
from world import (CALDWELL, GREYSTONE_DRAWN, NEEDED_FIELDS, PACKET_FIELDS, greystone_config, known_values, pennant,
                   provider_log, referrals)


def test_greystone_generated_map_finds_what_the_drawing_missed():
    gen = generate(greystone_config(122))
    assert (len(GREYSTONE_DRAWN), len(gen), len(diff(GREYSTONE_DRAWN, gen))) == (5, 14, 9)
    found = lint(gen, {"HIPAA"}, owner="Greystone")
    assert len(found) == 5 and len({f.hop for f in found}) == 3
    assert lint(GREYSTONE_DRAWN, {"HIPAA"}, owner="Greystone") == []


def test_greystone_v2_clean_and_digest_reproducible():
    a, b = generate(greystone_config(125)), generate(greystone_config(125))
    assert len(a) == 13 and lint(a, {"HIPAA"}, owner="Greystone") == [] and digest(a) == digest(b)


def test_failure_injection_scan_and_rescan():
    refs = referrals()
    before = pii_scan(provider_log(refs), known=known_values(refs))
    assert before.entries == 600 and before.hit_entries > before.pattern_only > 0
    after = pii_scan(provider_log(refs, fixed=True) * 3, known=known_values(refs))
    assert after.entries == 1800 and after.clean


def test_pennant_erasure_and_caldwell_weights():
    assert sum(not t[3] for t in erasure_trace(pennant(False))) == 2
    assert all(t[3] for t in erasure_trace(pennant(True)))
    assert [f.rule for f in lint(CALDWELL, {"STATE"}, owner="Caldwell")] == ["R1"]


def test_minimum_necessary():
    extra, share = minimum_necessary(PACKET_FIELDS, NEEDED_FIELDS)
    assert len(extra) == 9 and round(share, 2) == 0.56
