"""Write the two fixture weeks for the Chapter 1 lab into data/.

Week A is the FDE's week at Caldwell Mutual, days 81 to 85 (day 82 is the Tuesday in section 1.1).
Week B is the failure injection: the same engineer, the same engagement, a week in which every
customer meeting was cancelled and the time went into internal work. It is built to look productive.
All names are fictional (roster in the style sheet). Deterministic: no randomness except a seeded
generator for week B's commit hashes and file paths.
"""
import csv, hashlib, pathlib, random

D = pathlib.Path(__file__).resolve().parent / "data"
C, N = "caldwellmutual.com", "northlight.ai"
ME = f"fde@{N}"

# day, start, end, title, attendees (semicolon separated), tag
WEEK_A_CAL = [
    (81, "08:30", "09:00", "Plan the week from the decision log", ME, "decide"),
    (81, "09:00", "09:30", "Northlight FDE stand-up", f"{ME};laura.finch@{N}", "internal"),
    (81, "10:00", "12:00", "Sit with the intake team in the mailroom", f"{ME};tom.whitfield@{C}", "discover"),
    (81, "13:00", "16:00", "Focus: policy-number parser", ME, "build"),
    (81, "16:00", "17:00", "Review 20 corrected extractions", f"{ME};anne.kessler@{C}", "pass"),
    (81, "17:00", "17:30", "Runbook draft: what the parser does when it fails", ME, "hand over"),
    (82, "07:30", "08:00", "Gateway key rotation check", ME, "access"),
    (82, "08:30", "10:00", "Sit with Tom Whitfield at intake", f"{ME};tom.whitfield@{C}", "discover"),
    (82, "10:00", "10:30", "Write up: which fields need no model", ME, "decide"),
    (82, "10:30", "11:00", "Correction review with Anne Kessler", f"{ME};anne.kessler@{C}", "pass"),
    (82, "11:00", "12:00", "Shadow feed design: Priya's three questions", f"{ME};priya.natarajan@{C}", "access"),
    (82, "13:00", "15:30", "Focus: deterministic policy-number parser", ME, "build"),
    (82, "15:30", "16:00", "Update access tracker, send to Daniel Reyes", ME, "access"),
    (82, "16:00", "16:30", "Hours and margin with Laura", f"{ME};laura.finch@{N}", "internal"),
    (82, "16:30", "17:00", "Decision log", ME, "decide"),
    (83, "09:00", "09:30", "Northlight FDE stand-up", f"{ME};laura.finch@{N}", "internal"),
    (83, "09:30", "12:00", "Focus: parser tests on the 47 low-confidence files", ME, "build"),
    (83, "13:00", "14:00", "Claims supervisors: exceptions they see weekly", f"{ME};anne.kessler@{C};supervisors@{C}", "discover"),
    (83, "14:00", "16:00", "Turn Anne's corrections into evaluation cases", ME, "pass"),
    (83, "16:00", "17:00", "Product feedback: the parser as a product feature", f"{ME};product@{N}", "internal"),
    (84, "09:00", "10:00", "Weekly decisions with Daniel Reyes and Anne Kessler", f"{ME};daniel.reyes@{C};anne.kessler@{C}", "decide"),
    (84, "10:00", "12:00", "Focus: wire parser into the intake pipeline", ME, "build"),
    (84, "13:00", "14:00", "Log retention for the shadow feed", f"{ME};priya.natarajan@{C}", "access"),
    (84, "14:00", "14:30", "Walk Caldwell on-call through the parser's failure modes", f"{ME};claims-oncall@{C}", "hand over"),
    (84, "14:30", "16:00", "Focus: pipeline integration tests", ME, "build"),
    (84, "16:30", "18:30", "Drive Hartford to Boston", ME, "travel"),
    (85, "09:00", "10:00", "Northlight engagement review", f"{ME};laura.finch@{N};graham.lowell@{N}", "internal"),
    (85, "10:00", "12:00", "Focus: parser edge cases from Tom's examples", ME, "build"),
    (85, "13:00", "13:30", "Follow-up questions for Tom Whitfield", f"{ME};tom.whitfield@{C}", "discover"),
    (85, "13:30", "15:00", "Friday status and evidence links", ME, "pass"),
    (85, "15:00", "15:30", "Friday status call with Daniel Reyes", f"{ME};daniel.reyes@{C}", "decide"),
]

