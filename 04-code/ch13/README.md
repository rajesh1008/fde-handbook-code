# Chapter 13 lab: Running the Engagement (cadence, status and decisions)

Runs offline on the chapter's fixtures (cadence_data.py). No model call is made anywhere in this lab; every number in the
chapter's Output blocks and figures comes from these scripts.

| Script | What it shows | Output |
|---|---|---|
| sprint_zero.py | Caldwell sprint zero exit check (days 15 to 28): counterparts, access requests, golden paths, registers | output/sprint_zero.txt |
| backlog_order.py | Pennant sprint 2 planned two ways; displacement guard names the EU-residency control | output/backlog_order.txt |
| clinic.py | Greystone's four clinics; 11 of 12 items with an outcome, SQ-12 flagged | output/clinic.txt |
| playback.py | Caldwell day-49 playback on 200 real documents; items changed, criteria lowered (0) | output/playback.txt |
| sprint_review.py | Caldwell sprint 2 review (day 56): three outcomes, 18 of 23 points, flow measures | output/sprint_review.txt |
| decision_register.py | Caldwell decision register on day 56 with alerts and the generated status block | output/decision_register.txt |
| key_person.py | Key-person grids for Pennant and Caldwell, both sides | output/key_person.txt |
| try_it.py N | The three Try It Yourself exercises | output/try_it_N.txt |
| test_ch13.py | 9 lab tests | output/pytest.txt |

The reusable code lives in `fieldkit` v1.6 (`04-code/fieldkit/fieldkit/cadence.py`, tests in `fieldkit/tests/test_cadence.py`).

Regenerate:

    bash make_outputs.sh                                # all outputs (uses /workspace/books/.venv)
    /workspace/books/.venv/bin/python assemble.py       # rebuild 02-manuscript/ch13.md from _draft/ with real code and output
    /workspace/books/.venv/bin/python ../../05-build/tools/render_figures.py ch13   # figures 13.1 to 13.12 (run from book root)

`_draft/p1.md` to `p4.md` are the chapter source; `{{OUT:name}}`, `{{CODE:path:Symbol}}` and `{{HEAD:path:N}}`
placeholders are resolved by assemble.py so listings and outputs cannot drift from the code.
