"""Failure injection: the fine-tuned model wins on its test split and on Anne's set, and fails on a class it never saw."""
import _paths  # noqa: F401
from collections import Counter
import lab
import models as M
from world import h

S = lab.sets()
m = lab.ft1()
print("c06 document type: c06-ft1 (fine-tuned small model) vs c06-p4 (prompted frontier), deterministic stand-in")
print(f"training: history-6000 split 80/20 -> {len(S['train'])} train, {len(S['test'])} test; vocabulary {len(m.vocab)}")
sig = lambda d: h(" ".join(sorted(d.tokens)))
dupes = len({sig(d) for d in S["train"]} & {sig(d) for d in S["anne"]})
print(f"dedupe check, training vs Anne's set (exact token multiset): {dupes} overlaps")
print()
print(f"{'evaluation set':<34}{'n':>5}   {'c06-ft1':>12}   {'c06-p4':>12}")
rows = [("history test split (clerk labels)", S["test"], "label"), ("Anne's set (adjuster labels)", S["anne"], "truth"),
        ("legal-60 misfile slice", S["legal"], "truth")]
for name, docs, attr in rows:
    a, b = lab.n_right(m.predict(docs), docs, attr), lab.n_right(M.frontier(docs), docs, attr)
    print(f"{name:<34}{len(docs):>5}   {lab.pct(a, len(docs))}   {lab.pct(b, len(docs))}")
print()
for name, docs in (("Anne's set", S["anne"]), ("legal-60", S["legal"])):
    att = [d for d in docs if d.kind == "attorney"]
    print(f"attorney letters in {name}: {len(att)}; c06-ft1 answers {dict(Counter(m.predict(att)))};"
          f" c06-p4 answers {dict(Counter(M.frontier(att)))}")
print()
print("FAILURE: c06-ft1 wins on the test split and on Anne's set, and files attorney letters as first-notice")
print("letters (T3). History-6000 holds no attorney letters: they go to legal, never through intake clerks.")
print("A model answers only with classes it was shown, so the test split could not reveal this.")
