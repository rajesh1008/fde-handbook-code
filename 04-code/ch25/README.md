# Chapter 25 lab: agents that act in the customer's systems

**Deterministic stand-in.** Every number this lab prints comes from seeded simulators in `sim.py`: a
pre-production copy of a 2009-style claims system reached through its first-notice screens (`ClaimsCore`: FNOL-1
commits a claim number at once, FNOL-2 runs rule V-118, a confirmation page can time out after the claim is
committed), first-notice documents with gold fields, seeded extraction errors, a confidence and the model's own
description, and a Greystone-style referral week. No customer data and no model call. Code runs on the box; in the
engagement the same code runs in Caldwell's pre-production account under `svc-nl-claims-wr`, calls models only through
Caldwell's gateway, and writes its action records to `/caldwell/nl-shadow/actions`, readable by the SSO group
`nl-shadow-readers`.

Run everything: `./make_outputs.sh` (writes `output/*.txt`, runs `test_ch25.py` and the fieldkit suite).

| Listing | Script | What it shows |
|---|---|---|
| 25.1 | `policy.py`, run by `boundaries.py` | Release boundaries for Caldwell and Greystone, level by level, with refusals named |
| 25.2 | `authorize_week.py` | Per-call authorization over the shadow week: what was denied and at which stage |
| 25.3 | `greystone_drafts.py` | Greystone drafts only: red flags routed, refused actions denied, no duplicate drafts |
| 25.4 | `day109_fixed.py` | The Executor: one intent key, retries owned by the executor, rejections final |
| 25.5 | `three_records.py` | Recommendation, human response and final outcome as three joined records against one |
| 25.6 | `day109_retry.py` | **Failure injection:** a key per call and a model that retries: duplicates and guessed codes |
| 25.7 | `compensate.py` | Compensation through claims-core's own VOID-DUP; touched duplicates and guesses go to people |
| 25.8 | `review_surface.py` | Review capacity model and a review screen drawn from the payload, not the description |

`tryit.py a|b|c` holds the three Try It Yourself exercises. The reusable module is
`../fieldkit/fieldkit/actions.py` (book layer v3.2; the package version stays 0.1.0), with tests in
`../fieldkit/tests/test_v32_ch25.py`.