# id, opened_day, closed_day ('' if open), title, owner, tag
WEEK_A_TICKETS = [
    ("CAL-112", 78, 82, "Gateway key rotation: confirm pipeline picks up new key", f"priya.natarajan@{C}", "access"),
    ("CAL-118", 80, 85, "Policy-number parser for the HP###### pattern", ME, "build"),
    ("CAL-119", 81, 83, "Parser: handle policy numbers split across two OCR lines", ME, "build"),
    ("CAL-121", 81, "", "Shadow feed: where it runs, under whose identity, who sees the logs", f"priya.natarajan@{C}", "access"),
    ("CAL-122", 82, 84, "Log retention for shadow feed", f"priya.natarajan@{C}", "access"),
    ("CAL-123", 82, 85, "Evaluation cases from Anne's 20 corrections", f"anne.kessler@{C}", "pass"),
    ("CAL-124", 83, "", "Supervisors' weekly exception list", f"anne.kessler@{C}", "discover"),
    ("CAL-125", 84, 84, "Decision: parser output is advisory until Anne signs off", f"daniel.reyes@{C}", "decide"),
    ("CAL-126", 84, "", "On-call runbook: parser failure modes", ME, "hand over"),
]

WEEK_A_COMMITS = [
    (81, "Add policy-number pattern and checksum", "intake/policy_number.py"),
    (81, "Tests: 12 policy numbers from Tom's desk", "tests/test_policy_number.py"),
    (82, "Handle split policy numbers across OCR lines", "intake/policy_number.py"),
    (82, "Record key-rotation check in run log", "ops/gateway_check.py"),
    (82, "Decision log: fields that need no model", "docs/decisions/0007-no-model-fields.md"),
    (83, "Tests: 47 low-confidence files, parser only", "tests/test_low_confidence.py"),
    (83, "Evaluation cases from Anne's corrections", "evals/cases_anne_v1.jsonl"),
    (84, "Wire parser ahead of model call", "intake/pipeline.py"),
    (84, "Runbook: parser failure modes", "docs/runbook/parser.md"),
    (84, "Integration test: parser then gateway", "tests/test_pipeline.py"),
    (85, "Edge cases from Tom's examples", "intake/policy_number.py"),
    (85, "Friday status with evidence links", "docs/status/day85.md"),
]

WEEK_B_CAL = [
    (88, "09:00", "09:30", "Northlight FDE stand-up", f"{ME};laura.finch@{N}", "internal"),
    (88, "09:30", "12:30", "Focus: refactor pipeline into plugins", ME, "build"),
    (88, "13:30", "17:30", "Focus: refactor pipeline into plugins", ME, "build"),
    (89, "09:00", "09:30", "Northlight FDE stand-up", f"{ME};laura.finch@{N}", "internal"),
    (89, "09:30", "12:30", "Focus: async extraction workers", ME, "build"),
    (89, "13:30", "15:30", "Focus: async extraction workers", ME, "build"),
    (89, "15:30", "16:30", "Internal demo: new pipeline", f"{ME};product@{N};graham.lowell@{N}", "internal"),
    (90, "09:00", "09:30", "Northlight FDE stand-up", f"{ME};laura.finch@{N}", "internal"),
    (90, "09:30", "12:30", "Focus: test coverage to 90%", ME, "build"),
    (90, "13:30", "17:00", "Focus: CI pipeline speed-up", ME, "build"),
    (91, "09:00", "12:00", "Focus: prompt template library", ME, "build"),
    (91, "13:00", "15:00", "Benchmark three models on synthetic claims", ME, "pass"),
    (91, "15:00", "16:00", "Product feedback: plugin architecture", f"{ME};product@{N}", "internal"),
    (92, "09:00", "10:00", "Northlight engagement review", f"{ME};laura.finch@{N};graham.lowell@{N}", "internal"),
    (92, "10:00", "12:30", "Focus: docs site for the plugin API", ME, "build"),
    (92, "13:30", "16:00", "Focus: clean-up and release notes", ME, "build"),
]


