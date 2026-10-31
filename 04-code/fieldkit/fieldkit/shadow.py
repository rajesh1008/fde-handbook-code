"""Shadowing: watching real data without storing it (Chapter 16, fieldkit v2.1).

A ShadowTap sees each real document as it passes, runs the pipeline on it, compares the answer with what the
adjuster keyed, and keeps only three things: a keyed hash of the document id (so a disputed case can be found again
inside the customer's system), per-field agreement, and label-free profile features. No text, no field values.

The claim "we do not store it" is tested, not asserted: canary documents carrying unique made-up tokens are fed
through the tap, then every store the tap can write to (logs, metrics, caches, traces) is scanned for the tokens.
One hit anywhere fails the run.
"""
from __future__ import annotations

import hashlib
import hmac
import json
import os
import random
import string
from dataclasses import dataclass, field


def keyed_id(doc_id, secret):
    return hmac.new(secret.encode(), doc_id.encode(), hashlib.sha256).hexdigest()[:16]


def make_canary(rng=None, prefix="Zelphine"):
    """A canary document's identifiers: a surname and policy number that cannot occur in real data."""
    rng = rng or random.Random()
    tail = "".join(rng.choice(string.ascii_lowercase) for _ in range(5))
    return {"claimant_name": f"{prefix} Quorvant{tail}", "policy_number": f"HP9{rng.randint(10000, 99999)}Q",
            "token": f"CANARY-{rng.randint(100000, 999999)}"}


@dataclass
class ShadowTap:
    secret: str
    store_dir: str
    debug_log: bool = False          # the failure injection: a well-meant debug line that writes raw text
    rows: list = field(default_factory=list)

    def __post_init__(self):
        os.makedirs(self.store_dir, exist_ok=True)

    def observe(self, doc_id, text, predicted, keyed, features):
        agree = {f: (str(predicted.get(f)).lower() == str(keyed.get(f)).lower()) for f in keyed}
        row = {"doc": keyed_id(doc_id, self.secret), "agree": agree, "features": features}
        self.rows.append(row)
        with open(os.path.join(self.store_dir, "agreement.jsonl"), "a") as fh:
            fh.write(json.dumps(row) + "\n")
        if self.debug_log:
            with open(os.path.join(self.store_dir, "debug.log"), "a") as fh:
                fh.write(f"doc={doc_id} predicted={json.dumps(predicted)} text={text[:200]!r}\n")
        return row

    def agreement(self):
        fields = sorted({f for r in self.rows for f in r["agree"]})
        return {f: sum(r["agree"][f] for r in self.rows) / len(self.rows) for f in fields} if self.rows else {}


def scan_stores(store_dir, tokens):
    """Every file under store_dir, every token: (file, token) for each hit. Case-insensitive."""
    hits = []
    for root, _dirs, files in os.walk(store_dir):
        for name in files:
            path = os.path.join(root, name)
            try:
                data = open(path, encoding="utf-8", errors="ignore").read().lower()
            except OSError:
                continue
            for t in tokens:
                if t and t.lower() in data:
                    hits.append((os.path.relpath(path, store_dir), t))
    return hits
