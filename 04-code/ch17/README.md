# Chapter 17 lab: identity, network and the customer's environment

**Deterministic stand-in.** Nothing here calls a cloud. `terraform/main.tf.json` is the module Caldwell's
pipeline applies (AWS, team account 111122223333, us-east-1); the scripts read it, replay the day-64
deployment against Caldwell's egress rules, and lint the environment document. Standard library plus
`fieldkit` (v2.2 adds `fieldkit/environment.py`). Terraform is not required to run the lab.

| Script | What it shows | Chapter |
|---|---|---|
| `tenancy.py` | tenancy chosen from the controls each customer requires | Listing 17.1, Figure 17.1 |
| `obo_recheck.py` | 600 replayed searches: service account (105 leaks) against delegation with recheck (0) | Listing 17.2, Figures 17.2 to 17.4 |
| `account.py` | reads the module into egress rules, keys and log stores | Section 17.3 |
| `day64_deploy.py`, `runner.py` | failure injection: image 0.9 ignores the gateway address and exports traces; Caldwell's egress log denies 144 attempts; image 0.9.1 passes | Listing 17.4, Figures 17.5, 17.6 |
| `keys.py` | secret scan (line 202 of the day-57 template) and key inventory, template against module | Listing 17.6, Figure 17.8 |
| `env_doc.py` | the three-questions document, day 57 (10 findings) and day 63 (0) | Listing 17.9, Table 17.4, Figure 17.13 |
| `greystone_review.py` | Greystone's lint and the four changes required on day 89 | Listing 17.8, Figure 17.12 |
| `tryit.py a|b|c` | Try It Yourself exercises | Try It Yourself |
| `test_ch17.py` | lab tests | Listing 17.10 |

Run `./make_outputs.sh` to regenerate `output/` and run the lab tests and the fieldkit suite.
`staging/` holds the manuscript parts and the assembly script used to build `02-manuscript/ch17.md`.
