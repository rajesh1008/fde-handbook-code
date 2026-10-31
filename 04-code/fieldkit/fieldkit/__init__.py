"""fieldkit: the forward deployed engineer's toolkit that grows chapter by chapter.

v0.1 (Stage 0): access tracker, data-readiness register, four customer fixtures.
Book layer v0 (Chapter 3): engagement repository (notes, decisions, requests, evidence, generated status).
Book layer v1 (Chapter 6): discovery notes as data (Note with an identifier validator, DiscoveryLog, CoverageReport,
contradictions resolved by a named person, permission gaps).
Chapter 4 (uses current): deployment-readiness checklist (25 proofs, five dimensions, gated scoring).
Book layer v1.6 (Chapter 13): cadence (P0-P3 ordering with a displacement guard, Ready/Done/Accepted, sprint review
  with an exception list, decision register with staleness alerts, status lint: acceptance is not approval).
Chapter 15 (fieldkit v2, uses current): escalation with dates, field-level data-readiness register
(meaning, entitlement, freshness, owner), access histories replayable to any day, rung dates, RUNG_WORK.
Chapter 16 (v2.1, uses current): representativeness report (PSI, exception coverage, two-sample classifier, gap line
with the stop rule), de-identification tested by attack (known-value scan, k-anonymity, linkage), shadow tap with
canary scan, stratified sampling with a signed manifest. Modules: synthetic, deid, shadow, sampling.
Chapter 9 (module version 1.3): autonomy, the autonomy decision tree (Signature 3) as data. Module: autonomy.
Chapter 17 (v2.2, book layer; package stays 0.1.0): environment (tenancy, on-behalf-of delegation with rights recheck,
default-deny egress, secrets/key ownership, customer-owned hash-chained audit log, three-questions doc lint). Module: environment.
Chapter 18 (v2.3): gateway adapter, key rotation, deprecation register, version ledger. Module: gateway.
Chapter 19 (v2.4, book layer; package stays 0.1.0): connectors for systems with no API (surface inventory, file drop
with drift and volume guards, mail queue with two dedupe keys, fingerprinted screens, write-back outbox with
preflight, read-back and compensation, reconciliation, X12 envelope checks). Module: connectors.
Chapter 20 (v2.5, book layer; package stays 0.1.0): estates (five ports, one thin adapter per cloud, pinned model
versions that refuse substitution by region, fourteen parity checks, cost per estate). Module: estates.
Chapter 21 (v2.6, book layer; package stays 0.1.0): upfront quality scorer (completeness, legibility,
consistency as hard gates; request, never guess) with a per-source register, and the lineage chain
(source, page, extraction, calculation, claim, release; versioned reference tables). Modules: quality, lineage.
Chapter 23 (v3, book layer; package stays 0.1.0): retrieval on the customer's documents (ACLs inherited from the
source at ingest and failing closed, permission and lifecycle filters before ranking, explicit supersession in the
context header, multi-participant audiences as an intersection, ACL drift check, question-set recall at k by
category, cost lines with payer and cost center). Module: retrieval.
Chapter 24 (v3.1, book layer; package stays 0.1.0): surface where they work, brain where it is governed (option
scoring with flip points and weight draws, parallel fan-out with per-source timeouts, on-behalf-of token broker
that refuses foreign audiences, the one-call turn contract, and a mode flag enforced in the brain). Module: surface.
Chapter 26 (v3.3, book layer; package stays 0.1.0): evaluation suites built with the customer's experts (14-day
gold-value rule, kappa calibration with exact and judgment lines, a named adjudicator with reason codes, judge
validation by TPR and TNR with corrected rate and interval, flip rate, four-cell regression comparison and a
customer-owned gate that blocks lost critical items). Module: evals.
Chapter 27 (v3.4, book layer; package stays 0.1.0): the confidence router (reliability, ECE, resolution and
AUROC; a correctness model with isotonic calibration; proceed threshold by Wilson lower bound and a floor below
which nothing is suggested; fail-closed evidence gates and the not-in-the-documents answer check; post-review
error, drift monitor and the signed threshold record). Module: routing.
Chapter 28 (v3.5, book layer; package stays 0.1.0): guardrails and the customer's rules (rule cards with owner,
source, effect, modality and VERIFY review day; rules as tests with a passing and a catching case; fail-closed
suite with block > route > repair > flag precedence; input, output, action and budget kinds; budgets, a
progress-defined circuit breaker and a fleet breaker). Module: guardrails.
Chapter 29 (v3.6, book layer; package stays 0.1.0): the pyramid runner (five layers with coverage target,
frequency and budget; change-aware layer selection by path; three-valued slice verdicts by paired sign test; a
merge gate that blocks on any fail and holds inconclusive slices without item sign-off; seeded control mutants
that must be caught at their designed layer; stream independence; hash-chained test evidence and a trace
matrix). Module: pyramid.
Chapter 30 (v3.7, book layer; package stays 0.1.0): small models and fine-tuning on site (the fine-tune
evaluation suite: paired comparison on the same expert-scored documents with Wilson intervals and an exact McNemar
test, per-class accuracy, familiarity and an absent-class guard with owner rules, cost per document, monthly cost
and crossover by serving option, the signed training-data record, the model-risk classification change and the
switch gate). Module: finetune.
Chapter 33 (v4.1, book layer; package stays 0.1.0): model risk and the customer's governance (the classification
test as data with frameworks as ordered rules, registers re-run at every design change, the validation plan per
outcome, a model-risk pack generated from evaluation-suite evidence with a lint, the monitoring computability check
that every metric can be run by the customer without the vendor, repeat-run agreement, the validator's question
map and review conditions). Module: modelrisk.
Chapter 34 (v4.2, book layer; package stays 0.1.0): procurement, legal and the contract (vendor commitments
extracted from numbered clauses and classed by kind, a lint against the dependency and decision registers,
undefined acceptance triggers, service levels designed as tests with an exact binomial n and k, point and
zero-tolerance rules priced for comparison, services net by contract form and the margin a contract leaves).
Module: contract.
Chapter 35 (v4.3, book layer; package stays 0.1.0): data protection as data (the data map generated from deployed
configuration with one hop per component and store, HIPAA, GDPR and state-law rules as lint, a PII scan with
patterns and known values that never prints a value, an erasure trace per subject, minimum necessary, and a map
digest the approver signs). Module: privacy.
Chapter 37 (v4.5, book layer; package stays 0.1.0): the gate tracker (five gates with entry evidence, exit
criteria judged per class with Wilson intervals, evidence kinds that refuse model confidence, fluent summaries and
component tests for customer outcomes, gate order that holds a later decision) and the accountable executive's
pack (eight artifacts, present/partial/missing, digest) with a residual-risk lint. Module: gates.
Chapter 41 (v5, book layer; package stays 0.1.0): the hand-over test (an evidence-weighted readiness score
where credit needs a named customer person doing the task alone, four gates that cap the score at 0.60, the
single-person drop, runbook lint RB1 to RB6 with the mode rule, alert route check, RACI check, reading-path
coverage and a failure drill in which any page to the vendor is a touch). Module: handover.
Chapter 42 (v5.1, book layer; package stays 0.1.0): the first ninety days (a drift monitor with a leading
fingerprint PSI and a lagging scored sample that only counts customer reads, threshold re-calibration on the
Wilson upper bound with a gold-set owner's signature, page-route lint with the customer as primary, incident
timelines with detect, acknowledge and mitigate, a deprecation plan against freeze windows, an upgrade gate
returning PROMOTE, HOLD or ROLLBACK, an ownership map with departures, deputies and orphans, and a Live Stable
review that refuses vendor-measured criteria). Module: liveops.
Chapter 43 (v5.2, book layer; package stays 0.1.0): managed service or hand-over (readiness with use-decay, a
two-year cost and dependency model for both sides, exit lint by asset owner, exit drill, retainer pricing with
rollover). Module: service.
Chapter 47 (v5.4, book layer; package stays 0.1.0): engagement linter and playbook registry, recurrence by shape,
evidence-ranked field reports and rotation continuity. Module: playbooks.
"""
__version__ = "0.1.0"
from .access import AccessRequest, AccessTracker, LADDER
from .readiness import ReadinessRegister, ReadinessResult
from .engagement import Decision, EngagementRepo, Evidence, Note, Request
from .deployment import Checklist, Proof, Verdict, DIMENSIONS, is_person
from .cadence import Item, Plan, Record, Register, plan_sprint, gate_check, review, lint_status, bus_factor
from .escalation import Escalation, EscalationPolicy, customer_days
from .datareadiness import DataReadinessRegister, FieldSpec, FieldReadiness
from .histories import AccessHistory, RUNG_WORK, rung_reached_days
from .synthetic import RepresentativenessReport, GapLine, psi, coverage, classifier_auc
from .deid import known_value_scan, scrub_known, k_anonymity, linkage_attack, ReleaseCheck
from .shadow import ShadowTap, make_canary, scan_stores
from .sampling import allocate, weighted_accuracy, Manifest
from .connectors import FileDrop, MailQueue, ScreenConnector, WriteBack, reconcile
from .gateway import (GatewayAdapter, GatewayStop, RotationSchedule, DeprecationRegister, VersionLedger,
                      capability_gap, classify, cost_per_success, ACTIONS)
from .estates import (ModelPin, ModelResult, VersionUnavailable, resolve_pin, conformance, estate_cost,
                      Evidence as EstateEvidence, CHECKS as PARITY_CHECKS, REFUSE_TO_ABSTRACT)
from .quality import Check, QualityScorer, Verdict, summarize, request_for, SourceSpec, SourceRegister
from .lineage import LineageStore, RefTables, KINDS as LINEAGE_KINDS, digest
from .retrieval import (Index, Passage, Principal, Audience, Question, IngestRefused, evaluate, context_header,
                        acl_drift, CostMeter, CostLine, token_cost)
from .surface import (Option, total as option_total, contributions, rank as rank_options, lead, flip_point,
                      sensitivity, weight_draws, Source, run_turn, percentile, Token, TokenBroker,
                      AudienceMismatch, TurnRequest, TurnResponse, ModeFlag, MODES)
from . import routing  # noqa: F401,E402
from . import pyramid  # noqa: F401,E402
from . import finetune  # noqa: F401,E402
from . import service  # noqa: F401,E402
from . import redteam  # noqa: F401,E402  (v4.4, Chapter 36)
from . import playbooks  # noqa: E402,F401
