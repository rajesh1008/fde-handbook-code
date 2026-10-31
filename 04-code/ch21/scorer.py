"""Listing 21.3: the quality scorer at the door, and what it does to downstream exceptions."""
import _paths  # noqa: F401
from collections import Counter
from fieldkit.quality import summarize
from pennant import feed, is_exception, u
from checks import scorer

ANSWER_RATE = 0.80   # senders who answer a request within two business days (stand-in)
RESEND_RATE = 0.70   # senders who resend a legible copy


def run(threshold=None):
    docs = feed()
    s = scorer()
    if threshold is not None:
        import pennant, checks
        pennant.LEGIBLE_AT = threshold
        checks.LEGIBLE_AT = threshold
    verdicts = s.run(docs)
    without = Counter()
    for d in docs:
        if is_exception(d):
            without[_cause(d)] += 1
    withs, awaiting, returned = Counter(), 0, 0
    for d, v in zip(docs, verdicts):
        if v.decision == "accept":
            if is_exception(d):
                withs[_cause(d)] += 1
            continue
        rate = RESEND_RATE if v.decision == "reject" else ANSWER_RATE
        if u(d["doc_id"], "answer") < rate:
            returned += 1
            clean = dict(d, _truth=set(), legibility=max(d["legibility"], 0.9))
            if is_exception(clean, "second"):
                withs["clean"] += 1
        else:
            awaiting += 1
    return docs, verdicts, without, withs, awaiting, returned


def _cause(d):
    return sorted(d["_truth"])[0] if d["_truth"] else ("marginal" if d["legibility"] < 0.75 else "clean")


if __name__ == "__main__":
    docs, verdicts, without, withs, awaiting, returned = run()
    sm = summarize(verdicts)
    print(f"scorer {verdicts[0].scorer_version} on {sm['documents']} documents (deterministic stand-in feed)")
    print(f"  accept {sm['accept']}, request {sm['request']}, reject {sm['reject']}; held at the door {sm['held']} ({sm['held_share']:.1%})")
    truth = sum(1 for d in docs if d["_truth"])
    caught = sum(1 for d, v in zip(docs, verdicts) if d["_truth"] and v.decision != "accept")
    false_hold = sum(1 for d, v in zip(docs, verdicts) if not d["_truth"] and v.decision != "accept")
    print(f"  defective documents {truth}, held {caught}, passed {truth - caught}; clean documents held {false_hold}")
    reasons = Counter(f[1] for v in verdicts for f in v.failures)
    print("  failures by dimension:", dict(sorted(reasons.items())))
    for v in [v for v in verdicts if v.decision != "accept"][:4]:
        print("   ", v.line())
    a, b = sum(without.values()), sum(withs.values())
    print(f"downstream exceptions without the scorer: {a}  " + str(dict(sorted(without.items()))))
    print(f"downstream exceptions with the scorer:    {b}  " + str(dict(sorted(withs.items()))))
    print(f"  change {(b - a) / a:+.0%}; held documents returned and processed {returned}; still awaiting the sender {awaiting}")
