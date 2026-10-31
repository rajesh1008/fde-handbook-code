"""Accuracy is defined by who scores it: three of Caldwell's scorers on one calibration set (deterministic stand-in).

60 synthetic first-notice documents built to Caldwell's layouts (no customer data), one set of system outputs,
14 fields. Anne Kessler, Tom Whitfield and a second senior adjuster each mark every field right or wrong,
independently. Round 1 is before any definitions were written; round 2 is after the day-25 alignment session
wrote definitions for date_received and loss_location. Disagreement is generated per field and scorer from fixed
seeds; no model is called and no adjuster's real marks are held.
"""
from __future__ import annotations

import random

FIELDS = ["policy_number", "insured_name", "claimant_name", "date_of_loss", "time_of_loss", "loss_location",
          "line_of_business", "police_report_number", "vehicle_or_property_id", "reported_by", "contact_phone",
          "date_received", "injury_reported", "cause_of_loss"]
SCORERS = ["Anne Kessler", "Tom Whitfield", "senior adjuster B"]
N_DOCS = 60
# chance the system output is actually right, per field (stand-in)
P_RIGHT = {f: 0.95 for f in FIELDS}
P_RIGHT.update(policy_number=0.97, contact_phone=0.93, date_received=0.90, loss_location=0.91,
               injury_reported=0.88, cause_of_loss=0.85)
# chance a scorer marks against the truth because the field is open to reading (per round)
READING = {1: dict(date_received=0.16, loss_location=0.13, injury_reported=0.10, cause_of_loss=0.20),
           2: dict(date_received=0.01, loss_location=0.015, injury_reported=0.09, cause_of_loss=0.18)}
LEAN = {"Anne Kessler": 0.0, "Tom Whitfield": 0.6, "senior adjuster B": -0.4}   # Tom stricter, B more lenient
FLOOR = 0.005                                            # slips on any field


def marks(rnd: int, seed: int = 189):
    rng = random.Random(seed)
    truth = {(d, f): rng.random() < P_RIGHT[f] for d in range(N_DOCS) for f in FIELDS}
    out = {}
    for s in SCORERS:
        r2 = random.Random(f"{seed}-{rnd}-{s}")
        for (d, f), t in truth.items():
            p = READING[rnd].get(f, 0.0)
            # a lean makes the scorer stricter (marks right as wrong) or lenient (wrong as right)
            if t:
                flip = r2.random() < FLOOR + p * max(0.2, 1 + LEAN[s]) / 2
            else:
                flip = r2.random() < FLOOR + p * max(0.2, 1 - LEAN[s]) / 2
            out[(s, d, f)] = (not t) if flip else t
    return truth, out


def kappa(a: list, b: list) -> float:
    n = len(a)
    po = sum(x == y for x, y in zip(a, b)) / n
    pa, pb = sum(a) / n, sum(b) / n
    pe = pa * pb + (1 - pa) * (1 - pb)
    return 1.0 if pe == 1 else (po - pe) / (1 - pe)


def per_field(rnd: int):
    _, m = marks(rnd)
    rows = []
    for f in FIELDS:
        cols = {s: [m[(s, d, f)] for d in range(N_DOCS)] for s in SCORERS}
        pairs = [(SCORERS[i], SCORERS[j]) for i in range(3) for j in range(i + 1, 3)]
        ks = [kappa(cols[x], cols[y]) for x, y in pairs]
        agree = sum(len({cols[s][d] for s in SCORERS}) == 1 for d in range(N_DOCS)) / N_DOCS
        rows.append((f, sum(ks) / 3, agree))
    return rows


def accuracy_by_scorer(rnd: int, fields=None):
    _, m = marks(rnd)
    fields = fields or FIELDS
    return {s: sum(m[(s, d, f)] for d in range(N_DOCS) for f in fields) / (N_DOCS * len(fields)) for s in SCORERS}


if __name__ == "__main__":
    print(f"CALIBRATION  Caldwell Mutual  {N_DOCS} synthetic documents x {len(FIELDS)} fields x {len(SCORERS)} scorers")
    r1, r2 = per_field(1), per_field(2)
    print(f"{'field':<24}{'round 1 kappa':>14}{'all agree':>11}{'round 2 kappa':>15}  verdict")
    exact = []
    for (f, k1, a1), (_, k2, a2) in zip(r1, r2):
        v = "exact check" if k2 >= 0.8 else "judgment range"
        if k2 >= 0.8:
            exact.append(f)
        print(f"{f:<24}{k1:>14.2f}{a1:>11.0%}{k2:>15.2f}  {v}")
    print(f"fields at kappa >= 0.80: round 1 {sum(k >= 0.8 for _, k, _ in r1)} of 14, "
          f"round 2 {sum(k >= 0.8 for _, k, _ in r2)} of 14")
    for rnd in (1, 2):
        acc = accuracy_by_scorer(rnd)
        spread = max(acc.values()) - min(acc.values())
        print(f"round {rnd} accuracy, all 14 fields, same outputs:  " +
              "  ".join(f"{s.split()[0] if s != 'senior adjuster B' else 'adjuster B'} {v:.1%}" for s, v in acc.items())
              + f"  spread {spread * 100:.1f} points")
    acc = accuracy_by_scorer(2, exact)
    print(f"round 2 accuracy, {len(exact)} exact fields only:      " +
          "  ".join(f"{s.split()[0] if s != 'senior adjuster B' else 'adjuster B'} {v:.1%}" for s, v in acc.items())
          + f"  spread {(max(acc.values()) - min(acc.values())) * 100:.1f} points")
    print("judgment fields -> OD-5 (cause of loss framework, Anne Kessler, due day 35); reported as a range until then")
