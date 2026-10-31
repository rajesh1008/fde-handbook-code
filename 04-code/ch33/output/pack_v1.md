# Model-risk pack v1, Caldwell Mutual claims intake

## C06: registered, not validated
- purpose: system card: what each component decides, what it never decides (Ch8 scope) (measured by Callum Reid, on signed scope v3; engagement repo, system-card.md)
- vendor_due_diligence: provider system card, model pin, deprecation notice period, incident notice clause (measured by Priya Natarajan, on provider contract schedule 4; procurement record)
- design_review: deterministic first, model last: 9 of 12 steps without a model; prompts and retrieval under the prompt registry (measured by Callum Reid, on Ch9 classification, Ch23 retrieval design; Ch9, Ch23)
- outcomes: c06-p4 88.4% correct (measured by Anne Kessler's labelers, on Anne's set, 900 documents; 04-code/ch30/output/compare.txt)
- sensitivity: accuracy by field under fax noise, rotation and handwriting (measured by Sofia Brennan, on 201 gold-heldout documents; 04-code/ch33/output/evidence.txt)
- stability: repeat-run agreement by field, 20 runs at fixed settings (measured by Sofia Brennan, on 201 gold-heldout documents; 04-code/ch33/output/evidence.txt)
- limits: limits register: conditions where a field's accuracy falls more than 10 points (measured by Sofia Brennan, on 201 gold-heldout documents, four conditions; 04-code/ch33/output/evidence.txt)
- monitoring: monitoring plan M1 to M6 with thresholds and owners (measured by Callum Reid, on pack; pack.md)
- change_control: pins resolved per estate; a version change is a recorded model change; merge gate with no override flag (measured by Priya Natarajan, on gateway version ledger; Ch18, Ch20, Ch29)

