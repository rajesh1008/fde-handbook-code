"""The two arms of the comparison.

SmallModel is a real, trained classifier: softmax regression over a word vocabulary learned from the training set,
fitted with numpy. It stands in for fine-tuning a small open-weight model on Caldwell's clerk-labeled history; like
the real thing it learns the labels it is shown and nothing it is not shown, and words absent from training carry no
weight. Frontier is a deterministic stand-in for the pinned frontier model with prompt c06-p4 (Caldwell's type
definitions and eight examples). Its error profile is an assumption, written down below, not a measurement.
"""
import _paths  # noqa: F401
import numpy as np
from world import CLASSES, h


class SmallModel:
    def __init__(self, l2=1e-4, epochs=300, lr=20.0, seed=7):
        self.l2, self.epochs, self.lr, self.seed = l2, epochs, lr, seed

    def _x(self, docs):
        X = np.zeros((len(docs), len(self.vocab)), dtype=np.float32)
        for i, d in enumerate(docs):
            for t in d.tokens:
                j = self.vocab.get(t)
                if j is not None:
                    X[i, j] += 1.0
        X /= np.maximum(1.0, np.linalg.norm(X, axis=1, keepdims=True))
        return X

    def fit(self, docs, labels=None):
        labels = labels or [d.label for d in docs]
        self.vocab = {}
        for d in docs:
            for t in d.tokens:
                self.vocab.setdefault(t, len(self.vocab))
        X = self._x(docs)
        y = np.array([CLASSES.index(l) for l in labels])
        Y = np.eye(len(CLASSES))[y]
        rng = np.random.default_rng(self.seed)
        self.W = rng.normal(0, 0.01, (X.shape[1], len(CLASSES))).astype(np.float32)
        self.b = np.zeros(len(CLASSES), dtype=np.float32)
        for _ in range(self.epochs):
            P = self._softmax(X @ self.W + self.b)
            G = (P - Y) / len(docs)
            self.W -= self.lr * (X.T @ G + self.l2 * self.W)
            self.b -= self.lr * G.sum(0)
        self.n_train = len(docs)
        return self

    @staticmethod
    def _softmax(Z):
        Z = Z - Z.max(1, keepdims=True)
        E = np.exp(Z)
        return E / E.sum(1, keepdims=True)

    def proba(self, docs):
        return self._softmax(self._x(docs) @ self.W + self.b)

    def predict(self, docs):
        return [CLASSES[i] for i in self.proba(docs).argmax(1)]


# Frontier stand-in error profile (assumption). The prompt carries Caldwell's definitions, but two of them depend on
# Caldwell's own conventions: an agency form on Caldwell's portal template is T2 (the footer decides), and a letter
# about an existing claim is other correspondence, not a first notice. Prompted, the model follows the page's look.
FRONTIER_ERR = {"T2p": ("T1", 0.62), "corr": ("T3", 0.40), "T4s": ("T4", 0.0), "attorney": ("T3", 0.04)}
FRONTIER_BASE = {"clean": 0.045, "medium": 0.070, "hard": 0.18}
NEW_RULE = {"active": False}   # Joan Mercer's day-146 supplement ruling, one line in the prompt when active


def frontier(docs):
    out = []
    for d in docs:
        r = h("fr:" + d.id)
        if d.kind == "T4s" and NEW_RULE["active"]:
            out.append("none" if r >= 0.06 else "T4"); continue
        if d.kind in FRONTIER_ERR:
            alt, p = FRONTIER_ERR[d.kind]
            if r < p:
                out.append(alt); continue
        if r > 1 - FRONTIER_BASE[d.condition]:
            out.append(CLASSES[(CLASSES.index(d.truth) + 1 + int(h("alt:" + d.id) * 4)) % 5]); continue
        out.append(d.truth if not (d.kind == "T4s" and NEW_RULE["active"]) else "none")
    return out


def accuracy(pred, truth):
    return sum(p == t for p, t in zip(pred, truth)) / len(truth)
