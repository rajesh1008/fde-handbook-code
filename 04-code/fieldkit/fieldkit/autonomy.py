"""fieldkit.autonomy: the autonomy decision tree (Signature 3) as data.  Module version 1.3 (Chapter 9).

Four classes, three questions asked in a fixed order, stop at the first yes:
  Q1 Is the output fixed by a lookup, a calculation, a format or a write to a system of record?  -> deterministic service
  Q2 Is it a decision from a finite written rule set that a named person maintains?               -> rules plus guardrails
  Q3 Is the input free text or an image, and the output a closed set or schema a check can verify? -> constrained small model
  otherwise                                                                                        -> frontier model with retrieval
Two refusals are part of the tree, not advice about it:
  - a Q2 yes with no named rule owner raises: rules with no named owner are not rules, they are habits;
  - a Q3 yes with no named check raises: a closed output nobody checks is not closed.
And one guard: a step classified to a model class may not perform a join, arithmetic, a threshold or an identity
decision (NEVER). Such a step is split, and the forbidden operation goes to a deterministic step.
"""
from dataclasses import dataclass, field

AUTONOMY_VERSION = "1.3"
CLASSES = ("deterministic service", "rules plus guardrails", "constrained small model", "frontier model with retrieval")
SHORT = ("det", "rules", "small", "frontier")
NEVER = ("join", "arithmetic", "threshold", "identity")

TREE = (
    dict(key="Q1", ask="Is the output fixed by a lookup, a calculation, a format or a write to a system of record?",
         attr="determined", yes=0),
    dict(key="Q2", ask="Is it a decision from a finite written rule set that a named person maintains?",
         attr="written_rules", yes=1, requires="rule_owner",
         refusal="rules with no named owner are not rules, they are habits"),
    dict(key="Q3", ask="Is the input free text or an image, and the output a closed set or schema a check can verify?",
         attr="closed_output", yes=2, requires="check", refusal="a closed output nobody checks is not closed"),
)
FALLBACK = 3


class TreeError(ValueError):
    """The tree refused to classify a step as written."""


@dataclass(frozen=True)
class Step:
    n: str
    name: str
    determined: bool = False
    written_rules: bool = False
    closed_output: bool = False
    rule_owner: str | None = None
    check: str | None = None
    ops: tuple = field(default=())


def walk(step, tree=TREE):
    """Return (class index, the answers asked in order), raising TreeError on a refusal or a NEVER breach."""
    answers = []
    cls = FALLBACK
    for node in tree:
        yes = bool(getattr(step, node["attr"]))
        answers.append(f"{node['key']} {'yes' if yes else 'no'}")
        if yes:
            req = node.get("requires")
            if req and not getattr(step, req):
                raise TreeError(f"{step.n} {step.name}: {node['refusal']}")
            cls = node["yes"]
            break
    bad = sorted(set(step.ops) & set(NEVER))
    if cls >= 2 and bad:
        raise TreeError(f"{step.n} {step.name}: a model step may not do {', '.join(bad)}; split the step")
    return cls, tuple(answers)


def classify(step, tree=TREE):
    return walk(step, tree)[0]


def split(steps, tree=TREE):
    out = {c: 0 for c in CLASSES}
    for s in steps:
        out[CLASSES[classify(s, tree)]] += 1
    return out


def share(steps, k=0, tree=TREE):
    """Share of steps in class k (default: deterministic)."""
    steps = list(steps)
    return sum(classify(s, tree) == k for s in steps) / len(steps)


def no_model_share(steps, tree=TREE):
    steps = list(steps)
    return sum(classify(s, tree) <= 1 for s in steps) / len(steps)


def table(steps, tree=TREE):
    rows = []
    for s in steps:
        cls, ans = walk(s, tree)
        rows.append(f"{s.n:<4} {SHORT[cls]:<8} {' / '.join(ans):<22} {s.name}")
    return "\n".join(rows)
