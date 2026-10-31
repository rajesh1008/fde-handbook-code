# Chapter 19 lab: systems with no API

**Deterministic stand-in.** Every number this lab prints comes from seeded simulators in `sim.py`: a 2009-style
claims system reached only through two first-notice screens (`ClaimsCore`), a 200-document sample shaped like
Caldwell's `claims-sample-200`, thirty nights of a Pennant-style TMS export and one day of X12 214 carrier status
messages. No customer data, no model call. The extraction step is a stand-in that returns the sample's gold
fields, with a cause-of-loss code missing exactly where the source document does not state one.

Run everything: `./make_outputs.sh` (writes `output/*.txt`, runs `test_ch19.py` and the fieldkit suite).

| Listing | Script | What it shows |
|---|---|---|
| 19.1 | `inventory.py` | Surface inventory for Caldwell, Greystone and Pennant, scored, with open facts |
| 19.2 | `file_drop.py` | Thirty nights of the TMS export: duplicate, schema drift, truncation, a missing file |
| 19.3 | `mail_queue.py` | The intake mailbox as a queue: redeliveries and forwards, two dedupe keys |
| 19.4 | `screen_reliability.py` | Compounding per-step reliability; a vendor patch against a positional script |
| 19.5 | `writeback_failure.py` | **Failure injection:** write-back passes in UAT, rejected by production rules |
| 19.6 | `writeback_fixed.py` | Outbox, idempotency key, preflight, read-back, compensation, retry of unknowns |
| 19.7 | `reconcile_caldwell.py` | Caldwell intake end to end on the sample, reconciled against the system's extract |
| 19.8 | `pennant_edi.py` | X12 214 envelope checks, intraday status, reconciliation with the 02:00 export |

`tryit.py a|b|c` holds the three Try It Yourself exercises. The reusable module is
`../fieldkit/fieldkit/connectors.py` (book layer v2.4; the package version stays 0.1.0), with tests in
`../fieldkit/tests/test_v24_ch19.py`. `staging/` keeps the copy the chapter was written against.