## C07: registered, not validated
- purpose: system card: what each component decides, what it never decides (Ch8 scope) (measured by Callum Reid, on signed scope v3; engagement repo, system-card.md)
- vendor_due_diligence: provider system card, model pin, deprecation notice period, incident notice clause (measured by Priya Natarajan, on provider contract schedule 4; procurement record)
- design_review: deterministic first, model last: 9 of 12 steps without a model; prompts and retrieval under the prompt registry (measured by Callum Reid, on Ch9 classification, Ch23 retrieval design; Ch9, Ch23)
- outcomes: loss-cause code agreement with the clerk-coded history (measured by Anne Kessler's labelers, on gold-heldout loss_type field; 04-code/ch26/output)
- sensitivity: accuracy by field under fax noise, rotation and handwriting (measured by Sofia Brennan, on 201 gold-heldout documents; 04-code/ch33/output/evidence.txt)
- stability: repeat-run agreement by field, 20 runs at fixed settings (measured by Sofia Brennan, on 201 gold-heldout documents; 04-code/ch33/output/evidence.txt)
- limits: limits register: conditions where a field's accuracy falls more than 10 points (measured by Sofia Brennan, on 201 gold-heldout documents, four conditions; 04-code/ch33/output/evidence.txt)
- monitoring: monitoring plan M1 to M6 with thresholds and owners (measured by Callum Reid, on pack; pack.md)
- change_control: pins resolved per estate; a version change is a recorded model change; merge gate with no override flag (measured by Priya Natarajan, on gateway version ledger; Ch18, Ch20, Ch29)

## C11: registered, not validated
- purpose: system card: what each component decides, what it never decides (Ch8 scope) (measured by Callum Reid, on signed scope v3; engagement repo, system-card.md)
- vendor_due_diligence: provider system card, model pin, deprecation notice period, incident notice clause (measured by Priya Natarajan, on provider contract schedule 4; procurement record)
- design_review: deterministic first, model last: 9 of 12 steps without a model; prompts and retrieval under the prompt registry (measured by Callum Reid, on Ch9 classification, Ch23 retrieval design; Ch9, Ch23)
- outcomes: citation audit: every statement cited, citations checked (measured by Tom Whitfield, on 60 summaries, day 146; 04-code/ch33/output/review.txt)
- sensitivity: accuracy by field under fax noise, rotation and handwriting (measured by Sofia Brennan, on 201 gold-heldout documents; 04-code/ch33/output/evidence.txt)
- stability: repeat-run agreement by field, 20 runs at fixed settings (measured by Sofia Brennan, on 201 gold-heldout documents; 04-code/ch33/output/evidence.txt)
- limits: limits register: conditions where a field's accuracy falls more than 10 points (measured by Sofia Brennan, on 201 gold-heldout documents, four conditions; 04-code/ch33/output/evidence.txt)
- monitoring: monitoring plan M1 to M6 with thresholds and owners (measured by Callum Reid, on pack; pack.md)
- change_control: pins resolved per estate; a version change is a recorded model change; merge gate with no override flag (measured by Priya Natarajan, on gateway version ledger; Ch18, Ch20, Ch29)

## EX: registered, not validated
- purpose: system card: what each component decides, what it never decides (Ch8 scope) (measured by Callum Reid, on signed scope v3; engagement repo, system-card.md)
- vendor_due_diligence: provider system card, model pin, deprecation notice period, incident notice clause (measured by Priya Natarajan, on provider contract schedule 4; procurement record)
- design_review: deterministic first, model last: 9 of 12 steps without a model; prompts and retrieval under the prompt registry (measured by Callum Reid, on Ch9 classification, Ch23 retrieval design; Ch9, Ch23)
- outcomes: 76.7% of fields correct for p7, corrected by judge_v2 (TPR 0.97, TNR 0.88) (measured by Anne Kessler, on 201 gold-heldout documents; 04-code/ch26/output)
- sensitivity: accuracy by field under fax noise, rotation and handwriting (measured by Sofia Brennan, on 201 gold-heldout documents; 04-code/ch33/output/evidence.txt)
- stability: repeat-run agreement by field, 20 runs at fixed settings (measured by Sofia Brennan, on 201 gold-heldout documents; 04-code/ch33/output/evidence.txt)
- limits: limits register: conditions where a field's accuracy falls more than 10 points (measured by Sofia Brennan, on 201 gold-heldout documents, four conditions; 04-code/ch33/output/evidence.txt)
- monitoring: monitoring plan M1 to M6 with thresholds and owners (measured by Callum Reid, on pack; pack.md)
- change_control: pins resolved per estate; a version change is a recorded model change; merge gate with no override flag (measured by Priya Natarajan, on gateway version ledger; Ch18, Ch20, Ch29)

## EM: registered as a tool
- purpose: system card: what each component decides, what it never decides (Ch8 scope) (measured by Callum Reid, on signed scope v3; engagement repo, system-card.md)
- validity_check: question-set recall at 10 by category; ACL drift check (measured by Joan Mercer, on claims-manual question set; Ch23)
- change_control: pins resolved per estate; a version change is a recorded model change; merge gate with no override flag (measured by Priya Natarajan, on gateway version ledger; Ch18, Ch20, Ch29)

## JG: registered as a tool
- purpose: system card: what each component decides, what it never decides (Ch8 scope) (measured by Callum Reid, on signed scope v3; engagement repo, system-card.md)
- validity_check: judge_v2 TPR 0.97, TNR 0.88 against Anne's labels; weekly 20-document check (measured by Anne Kessler, on 201 gold-heldout documents; 04-code/ch26/output)
- change_control: pins resolved per estate; a version change is a recorded model change; merge gate with no override flag (measured by Priya Natarajan, on gateway version ledger; Ch18, Ch20, Ch29)

## RT: full scope
- purpose: system card: what each component decides, what it never decides (Ch8 scope) (measured by Callum Reid, on signed scope v3; engagement repo, system-card.md)
- conceptual_soundness: isotonic correctness model; reliability, ECE and resolution reported (measured by Callum Reid, on cal-600 odd documents; 04-code/ch27/output/calibrate.txt)
- development_data: cal-600 scored by Tom Whitfield and adjuster B, ties by Anne Kessler; 100 broker documents day 150 (measured by Tom Whitfield, on 600 + 100 shadow documents; 04-code/ch27/output/thresholds.txt)
- outcomes: post-review error 0.9% (36 of 4,000 fields) (measured by Anne Kessler, on audit-400; 04-code/ch27/output/audit.txt)
- benchmark: v1.1 against v1: lower bound 98.8% on 2,656 proceed fields (measured by Anne Kessler, on cal-600 odd; 04-code/ch27/output/drift.txt)
- sensitivity: accuracy by field under fax noise, rotation and handwriting (measured by Sofia Brennan, on 201 gold-heldout documents; 04-code/ch33/output/evidence.txt)
- stability: repeat-run agreement by field, 20 runs at fixed settings (measured by Sofia Brennan, on 201 gold-heldout documents; 04-code/ch33/output/evidence.txt)
- limits: limits register: conditions where a field's accuracy falls more than 10 points (measured by Sofia Brennan, on 201 gold-heldout documents, four conditions; 04-code/ch33/output/evidence.txt)
- monitoring: monitoring plan M1 to M6 with thresholds and owners (measured by Callum Reid, on pack; pack.md)
- change_control: pins resolved per estate; a version change is a recorded model change; merge gate with no override flag (measured by Priya Natarajan, on gateway version ledger; Ch18, Ch20, Ch29)

## C06-ft1: full scope
- purpose: system card: what each component decides, what it never decides (Ch8 scope) (measured by Callum Reid, on signed scope v3; engagement repo, system-card.md)
- conceptual_soundness: fine-tune on one closed-set task with an absent-class guard (measured by Callum Reid, on Ch30 design note; 04-code/ch30/output)
- development_data: history-6000 under the training-data record signed day 138 (measured by Ruth Calloway, on 6,000 clerk-coded documents; 04-code/ch30/output)
- outcomes: c06-ft1 with guard 93.1% correct (measured by Anne Kessler's labelers, on Anne's set, 900 documents; 04-code/ch30/output/compare.txt)
- benchmark: paired against c06-p4 on the same 900 documents (measured by Anne Kessler's labelers, on Anne's set; 04-code/ch30/output/compare.txt)
- sensitivity: accuracy by field under fax noise, rotation and handwriting (measured by Sofia Brennan, on 201 gold-heldout documents; 04-code/ch33/output/evidence.txt)
- stability: repeat-run agreement by field, 20 runs at fixed settings (measured by Sofia Brennan, on 201 gold-heldout documents; 04-code/ch33/output/evidence.txt)
- limits: limits register: conditions where a field's accuracy falls more than 10 points (measured by Sofia Brennan, on 201 gold-heldout documents, four conditions; 04-code/ch33/output/evidence.txt)
- monitoring: monitoring plan M1 to M6 with thresholds and owners (measured by Callum Reid, on pack; pack.md)
- change_control: pins resolved per estate; a version change is a recorded model change; merge gate with no override flag (measured by Priya Natarajan, on gateway version ledger; Ch18, Ch20, Ch29)

## Monitoring
- M1 proceed-band error, weekly audit sample; threshold Wilson lower bound at most 2%; read by Anne Kessler; covers RT, EX
- M2 router score drift (PSI); threshold PSI at most 0.10; read by Anne Kessler; covers RT
- M3 field and type accuracy on the 30-day refresh sample; threshold at or above the gate line; read by Anne Kessler; covers EX, C06, C06-ft1, C07
- M4 summary and field quality against the reference suite; threshold at most 2 points below the shadow baseline; read by Anne Kessler; covers C11, EX
- M5 pin age and provider deprecation dates; threshold re-review 30 days before any pin expires; read by Priya Natarajan; covers EX, C06, C07, C11, EM, JG
- M6 judge validity, 20 documents a week; threshold more than three false passes marks the judge suspect; read by Anne Kessler; covers JG
