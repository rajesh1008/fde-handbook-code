"""Section 27.6: the 'not in the documents' gate promised in Chapter 23, run on Anne Kessler's 150 questions.
Retrieval is Chapter 23's index (day 88); the drafted answer is a stand-in that quotes the best-matching sentence
of each of the top three passages. The gate is fieldkit.routing.AnswerCheck."""
import os
import re
import sys

import common as C  # noqa: F401
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "ch23"))
import caldwell_docs as D  # noqa: E402
from fieldkit.retrieval import tokens  # noqa: E402
from fieldkit.routing import AnswerCheck  # noqa: E402

ix, recs, acl, versions = D.build(day=88)
D.apply_register(ix, D.lifecycle_register(versions))
qs = D.questions(recs)
STOP = {"what", "does", "manual", "about", "form", "current", "rule", "with", "from", "that", "this", "when",
        "have", "need", "before", "after", "there", "which", "under", "into", "your", "their", "will", "should"}
# Caldwell's adjuster glossary: each adjuster phrasing in Anne's set mapped to the manual's term, so a question asked
# in slang is checked against the words the manual uses. An unknown word stays unknown and counts against coverage.
GLOSS = {}
for man, sl in D.DET + D.TOP:
    for w in tokens(sl):
        if w not in STOP and len(w) >= 4 and w not in tokens(man):
            GLOSS.setdefault(w, max(tokens(man), key=len))
bm = lambda q: max(ix._bm25(q.text, ix.passages).values(), default=0.0)
K = 5
LINE = 7.7          # Chapter 23: the answerable 5th percentile of the top lexical score
chk = AnswerCheck()


def draft(q):
    hits = ix.search(q.text, D.who_for(q), k=K)
    qt = set(tokens(q.text))
    quotes = []
    for p, _ in hits:
        sents = [s.strip() for s in re.split(r"(?<=[.;])\s+", p.text) if s.strip()]
        best = max(sents, key=lambda s: len(qt & set(tokens(s))))
        if len(qt & set(tokens(best))) >= 2:
            quotes.append(best)
    terms = list(dict.fromkeys(GLOSS.get(t, t) for t in tokens(q.text) if len(t) >= 4 and t not in STOP))
    return quotes, [p.text for p, _ in hits], terms


res = {}
cov = {}
for q in qs:
    quotes, passages, terms = draft(q)
    band, why = chk.route(quotes, passages, terms)
    band = {"escalate": "declined"}.get(band, band)
    if band == "proceed" and bm(q) < LINE:
        band = "review"          # the retrieval score routes after the gate; it is not the gate
    res[q.id if hasattr(q, "id") else q.qid] = (bool(q.gold), band)
    cov[q.id if hasattr(q, "id") else q.qid] = (bool(q.gold), chk.coverage(quotes, passages, terms) if quotes else 0.0)
ans = [b for g, b in res.values() if g]
na = [b for g, b in res.values() if not g]
score_only = sum(1 for q in qs if not q.gold and bm(q) < LINE)
print(f"Anne Kessler's set: {len(qs)} questions, {len(ans)} answerable, {len(na)} not in the documents")
print()
print(f"score threshold alone (Chapter 23, top lexical score below {LINE}): {score_only} of {len(na)} caught")
print(f"evidence gate (every quote verbatim in a retrieved, permitted, in-force passage; key terms covered: "
      f"decline below {chk.min_coverage:.0%}, review below {chk.review_below:.0%}):")
for label, xs in (("not in the documents", na), ("answerable", ans)):
    print(f"  {label:22s} declined {xs.count('declined'):3d}  review {xs.count('review'):3d}  proceed {xs.count('proceed'):3d}")
print()
print("where to put the decline line (coverage of key terms by the quoted passages):")
print(f"{'line':>5s} {'not-in-docs let through':>23s} {'answerable declined':>19s}")
sweep = []
for line in (0.4, 0.5, 0.6, 0.7, 0.8):
    a1 = sum(1 for g, c in cov.values() if not g and c >= line); a2 = sum(1 for g, c in cov.values() if g and c < line)
    sweep.append(dict(line=line, through=a1, declined=a2))
    print(f"{line:5.1f} {a1:23d} {a2:19d}")
print()
print(f"false declines: {ans.count('declined')} of {len(ans)} answerable questions go to a person with "
      f"'not in the documents'; none of the {len(na)} reaches proceed" if na.count("proceed") == 0 else "")
C.dump("notindocs", dict(sweep=sweep, score_only=score_only, na={b: na.count(b) for b in ("declined", "review", "proceed")},
                         ans={b: ans.count(b) for b in ("declined", "review", "proceed")}, n_na=len(na), n_ans=len(ans)))
