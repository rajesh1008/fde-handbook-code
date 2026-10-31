"""Try It Yourself 16.A, 16.B and 16.C. Run: python tryit.py a|b|c"""
import dataclasses
import random
import sys
import _paths  # noqa: F401
from claimsgen import generate
from standin_sample import sample
from features import features
from profile_v2 import profile_from_sample
from extract_standin import extract
from score import score
from fieldkit.synthetic import RepresentativenessReport
from fieldkit.deid import k_anonymity
from runs import SYN_N, V2_SEED

real = sample()


def a():
    """Remove one thing from the v2 profile and watch the report catch it."""
    v2 = profile_from_sample(real)
    for label, change in (("as built", {}), ("no faded scans", {"scanned_below": 0.0, "ocr": ("uniform", 0.90, 0.99)}),
                          ("first notices only", {"doc_type": {"first notice of loss": 1.0}})):
        p = dataclasses.replace(v2, **change)
        syn = generate(p, SYN_N, V2_SEED)
        r = RepresentativenessReport([features(d) for d in syn], [features(d) for d in real],
                                     [d["tags"] for d in syn], [d["tags"] for d in real]).run()
        print(f"{label:<20} auc {r.auc_value:.2f}  failures {len(r.failures)}  verdict {r.verdict}")


def b():
    """How many real documents does a gap estimate need? Bootstrap the real accuracy at three sample sizes."""
    per_doc = score(real, [extract(d, "v1") for d in real])["per_doc"]
    rng = random.Random(16)
    for n in (50, 100, 200):
        means = sorted(sum(rng.choice(per_doc) for _ in range(n)) / n for _ in range(2000))
        lo, hi = means[50], means[1949]
        print(f"n={n:<4} real accuracy 95% interval {lo:.1%} to {hi:.1%}  (width {(hi - lo) * 100:.1f} points)")


def c():
    """Choose quasi-identifiers and see the smallest group."""
    rows = [dict(date=d["gold"]["loss_date"], month=(d["gold"]["loss_date"] or "")[:7],
                 town=(d["gold"]["loss_location"] or ", none").rsplit(", ", 1)[-1], type=d["gold"]["loss_type"],
                 doc=d["doc_type"]) for d in real]
    for keys in (["date", "town", "type"], ["month", "town", "type"], ["month", "type"], ["type", "doc"]):
        kmin, sizes = k_anonymity(rows, keys)
        singles = sizes.get(1, 0)
        print(f"{' + '.join(keys):<22} smallest group {kmin:3d}   records alone in their group {singles}")


if __name__ == "__main__":
    {"a": a, "b": b, "c": c}[sys.argv[1] if len(sys.argv) > 1 else "a"]()
