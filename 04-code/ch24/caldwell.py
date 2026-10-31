"""Chapter 24 fixtures: Caldwell Mutual's surface decision (deterministic stand-in; days 104 to 119).
Weights were set by Daniel Reyes, Anne Kessler and Priya Natarajan on day 110; scores were proposed by Northlight
with a written reason each and challenged line by line. Latencies are a stand-in fitted to the day-112 prototype."""
from fieldkit.surface import Option, Source

DIMS = ["adoption", "governance visibility", "residency and egress", "identity fidelity",
        "verification and evaluation", "latency", "reversibility", "time to first user", "run cost",
        "operability and hand-over"]
WEIGHTS = dict(zip(DIMS, [16, 14, 10, 10, 10, 8, 8, 8, 6, 10]))

OPTIONS = [
    Option("A", "new application in Caldwell's cloud", dict(zip(DIMS, [2, 5, 5, 5, 5, 4, 3, 2, 3, 4]))),
    Option("B", "the suite's own agent", dict(zip(DIMS, [5, 2, 2, 3, 2, 4, 2, 5, 4, 4]))),
    Option("C", "hybrid: thin surface, governed brain", dict(zip(DIMS, [5, 4, 4, 4, 5, 4, 5, 2, 2, 3]))),
    Option("D", "suite orchestration, many calls out", dict(zip(DIMS, [5, 3, 3, 3, 3, 2, 3, 4, 3, 2]))),
]
REASONS = {
    ("A", "adoption"): "adjusters spend 61% of their day in the suite; a new tab competes with all of it",
    ("B", "governance visibility"): "prompts, retrieval and traces sit in the suite vendor's service, outside Caldwell's log groups",
    ("C", "time to first user"): "two deployables, two change routes, a token broker: about five weeks",
    ("C", "operability and hand-over"): "two owning teams: suite administration and the cloud platform",
    ("D", "latency"): "14 boundary crossings per turn, each paying the network and an exchange",
}
# User groups differ in where they work, so adoption is scored per group (day 104 sample).
GROUP_ADOPTION = {"adjusters": [2, 5, 5, 5], "supervisors": [2, 5, 5, 5], "intake clerks": [4, 3, 3, 3]}
TIME_IN_TOOL = {  # share of logged working minutes, 14 adjusters and 9 intake clerks, 5 days each (day 104)
    "adjusters": {"suite mail and calendar": 34, "suite chat and meetings": 21, "suite documents": 6,
                  "claims-core": 27, "phone and other": 12},
    "intake clerks": {"suite mail and calendar": 18, "suite chat and meetings": 7, "suite documents": 3,
                      "claims-core": 31, "intake queue tool": 36, "phone and other": 5},
}

SOURCES = [
    Source("policy-admin", 600, 0.30, "api://caldwell-policy"),
    Source("claims-core", 1400, 0.40, "api://caldwell-claims"),
    Source("retrieval", 700, 0.30, "api://nl-retrieval"),
    Source("loss-history", 900, 0.35, "api://caldwell-dw"),
    Source("rules-catalog", 300, 0.25, "api://caldwell-rules"),
    Source("fnol-docs", 650, 0.30, "api://caldwell-docs"),
]
BUDGET_P95_MS = 4000
TIMEOUT_MS = 2500
