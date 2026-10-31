# Chapter 40 lab: the evidence pack

Deterministic, labeled stand-in. No model calls, no network, no real claims. Every claim, adjuster ID, address and
police report number below is invented for the book.

## What it does

Generates the evidence pack for any decision the Caldwell intake agent made, and rehearses reconstruction of past
decisions. The pack has eight elements, in the order an auditor walks them: document, lineage, retrieval, prompt and
model, confidence and route, decision, review, action. Each element gets a status: verified, reconstructed, inferred,
contradicted, unverifiable or n/a. A pack is reconstructable when every element is verified, reconstructed or n/a.

## Failure injection

v0 run records (days 158 to 179) named the prompt by name and code commit `c7e41a2`. On day 166 at 02:10 a Northlight
on-call engineer hot-fixed the `loss_location` rule in the parameter store (text A, 72 tokens, to text B, 107 tokens).
The commit still held text A, so every v0 record from then on implied a prompt that was never sent. Gateway traces
caught the mismatch through input tokens, but traces are kept 30 days. Day 180: v1 records pin the prompt by content
hash at send time (`intake-summary@<hash>`), the gateway checks the hash, and the console write is removed. Day 181:
backfill from the parameter-store history, marked `reconstructed`.

## Run

    ./make_outputs.sh          # regenerates output/*.txt and runs the fieldkit suite plus 4 lab tests

| Script | Output | What it shows |
|---|---|---|
| rehearse.py v0 / history / months / v1 | rehearse_*.txt | 40-decision reconstruction rehearsal under each rule set |
| dispute.py | dispute.txt | v0 pack and rebuilt pack for disputed claim CW-26-1690013 |
| rerun.py | rerun.txt | prompt text actually sent per day, token gap, rerun agreement |
| monitor.py | monitor.txt | P1 completeness before and after backfill; monitor list M1 to M6, P1 to P3 |
| conventions.py | conventions.txt | one model, four customer homes |
| review.py | review.txt | the day-184 architects' review, Q1 to Q12 |
| audit.py | audit.txt | internal audit sample of 26 packs |
| tryit.py a / b / c | tryit_*.txt | Try It Yourself exercises |

fieldkit: uses current (`fieldkit.lineage`); no fieldkit change in this chapter. Package stays 0.1.0.
