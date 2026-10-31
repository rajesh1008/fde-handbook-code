"""Shared pieces for the Chapter 30 lab: the evaluation sets, the trained c06-ft1 and the absent-class guard."""
import _paths  # noqa: F401
import functools
import world as W
import models as M
from fieldkit.finetune import AbsentClassGuard, GuardRule

THRESHOLD = 0.95   # familiarity below this is held (chosen on the test split and history, never on Anne's set)


@functools.lru_cache(maxsize=None)
def sets():
    tr, te = W.split(W.history())
    return {"train": tr, "test": te, "anne": W.anne(), "legal": W.legal60()}


@functools.lru_cache(maxsize=None)
def ft1():
    return M.SmallModel().fit(sets()["train"])


def guard(model, threshold=THRESHOLD):
    registry = GuardRule("legal registry", lambda toks: any(t in W.REGISTRY for t in toks),
                         "legal mail coordinator", "legal mail coordinator")
    return AbsentClassGuard(set(model.vocab), threshold, [registry])


def guarded(model, docs, threshold=THRESHOLD):
    g = guard(model, threshold)
    out = []
    for d, p in zip(docs, model.predict(docs)):
        hold = g.check(d.tokens)
        out.append("hold:" + hold.route if hold else p)
    return out


def right(p, t):
    """A held document is right only if it is truly out of scope; a held in-scope document counts as wrong."""
    return p == t or (p.startswith("hold") and t == "none")


def n_right(pred, docs, attr="truth"):
    return sum(right(p, getattr(d, attr)) for p, d in zip(pred, docs))


def pct(k, n):
    return f"{k:>5} {100 * k / n:5.1f}%"
