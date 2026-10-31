"""Listing 16.7: the synthetic-to-real gap as a scoreboard line, by slice, with the stop rule applied.

Day 52 runs synthetic v1 against the real 200; day 58 runs synthetic v2. The extractor is the same day-44 stand-in
in both rows, so the only thing that changes is the document set. The day-58 extractor revision is scored last,
as a development number on the 200 it was tuned against."""
import _paths  # noqa: F401
from claimsgen import generate, V1
from standin_sample import sample
from extract_standin import extract
from profile_v2 import profile_from_sample
from score import score
from fieldkit.synthetic import GapLine
from runs import SYN_SEED, SYN_N, V2_SEED

SLICES = {
    "first notice, email": lambda d: d["doc_type"] == "first notice of loss" and d["channel"] == "email",
    "first notice, scan": lambda d: d["doc_type"] == "first notice of loss" and d["channel"] != "email",
    "other document types": lambda d: d["doc_type"] != "first notice of loss",
    "faded scans": lambda d: "faded scan" in d["tags"],
    "all documents": lambda d: True,
}
real = sample()
v2 = profile_from_sample(real)


def acc(docs, version):
    if not docs:
        return None, 0
    s = score(docs, [extract(d, version) for d in docs])
    return s["accuracy"], s["fields"]


def line(syn_docs, verdict, version="v1"):
    rows = {}
    for name, f in SLICES.items():
        a, _ = acc([d for d in syn_docs if f(d)], version)
        b, n = acc([d for d in real if f(d)], version)
        rows[name] = (a, b, n)
    return GapLine(rows, verdict=verdict)


print("day 52: synthetic v1 (report verdict NOT REPRESENTATIVE), extractor v1")
print(line(generate(V1, SYN_N, SYN_SEED), "NOT REPRESENTATIVE: plumbing only").render())
print("day 58: synthetic v2 (report verdict REPRESENTATIVE), extractor v1")
print(line(generate(v2, SYN_N, V2_SEED), "REPRESENTATIVE: regression use").render())
print("day 58: synthetic v2, extractor v2 (development number on the 200 it was tuned against; not a claim)")
print(line(generate(v2, SYN_N, V2_SEED), "REPRESENTATIVE: regression use", "v2").render())
