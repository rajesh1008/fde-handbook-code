# Chapter 47 lab: engagement linter and playbook registry (fieldkit v5.4)

Deterministic stand-in: twenty engagement manifests (four named customers, N05 to N20 numbered stand-ins), seventeen
component kinds, four playbooks, twelve field reports. No model calls. `./make_outputs.sh` regenerates every output
the chapter quotes and runs the lab tests with the full fieldkit suite.

| Script | Listing | What it shows |
|---|---|---|
| repeats.py | 47.1 | what repeats by name and by shape |
| lint_run.py 15 / 18 | 47.2 to 47.4 | the engagement linter E1 to E8 over all twenty manifests |
| registry_run.py form / n17 / probe / match | 47.8 to 47.11 | failure injection: PB-1@1.3 passes the form lint and fails at N17, which has no gateway; the probe and the precondition match |
| loop.py rank / ship | 47.5, 47.6 | field reports by votes and by evidence; two features shipped |
| absorb.py ttp / cap | 47.12, 47.13 | time to production by adoption order; capacity at month 18 |
| rotation.py | 47.7 | anchor changes as customers saw them |
| pod_loops.py | 47.14 | the pod's own loops: FK-N1's nineteen green nights, the stop registry and the pre-run hash check (Section 47.7) |
| tryit.py a / b / c | Try It Yourself | thresholds, a bank with no vault, an artifact for FR-003 |
