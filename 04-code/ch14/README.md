# Chapter 14 lab: Workshop: Scoping Greystone Health in Five Days

Run from this folder with the book's virtual environment (`/workspace/books/.venv/bin/python`). Every script
prints the output quoted in the chapter; `make_outputs.sh` writes all of it to `output/`.

`fieldkit`: uses current (v0.1.0). The engagement repository and the Greystone access fixture come from
`fieldkit`; the question bank, decision tree, scoping-document lint and projection are **chapter-local
stand-ins** for modules that Chapters 6 to 9 promote into `fieldkit` [CHECK ch06-ch09]. `fieldkit` is not modified.

| Script | Listing | What it shows |
|---|---|---|
| `question_bank.py` | 14.2 | four-part questions for Michael Hart's and Sam Oakley's rooms; lint and tally |
| `rooms.py` | 14.2 (output) | the bank by room, three questions in full, what stayed open |
| `decision_tree.py`, `pipeline.py` | 14.3 | the four-class tree; the 25-step electronic path and the 25-step fax path |
| `classify_pipeline.py` | 14.3 (output) | every electronic step classified: 16 deterministic of 25 (64%) |
| `scoping_doc.py`, `scope_doc_run.py` | 14.4 | the scoping document as data, the refuse-to-sign lint, the signed v1.0 |
| `projection.py` | 14.5 | days to pilot from gate days and calendars: day 140 |
| `five_day_run.py` | 14.1 | the five-day run, days 15 to 19 (`--no-fax` for the week as planned) |
| `day_five.py` | 14.6 | failure injection: the fax path found on day 19 doubles the scope |
| `tryit.py` | Try It | exercises a, b, c |
| `test_ch14.py` | | tests |

**Deterministic stand-in.** No model is called anywhere in this lab; there are no model keys on the box and
the chapter's claims do not depend on model output. The referral volumes (412 electronic, 253 fax at two
clinics over four days) and the effort per step class are **labeled stand-ins**, not Greystone data. The
step inventory, owners, gate days and calendars are the book's canon.
