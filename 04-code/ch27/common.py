"""Shared setup for the Chapter 27 lab: the sets, router v0, the correctness model, the signed thresholds and routing."""
import json
import os
from functools import lru_cache

import _paths  # noqa: F401
import world as W
from fieldkit.routing import (Isotonic, CorrectnessModel, Evidence, choose_proceed, set_thresholds, route_field,
                              route_document)

GRID = [x / 1000 for x in range(500, 1000, 5)]
MAX_BLANK = 4          # Anne Kessler's setting: more than four fields below the floor and the document is keyed whole
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output")


def acc(items):
    return sum(i.right for i in items) / max(1, len(items))


def rel(scores, outcomes, bins=10):
    b = [[] for _ in range(bins)]
    for s, o in zip(scores, outcomes):
        b[min(bins - 1, int(s * bins))].append((s, o))
    return [dict(lo=k / bins, n=len(x), score=sum(s for s, _ in x) / len(x), right=sum(o for _, o in x) / len(x))
            for k, x in enumerate(b) if x]


def dump(name, obj):
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, name + ".json"), "w") as f:
        json.dump(obj, f, indent=1)


@lru_cache(None)
def synthetic():
    return W.make("synthetic-2000", 2000, synthetic=True)


@lru_cache(None)
def v0():
    """Router v0, day 120: the model's own stated confidence, calibrated on Northlight's synthetic set."""
    syn = synthetic()
    iso = Isotonic().fit([i.verbal for i in syn], [i.right for i in syn])
    t, lb, n = choose_proceed([iso.predict(i.verbal) for i in syn], [i.right for i in syn], 0.98, 200, grid=GRID)
    return iso, t, lb, n


@lru_cache(None)
def gold():
    return W.make("gold-heldout", 201, stratified=True)


@lru_cache(None)
def cal():
    items = W.make("cal-600", 600)
    fit = [i for i in items if int(i.doc[-4:]) % 2 == 0]
    chk = [i for i in items if int(i.doc[-4:]) % 2 == 1]
    return items, fit, chk


@lru_cache(None)
def model():
    _, fit, _ = cal()
    return CorrectnessModel(lambda it: it.features(), names=W.FEATURE_NAMES).fit(fit, [i.right for i in fit])


@lru_cache(None)
def thresholds(target=0.98):
    m = model()
    _, fit, chk = cal()
    return set_thresholds([m.score(i) for i in fit], [i.right for i in fit], [m.score(i) for i in chk],
                          [i.right for i in chk], target=target)


NO_GATE = Evidence(True, None, None, True)


def route(items, m=None, th=None, gates=True, max_blank=MAX_BLANK):
    """Route every document; return one dict per document with the field routes and final outcomes."""
    m, th = m or model(), th or thresholds()
    out = []
    for d, its in W.docs(items).items():
        rs = [route_field(m.score(i), i.ev if gates else NO_GATE, th) for i in its]
        band, why = route_document(rs, [i.field for i in its], W.CRITICAL, max_blank=max_blank)
        fields = []
        for i, r in zip(its, rs):
            fb = "escalate" if band == "escalate" else ("review" if r.band == "escalate" else r.band)
            shown = band != "escalate" and r.show_recommendation
            fields.append(dict(item=i, route=r, band=fb, shown=shown, final=W.review_outcome(i, fb, shown)))
        out.append(dict(doc=d, stratum=its[0].stratum, band=band, reason=why, fields=fields))
    return out
