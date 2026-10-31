# Chapter 32 lab: the security questionnaire and the architecture review

Deterministic stand-in. Greystone Health's 41 security questions as data, each answer linked to evidence in a
register, checked for date, scope, owner and claim; the data flow inventory reconciled with observed flows; a
STRIDE-plus-agent threat model of the referral drafting agent; findings that close only with retest evidence; and
the gate stack (Signature 13) for four customers. Uses `fieldkit.security` (book layer v4).

Run `bash make_outputs.sh`. Scripts: `pack_check.py` (failure injection: a link check passes 41 of 41; the
evidence check passes 34), `triage.py`, `evidence_map.py`, `threat_model.py`, `dataflows.py`, `review.py`,
`remediation.py`, `gatestack.py`, `tryit.py a|b|c`.

On site this runs on the FDE's laptop or in the customer's build agent against the questionnaire export (CSV from
the customer's GRC tool) and an evidence register kept in the engagement repository. Nothing here needs network
access or customer data.

`answer_cards.py` (Section 32.8, Listing 32.14): three answers (SQ-09, SQ-26, SQ-30) as cards with claim type,
evidence, owner, expiry and falsifier; v1 as sent on day 100 against the finding each drew, v2 checked on pilot
day 131. Lab test `test_answer_cards_v2_pass_on_pilot_day`. `make_outputs.sh` runs lab plus fieldkit tests
(214 passing) before writing any output.

Listing map: 32.1 triage, 32.2 pack_check, 32.3 evidence_map, 32.4 review, 32.6 threat_model, 32.8 dataflows,
32.10 remediation, 32.12 gatestack, 32.14 answer_cards; 32.5, 32.7, 32.9, 32.11, 32.13 and 32.15 quote
`fieldkit/fieldkit/security.py`. Try It Yourself: `tryit.py a|b|c` (outputs in `output/tryit_*.txt`).
