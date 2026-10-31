"""Listing 7.9: generating the bank from discovery data. Every discovery item must be served by a question; the
day-20 draft written from memory is checked the same way. Templates produce candidates; people write the
expected answers."""
from discovery_snapshot import PATHS, EXCEPTIONS, GAPS, NOTES, ITEMS
from questionbank import coverage, Question
import caldwell_bank as cb

TEMPLATES = {
 "P": ("data", "data owner", "For documents arriving by {name}, which field records the date received, and who keys it?"),
 "X": ("functional", "operator", "When a document is '{name}', what happens next, and who decides?"),
 "G": ("identity", "security lead", "Who may '{name}', and can an agent acting for an adjuster do it?"),
 "N": ("data", "data owner", "What is true now about this: {name}?"),
}
def candidates():
    out = []
    for src in (PATHS, EXCEPTIONS, GAPS, NOTES):
        for k, v in src.items():
            cat, aud, t = TEMPLATES[k[0]]
            name = v[0] if isinstance(v, tuple) else v
            out.append(Question(f"C-{k}", cat, aud, t.format(name=name), "generated from discovery item " + k,
                                "", "decision required", "generator", (), "", 1, False, 1.5, (k,)))
    return out
MEMORY_DRAFT_SOURCES = ["P01", "P02", "P03", "N1", "N2", "N6", "X1", "X2", "X3"]  # the day-20 draft, 28 questions
cand = candidates()
print(f"discovery items: {len(ITEMS)} ({len(PATHS)} paths, {len(EXCEPTIONS)} exceptions, {len(GAPS)} permission gaps, {len(NOTES)} notes)")
print(f"day-20 draft from memory: 28 questions, serves {len(set(MEMORY_DRAFT_SOURCES))} of {len(ITEMS)} items")
print(f"  missing: {', '.join(i for i in ITEMS if i not in MEMORY_DRAFT_SOURCES)}")
print(f"generated candidates: {len(cand)}, each lint errors before editing: {len(cand[0].problems())} "
      f"({'; '.join(cand[0].problems())})")
b = cb.build()
print(f"edited bank: {len(b.questions)} questions, items not served: {len(coverage(b.questions.values(), ITEMS))}")
print(f"  data-owner set alone leaves: {', '.join(coverage(cb.DATA_OWNER, ITEMS))} (served by other roles)")
