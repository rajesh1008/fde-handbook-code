# Chapter 7 lab: the discovery question bank

Everything here runs on a laptop with Python 3.10+ and no network. **All records are synthetic** (seeded stand-ins
shaped by the answers in the chapter); there is no Caldwell data in this folder.

| File | What it shows | Listing |
|---|---|---|
| `questionbank.py` | shim: imports `fieldkit.questionbank` (v1.1), falls back to `questionbank_impl.py` | - |
| `discovery_snapshot.py` | frozen Chapter 6 discovery items (11 paths, 7 exceptions, 4 permission gaps, 9 notes) | - |
| `caldwell_bank.py` | 66 four-part questions for four roles; Ruth Calloway's 40 answers from day 24 | - |
| `failure_vendor_assumption.py` | failure injection: design v0 built on expected answers, six of them vendor positions | 7.2 |
| `prep_sheet.py [audience] [minutes]` | lint plus a time-boxed prep sheet | 7.3 |
| `day24_session.py` | reconcile answers: outcomes, design changes, follow-ups | 7.6 |
| `data_questions.py` | what grain, freshness and late-arriving answers change, measured | 7.4 |
| `whitfield.py` | acting-for permission gaps for Tom Whitfield | 7.7 |
| `rapid_fire.py` | the sixty-second round | 7.5 |
| `roles.py` | one bank, four audiences | 7.8 |
| `generate_bank.py` | coverage of discovery items, memory draft against generated bank | 7.9 |
| `tryit.py a|b|c` | the three Try It Yourself exercises | - |

Run `./make_outputs.sh` to regenerate `output/` and the tests.
