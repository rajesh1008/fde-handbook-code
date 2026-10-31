# Chapter 18 lab: the customer's model gateway

**Deterministic stand-in.** Everything here runs against `gateway_sim.py`, a simulated customer gateway with
weekly key rotation (Sunday 02:00, one-hour grace), Deprecation and Sunset headers, an IP allowlist, a quota,
a content filter, an alias that moves to a new model version, and a default API version. No real model,
no real key, no network. Engagement day 0 is a Thursday, so day 73 is a Sunday, as in the chapter.
Standard library plus `fieldkit` (v2.3 adds `fieldkit/gateway.py`). Prices are stand-in chargeback rates.

| Script | What it shows | Chapter |
|---|---|---|
| `sunday_rotation.py` | failure injection: the Sunday rotation takes the naive shadow runner down; the fieldkit adapter survives | Listing 18.1, 18.2, Figure 18.4 |
| `deprecation.py` | Deprecation and Sunset headers as a register with days left | Listing 18.3, Figure 18.6 |
| `version_drift.py` | the alias moves on day 77; item-level flips under a better aggregate | Listing 18.4, Figure 18.7 |
| `framework_header.py` | the error that only happened without the framework; a header contract test | Listing 18.5 |
| `allowlist.py` | a new runner address: retries trip a security alert, a stop does not | Listing 18.6 |
| `greystone_capability.py` | live catalog against documentation; lexical retrieval measured on a stand-in set | Listing 18.7, Figure 18.10 |
| `tryit.py a|b|c` | Try It Yourself exercises | Try It Yourself |

Run `./make_outputs.sh` to regenerate `output/` and run the tests.
