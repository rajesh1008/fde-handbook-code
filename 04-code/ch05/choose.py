"""Choosing a home: score each home against what a candidate wants, then the
questions that test the employer's answer.

Home scores 0 to 3 per dimension are the chapter's model; profile weights are the
candidate's own and sum to 1.0.
"""
from __future__ import annotations

DIMENSIONS = ["product depth", "platform variety", "frontier model access",
              "stays to production", "commercial exposure", "work changes the core"]

HOME_SCORES = {
    "vendor":     [3, 1, 1, 3, 2, 3],
    "integrator": [1, 3, 1, 2, 3, 1],
    "lab":        [2, 2, 3, 1, 1, 2],
}

PROFILES = {
    "Callum Reid": [0.10, 0.25, 0.05, 0.25, 0.25, 0.10],
    "Sofia Brennan": [0.10, 0.10, 0.40, 0.10, 0.05, 0.25],
}

EMPLOYER_QUESTIONS = [
    ("what does not bend here", "fixed point"),
    ("who paid for the last overrun, and how much", "integration tax"),
    ("show me a field fix that shipped, and how long it took", "reuse route"),
    ("what happens to my utilization target in a blocked month", "duration incentive"),
    ("who owns the system the day after go-live", "exit"),
    ("what am I measured on in my first review", "rewarded metric"),
]


def score(weights):
    assert abs(sum(weights) - 1.0) < 1e-9, "weights must sum to 1.0"
    return {h: round(sum(w * s for w, s in zip(weights, sc)), 2) for h, sc in HOME_SCORES.items()}


def best(weights):
    s = score(weights)
    return max(s, key=s.get), s


def main():
    print("CHOOSING A HOME  (home scores 0-3 per dimension, weighted by the candidate)")
    print("  " + " | ".join(DIMENSIONS))
    for name, w in PROFILES.items():
        top, s = best(w)
        print(f"  {name:<14}" + "  ".join(f"{h} {v:.2f}" for h, v in s.items()) + f"   -> {top}")
    print("QUESTIONS FOR A PROSPECTIVE EMPLOYER")
    for q, tests in EMPLOYER_QUESTIONS:
        print(f"  {q:<58}tests: {tests}")


if __name__ == "__main__":
    main()
