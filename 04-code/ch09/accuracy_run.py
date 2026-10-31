"""Listing 9.7: accuracy by class on 400 synthetic Caldwell documents.

Scored by the lab against the generator's ground truth; this is not a statement about Caldwell's paper, which
Anne Kessler's adjusters score from Chapter 15. The two deterministic steps are real code (parsers.py) run on
planted defects. The model steps are STAND-INS: their silent-error and low-confidence rates are parameters below,
set inside the ranges reported by the studies in the Recent Research box, so the harness can be shown working.
The point of the listing is the shape of failure per class, loud or silent, not the model numbers.
"""
import random
from datetime import date
from parsers import parse_policy, received_date, luhn_digit, Unreadable

rng = random.Random(47)
N = 400
STANDIN = {  # class: (silent error rate, below-threshold rate routed to a person)
    "small: document type": (0.020, 0.055),
    "small: loss cause": (0.035, 0.070),
    "frontier: summary statements": (0.030, 0.050),   # caught = statement with no supporting cited span
}
ROUTING_RULES = {"fast track": lambda amt, sev: amt <= 5000 and sev == "property only"}


def make_doc(i):
    digits = f"{rng.randrange(10**7):07d}"
    pol = f"CM{digits}{luhn_digit(digits)}"
    stamp = date(2026, rng.randint(1, 9), rng.randint(1, 28))
    truth = dict(policy=pol, received=stamp)
    defect = rng.random()
    if defect < 0.04:      # a clerk's typo: one digit changed, check digit no longer holds
        k = rng.randrange(7); bad = digits[:k] + str((int(digits[k]) + 3) % 10) + digits[k + 1:]
        shown = f"CM-{bad}-{pol[-1]}"; truth["defect"] = "policy number fails check digit"
    elif defect < 0.07:    # stamp missing on the scan
        shown = f"CM-{digits}-{pol[-1]}"; stamp = None; truth["defect"] = "no received stamp"
    else:
        shown = f"CM-{digits}-{pol[-1]}"
    stamp_txt = f"RECEIVED {stamp.day:02d} {list('JAN FEB MAR APR MAY JUN JUL AUG SEP OCT NOV DEC'.split())[stamp.month-1]} {stamp.year}" if stamp else ""
    text = f"{stamp_txt}\nFIRST NOTICE OF LOSS  Policy {shown}  Insured Robert Hayes  Claimant Emily Carter\n"
    return text, truth


def score():
    rows = {}
    def add(cls, outcome): rows.setdefault(cls, {"correct": 0, "caught": 0, "silent": 0})[outcome] += 1
    for i in range(N):
        text, truth = make_doc(i)
        for name, fn, key in (("det: policy number", parse_policy, "policy"), ("det: received date", received_date, "received")):
            try:
                got = fn(text)
                add(name, "correct" if got == truth[key] else "silent")
            except Unreadable as e:
                add(name, "caught" if truth.get("defect") == str(e) else "silent")
        for name, (silent, low) in STANDIN.items():
            r = rng.random()
            add(name, "silent" if r < silent else "caught" if r < silent + low else "correct")
        amt, sev = rng.choice([1200, 4800, 5000, 5001, 18000]), rng.choice(["property only", "injury"])
        expected = amt <= 5000 and sev == "property only"
        add("rules: fast-track routing", "correct" if ROUTING_RULES["fast track"](amt, sev) == expected else "silent")
    return rows


if __name__ == "__main__":
    rows = score()
    print(f"{'step (class: what)':<32}{'correct':>8}{'caught':>8}{'silent':>8}   documents: {N} synthetic, scored by the lab")
    for cls, r in rows.items():
        print(f"{cls:<32}{r['correct']:>8}{r['caught']:>8}{r['silent']:>8}")
    det_silent = sum(r["silent"] for k, r in rows.items() if not k.startswith(("small", "frontier")))
    mod_silent = sum(r["silent"] for k, r in rows.items() if k.startswith(("small", "frontier")))
    print(f"silent errors: code steps {det_silent}, model steps {mod_silent} (stand-in rates)")
