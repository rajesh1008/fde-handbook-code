"""Listing 28.1: from statements to rule cards; the register's coverage and lint."""
import _paths  # noqa: F401
from collections import Counter
from fieldkit.guardrails import elicitation_report, coverage_table
from rules import CARDS, SESSIONS, statements

st = statements()
rep = elicitation_report(st, CARDS)
cov = coverage_table(CARDS)
print("Greystone rule elicitation, days 120 to 127 (deterministic stand-in of the session record)")
print(f"sessions: {len(SESSIONS)}  minutes: {sum(s[2] for s in SESSIONS)}")
for key, day, mins, who in SESSIONS:
    print(f"  day {day}  {mins:>3} min  {key:<9} {rep['by_session'].get(key, 0):>2} statements  {who}")
print(f"statements: {rep['statements']}")
for k in ("rule", "merged", "out of scope", "contradicted"):
    print(f"  {k:<13} {rep['disposition'].get(k, 0):>3}")
print(f"rules from statements: {rep['rules_from_statements']}   rules from documents and tables: {len(CARDS) - rep['rules_from_statements']}")
print(f"dangling statements: {len(rep['dangling'])}")
print(f"rule cards: {len(CARDS)}")
print("by kind:        " + "  ".join(f"{k} {cov['kind'][k]}" for k in ("input", "output", "action", "budget")))
print("by enforcement: " + "  ".join(f"{k}/{e} {n}" for (k, e), n in sorted(cov['enforcement'].items())))
print("by source:      " + "  ".join(f"{k} {n}" for k, n in sorted(cov['source'].items(), key=lambda x: -x[1])))
print("by status:      " + "  ".join(f"{k} {n}" for k, n in sorted(cov['status'].items())))
print("by modality:    " + "  ".join(f"{k} {n}" for k, n in sorted(cov['modality'].items())))
print("by effect:      " + "  ".join(f"{k} {n}" for k, n in sorted(cov['effect'].items())))
own = Counter(c.owner for c in CARDS)
print("by owner:       " + "  ".join(f"{k} {n}" for k, n in own.most_common()))
print("VERIFY:         " + "  ".join(f"{c.rid} (review day {c.review_by})" for c in CARDS if c.status == "VERIFY"))
lint = [p for c in CARDS for p in c.lint()]
print(f"lint problems: {len(lint)}")
for s in st:
    if s.disposition.startswith("contradicted"):
        print(f"  contradicted  {s.sid} {s.said_by}: \"{s.text}\" -> {s.disposition.split(':', 1)[1]}")
