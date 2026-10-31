"""Cost and latency per document by class: the deterministic-first pipeline against the demo architecture.

STAND-IN PRICES. No provider was called. Prices are illustrative list prices in US dollars, written down here so the
arithmetic can be checked and rerun with a customer's own contract prices. Latencies are drawn from seeded
log-normal distributions with the medians below. Token counts per call are the lab's planning profile, not a
measurement of any provider's tokenizer.

Demo architecture (Chapter 3's demo, carried into a design): one frontier agent per document with the whole
document and all tools in context, calling tools turn by turn until it has done all twelve steps.
"""
import math, random

PRICE = {  # US dollars per million tokens (in, out); compute per step for the two code classes
    "frontier": (3.00, 15.00),
    "small": (0.10, 0.40),
}
COMPUTE_PER_STEP = {"det": 0.00002, "rules": 0.00001}
PLATFORM_PER_DOC = 0.006      # gateway logging, storage, evaluation sampling; paid by both architectures

DOC_TOKENS = {"scan": 3800, "email": 2600, "structured": 900}
SMALL_CALL = dict(tin=1500, tout=40)
FRONTIER_SYNTH = dict(extra_in=6900, tout=900)          # retrieved policy wording, claim history, instructions
DEMO = dict(turns=6, tools_in=3200, growth=450, tout=280)

LAT_MEDIAN_S = {"det": 0.040, "rules": 0.008, "small": 0.35, "frontier": 5.5, "demo_turn": 3.2}
LAT_SIGMA = 0.45


def tok_cost(kind, tin, tout):
    pin, pout = PRICE[kind]
    return (tin * pin + tout * pout) / 1e6


def pipeline_cost(counts, doc_kind):
    """counts = [det, rules, small, frontier] steps run for this document. Returns cost by class and total."""
    d = DOC_TOKENS[doc_kind]
    by = {
        "det": counts[0] * COMPUTE_PER_STEP["det"],
        "rules": counts[1] * COMPUTE_PER_STEP["rules"],
        "small": counts[2] * tok_cost("small", SMALL_CALL["tin"], SMALL_CALL["tout"]),
        "frontier": counts[3] * tok_cost("frontier", d + FRONTIER_SYNTH["extra_in"], FRONTIER_SYNTH["tout"]),
        "platform": PLATFORM_PER_DOC,
    }
    return by, sum(by.values())


def demo_cost(doc_kind):
    d = DOC_TOKENS[doc_kind]; t = DEMO["turns"]
    tin = t * (d + DEMO["tools_in"]) + DEMO["growth"] * t * (t - 1) // 2
    tout = t * DEMO["tout"]
    model = tok_cost("frontier", tin, tout)
    return {"frontier": model, "platform": PLATFORM_PER_DOC}, model + PLATFORM_PER_DOC


def _draw(rng, median):
    return median * math.exp(rng.gauss(0, LAT_SIGMA))


def pipeline_latency(counts, rng):
    """Seconds for one document; steps run in sequence. Returns per-class seconds and total."""
    by = {k: sum(_draw(rng, LAT_MEDIAN_S[k]) for _ in range(n)) for k, n in zip(("det", "rules", "small", "frontier"), counts)}
    return by, sum(by.values())


def demo_latency(rng):
    s = sum(_draw(rng, LAT_MEDIAN_S["demo_turn"]) for _ in range(DEMO["turns"]))
    return {"frontier": s}, s


def pct(xs, q):
    xs = sorted(xs); i = min(len(xs) - 1, max(0, int(round(q * (len(xs) - 1)))))
    return xs[i]
