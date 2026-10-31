"""Chapter 14: the autonomy decision tree applied to every step of Greystone's referral pipeline.

The four classes and the order of the questions follow Chapter 9 [CHECK ch09]. This module is a chapter-local
stand-in until the Chapter 9 module lands in fieldkit; the classification is computed from three recorded facts
about each step, never typed by hand.

    Q1  Is the output fully determined by a lookup, a calculation, a format or a write to a system of record?
        yes -> deterministic service
    Q2  Is it a decision from a finite written rule set that a named person at the customer maintains?
        yes -> rules plus guardrails
    Q3  Is the input free text or an image but the output a closed set or a fixed schema a check can verify?
        yes -> constrained small model
    else -> frontier model with retrieval
"""
from __future__ import annotations
from dataclasses import dataclass

CLASSES = ("deterministic service", "rules plus guardrails", "constrained small model", "frontier model with retrieval")
SHORT = {CLASSES[0]: "det", CLASSES[1]: "rules", CLASSES[2]: "small", CLASSES[3]: "frontier"}


@dataclass(frozen=True)
class Step:
    n: str              # "E07" electronic path, "F07" fax path
    name: str
    determined: bool    # Q1
    written_rules: bool  # Q2
    closed_output: bool  # Q3
    rule_owner: str = ""  # who maintains the rules (Q2 needs a person)
    michael: str = "allowed"   # allowed | draft only | refused (Michael Hart's ruling, day 17)


def classify(s: Step) -> str:
    if s.determined:
        return CLASSES[0]
    if s.written_rules:
        if not s.rule_owner:
            raise ValueError(f"{s.n}: rules with no named owner are not rules, they are habits")
        return CLASSES[1]
    if s.closed_output:
        return CLASSES[2]
    return CLASSES[3]


def split(steps) -> dict:
    out = {c: 0 for c in CLASSES}
    for s in steps:
        out[classify(s)] += 1
    return out


def share(steps, cls=CLASSES[0]) -> float:
    steps = list(steps)
    return split(steps)[cls] / len(steps)
