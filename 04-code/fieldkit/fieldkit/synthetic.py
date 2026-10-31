"""Representativeness of a synthetic document set against a real sample (Chapter 16, fieldkit v2.1).

Synthetic data proves the plumbing, not the accuracy. This module says, with numbers, how far a synthetic set is
from a real sample, and therefore what the synthetic results may be used for. It never looks at labels: every
feature is computed from the document and its metadata, so a sample that has not been keyed yet can be profiled.

Four tests, each with a threshold written down before the run:
  psi        population stability index per feature   (< 0.10 ok, 0.10 to 0.25 watch, > 0.25 fail)
  coverage   exception categories seen in the sample at >= 2% and absent or rare in the synthetic set
  auc        a two-sample classifier: can a simple model tell synthetic from real? (> 0.75 fail, 0.60+ watch)
  gap        accuracy on synthetic minus accuracy on real, per slice, once the real sample is scored
"""
from __future__ import annotations

import math
import random
from collections import Counter
from dataclasses import dataclass, field

PSI_WATCH, PSI_FAIL = 0.10, 0.25
AUC_WATCH, AUC_FAIL = 0.60, 0.75
COVERAGE_MIN_SHARE = 0.02
GAP_TRUST_POINTS = 5.0


def shares(values, smoothing=0.5, categories=None):
    """Category shares with additive smoothing so an absent category does not divide by zero."""
    c = Counter(values)
    cats = sorted(set(categories or []) | set(c))
    total = sum(c.values()) + smoothing * len(cats)
    return {k: (c.get(k, 0) + smoothing) / total for k in cats}


def psi(expected, actual):
    """Population stability index between two lists of categorical values (expected = real sample)."""
    cats = set(expected) | set(actual)
    e, a = shares(expected, categories=cats), shares(actual, categories=cats)
    return sum((a[k] - e[k]) * math.log(a[k] / e[k]) for k in cats)


def band(value, watch, fail):
    return "FAIL" if value > fail else ("WATCH" if value >= watch else "ok")


def coverage(synthetic_tags, sample_tags, min_share=COVERAGE_MIN_SHARE):
    """Each argument is a list of tag lists, one per document. Returns rows (tag, sample share, synthetic share, status)."""
    ns, nr = max(len(synthetic_tags), 1), max(len(sample_tags), 1)
    cs = Counter(t for tags in synthetic_tags for t in set(tags))
    cr = Counter(t for tags in sample_tags for t in set(tags))
    rows = []
    for tag in sorted(cr, key=lambda t: -cr[t]):
        rs, ss = cr[tag] / nr, cs.get(tag, 0) / ns
        if rs < min_share:
            status = "below floor"
        elif ss == 0:
            status = "MISSING"
        elif ss < rs / 4:
            status = "RARE"
        else:
            status = "ok"
        rows.append((tag, rs, ss, status))
    return rows


def _nb_fit(rows, labels):
    counts = {0: Counter(), 1: Counter()}
    prior = Counter(labels)
    for r, y in zip(rows, labels):
        for k, v in r.items():
            counts[y][(k, v)] += 1
    values = {}
    for r in rows:
        for k, v in r.items():
            values.setdefault(k, set()).add(v)
    return counts, prior, values


def _nb_score(model, r):
    counts, prior, values = model
    s = math.log((prior[1] + 1) / (prior[0] + 1))
    for k, v in r.items():
        nv = len(values.get(k, ())) + 1
        p1 = (counts[1][(k, v)] + 1) / (prior[1] + nv)
        p0 = (counts[0][(k, v)] + 1) / (prior[0] + nv)
        s += math.log(p1 / p0)
    return s


def auc(scores, labels):
    """Area under the ROC curve by rank (ties count half)."""
    pairs = sorted(zip(scores, labels))
    pos = sum(labels)
    neg = len(labels) - pos
    if not pos or not neg:
        return float("nan")
    rank_sum, i = 0.0, 0
    while i < len(pairs):
        j = i
        while j < len(pairs) and pairs[j][0] == pairs[i][0]:
            j += 1
        avg = (i + j + 1) / 2
        rank_sum += avg * sum(1 for _, y in pairs[i:j] if y)
        i = j
    return (rank_sum - pos * (pos + 1) / 2) / (pos * neg)