G, MSP = "greystonehealth.org", "greystone-msp.net"
# Second customer: Greystone Health's infrastructure is run by a managed-service provider whose staff
# sit on a different email domain. A contact rule keyed to one domain misses them.
WEEK_C_CAL = [
    (40, "09:00", "09:30", "Northlight FDE stand-up", f"{ME};laura.finch@{N}", "internal"),
    (40, "10:00", "11:30", "Private endpoint design", f"{ME};netops@{MSP}", "access"),
    (40, "13:00", "16:00", "Focus: note-summary evaluation harness", ME, "build"),
    (41, "09:00", "10:30", "Identity: managed identity for the pipeline", f"{ME};identity@{MSP};sam.oakley@{G}", "access"),
    (41, "11:00", "12:00", "Clinical review of 15 summaries", f"{ME};michael.hart@{G}", "pass"),
    (41, "13:00", "16:30", "Focus: evaluation harness", ME, "build"),
    (42, "09:00", "09:30", "Northlight FDE stand-up", f"{ME};laura.finch@{N}", "internal"),
    (42, "09:30", "11:00", "Firewall change request walkthrough", f"{ME};netops@{MSP}", "access"),
    (42, "11:00", "12:00", "Log export to the security team's tooling", f"{ME};soc@{MSP}", "access"),
    (42, "13:00", "16:00", "Focus: de-identification checks", ME, "build"),
    (43, "09:00", "12:00", "Focus: harness on the sampled notes", ME, "build"),
    (43, "13:00", "14:00", "Change advisory board dry run", f"{ME};change@{MSP}", "decide"),
    (43, "14:00", "16:00", "Write up evaluation results", ME, "pass"),
    (44, "09:00", "10:00", "Northlight engagement review", f"{ME};laura.finch@{N};graham.lowell@{N}", "internal"),
    (44, "10:00", "12:00", "Focus: harness clean-up", ME, "build"),
    (44, "13:00", "13:30", "Runbook outline for the operations team", f"{ME};ops@{MSP}", "hand over"),
]
WEEK_C_TICKETS = [
    ("GH-31", 38, 42, "Private endpoint for the model gateway", f"netops@{MSP}", "access"),
    ("GH-33", 40, "", "Managed identity for the pipeline", f"identity@{MSP}", "access"),
    ("GH-34", 41, 41, "Clinical review of 15 summaries", f"michael.hart@{G}", "pass"),
    ("GH-36", 42, "", "Log export format agreed", f"soc@{MSP}", "access"),
]
WEEK_C_COMMITS = [
    (40, "Evaluation harness skeleton", "evals/harness.py"),
    (41, "Harness: clinical rubric", "evals/rubric.py"),
    (42, "De-identification checks", "intake/deid.py"),
    (43, "Run harness on sampled notes", "evals/run_sampled.py"),
    (44, "Runbook outline", "docs/runbook/outline.md"),
]


def week_b_tickets():
    out, titles = [], ["Refactor stage %d into plugin", "Async worker for stage %d", "Raise coverage of module %d",
                       "Speed up CI job %d", "Template %d for prompt library", "Docs page %d for plugin API"]
    for i in range(19):
        out.append((f"NL-{400 + i}", 87, 88 + i % 5, titles[i % 6] % (i + 1), ME, "build"))
    return out


def week_b_commits():
    rng = random.Random(1)
    areas = ["pipeline/plugins/", "pipeline/workers/", "tests/", "ci/", "prompts/", "docs/plugin_api/"]
    verbs = ["Refactor", "Extract", "Rename", "Speed up", "Add tests for", "Document"]
    out = []
    for i in range(41):
        k = rng.randrange(len(areas))
        thing = rng.choice(["loader", "router", "worker", "stage", "config", "retry"])
        out.append((88 + i % 5, f"{verbs[k]} {thing}", areas[k] + f"{thing}_{rng.randint(1, 9)}.py"))
    return out


def write(name, cal, tickets, commits):
    with open(D / f"{name}_calendar.csv", "w", newline="") as f:
        w = csv.writer(f); w.writerow(["day", "start", "end", "title", "attendees", "tag"]); w.writerows(cal)
    with open(D / f"{name}_tickets.csv", "w", newline="") as f:
        w = csv.writer(f); w.writerow(["id", "opened_day", "closed_day", "title", "owner", "tag"]); w.writerows(tickets)
    with open(D / f"{name}_commits.log", "w") as f:
        for day, subject, path in commits:
            h = hashlib.sha1(f"{name}{day}{subject}{path}".encode()).hexdigest()[:10]
            f.write(f"{h}|day {day}|fde|{subject}|{path}\n")


if __name__ == "__main__":
    D.mkdir(exist_ok=True)
    write("week_a_caldwell", WEEK_A_CAL, WEEK_A_TICKETS, WEEK_A_COMMITS)
    write("week_b_injected", WEEK_B_CAL, week_b_tickets(), week_b_commits())
    write("week_c_greystone", WEEK_C_CAL, WEEK_C_TICKETS, WEEK_C_COMMITS)
    print("wrote", sorted(p.name for p in D.iterdir()))