def classifier_auc(synthetic_rows, sample_rows, folds=5, seed=16):
    """Cross-validated AUC of a naive Bayes model asked 'is this document from the real sample?'."""
    rows = [(r, 0) for r in synthetic_rows] + [(r, 1) for r in sample_rows]
    random.Random(seed).shuffle(rows)
    scores, labels = [], []
    for f in range(folds):
        train = [x for i, x in enumerate(rows) if i % folds != f]
        test = [x for i, x in enumerate(rows) if i % folds == f]
        model = _nb_fit([r for r, _ in train], [y for _, y in train])
        scores += [_nb_score(model, r) for r, _ in test]
        labels += [y for _, y in test]
    return auc(scores, labels)


@dataclass
class RepresentativenessReport:
    """Run all label-free tests. `synthetic` and `sample` are lists of feature dicts; tags are lists of tag lists."""
    synthetic: list
    sample: list
    synthetic_tags: list
    sample_tags: list
    name: str = "synthetic set"
    psi_rows: list = field(default_factory=list)
    coverage_rows: list = field(default_factory=list)
    auc_value: float = 0.0

    def run(self):
        feats = sorted({k for r in self.sample for k in r})
        self.psi_rows = []
        for k in feats:
            v = psi([r.get(k) for r in self.sample], [r.get(k) for r in self.synthetic])
            self.psi_rows.append((k, v, band(v, PSI_WATCH, PSI_FAIL)))
        self.coverage_rows = coverage(self.synthetic_tags, self.sample_tags)
        self.auc_value = classifier_auc(self.synthetic, self.sample)
        return self

    @property
    def failures(self):
        out = [f"psi {k} {v:.2f}" for k, v, s in self.psi_rows if s == "FAIL"]
        out += [f"coverage {t} {st.lower()}" for t, _, _, st in self.coverage_rows if st in ("MISSING", "RARE")]
        if self.auc_value > AUC_FAIL:
            out.append(f"classifier auc {self.auc_value:.2f}")
        return out

    @property
    def verdict(self):
        if self.failures:
            return "NOT REPRESENTATIVE: plumbing only"
        watch = any(s == "WATCH" for _, _, s in self.psi_rows) or self.auc_value >= AUC_WATCH
        return "REPRESENTATIVE WITH WATCH ITEMS: regression use" if watch else "REPRESENTATIVE: regression use"

    def render(self):
        lines = [f"representativeness report: {self.name}",
                 f"  synthetic documents {len(self.synthetic)}   sample documents {len(self.sample)}",
                 "  feature              psi    status"]
        lines += [f"  {k:<20} {v:5.2f}  {s}" for k, v, s in self.psi_rows]
        lines.append("  exception               sample  synthetic  status")
        lines += [f"  {t:<23} {rs:5.0%}   {ss:6.0%}    {st}" for t, rs, ss, st in self.coverage_rows]
        lines.append(f"  two-sample classifier auc {self.auc_value:.2f}  ({band(self.auc_value, AUC_WATCH, AUC_FAIL)})")
        lines.append(f"  verdict: {self.verdict}")
        return "\n".join(lines)


@dataclass
class GapLine:
    """The synthetic-to-real gap as a scoreboard line, with the stop rule attached.

    slices maps a slice name to (synthetic accuracy, real accuracy, real field count). The real number is a
    development number on the sample, not a claim; claims wait for the gold set.
    """
    slices: dict
    verdict: str = ""
    trust_points: float = GAP_TRUST_POINTS
    min_fields: int = 100

    def rows(self):
        out = []
        for name, (syn, real, n) in self.slices.items():
            gap = None if syn is None else (syn - real) * 100
            if syn is None:
                use = "untested: no synthetic documents"
            elif self.verdict.startswith("NOT"):
                use = "plumbing only (report failed)"
            elif n < self.min_fields:
                use = "too few real fields to judge"
            elif abs(gap) <= self.trust_points:
                use = "regression ok"
            else:
                use = "plumbing only"
            out.append((name, syn, real, n, gap, use))
        return out

    def render(self):
        lines = ["  slice                 synthetic   real   fields   gap    synthetic results usable for"]
        for name, syn, real, n, gap, use in self.rows():
            st = "    none" if syn is None else f"{syn:8.1%}"
            gp = "    -" if gap is None else f"{gap:+5.1f}"
            lines.append(f"  {name:<21} {st}  {real:6.1%}  {n:6d}  {gp}   {use}")
        return "\n".join(lines)
