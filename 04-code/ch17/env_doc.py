"""Days 57 and 63: Priya Natarajan's three questions answered in writing, linted before she reads them."""
import _paths  # noqa: F401
from fieldkit.environment import Answer, EnvironmentDoc

C, N = "Caldwell", "Northlight"
v1 = EnvironmentDoc(C, N, [
    Answer("where", "production", "Caldwell's AWS, in a team account", "", C),
    Answer("where", "pre-production", "Northlight build environment until the team account is ready",
           "northlight-ci runners", N),
    Answer("identity", "production", "service role for the runner",
           "arn:aws:iam::111122223333:role/nl-shadow-runner", C),
    Answer("logs", "production", "CloudWatch in the team account; traces to our tracing service for debugging",
           "northlight tracing project nl-caldwell", N),
])
v2 = EnvironmentDoc(C, N, [
    Answer("where", "production", "team account 111122223333, us-east-1, VPC with no route out; "
           "changed only by Caldwell's pipeline", "account 111122223333, VPC nl-shadow", C),
    Answer("where", "pre-production", "the same account, pre-production gateway tier; no laptop or vendor CI "
           "touches Caldwell data", "account 111122223333, us-east-1", C),
    Answer("identity", "production", "runner role under Caldwell's vendor boundary; claims reads as "
           "svc-nl-claims-ro; adjuster results on-behalf-of, rechecked with claims-core before return",
           "arn:aws:iam::111122223333:role/nl-shadow-runner; svc-nl-claims-ro", C),
    Answer("identity", "pre-production", "same role; no user delegation in shadow; engineers read results "
           "through Caldwell SSO group nl-shadow-readers", "SSO group nl-shadow-readers", C),
    Answer("logs", "production", "runner, egress and recheck logs in Caldwell's log archive under Caldwell's "
           "key; readers: four named; retention 90 days; no vendor tracing", "log group /caldwell/nl-shadow/runner", C),
    Answer("logs", "pre-production", "the same stores; readers: the same four named; retention 90 days",
           "log group /caldwell/nl-shadow/runner", C),
])
if __name__ == "__main__":
    for name, d in (("v1, day 57", v1), ("v2, day 63", v2)):
        out = d.lint()
        print(f"{name}: {len(d.answers)} answers, {len(out)} findings")
        for f in out:
            print(f"  {f}")
    print("\nv2 as signed (question / phase: evidence Caldwell can look up)")
    for a in v2.answers:
        print(f"  {a.question:8} / {a.phase:14}: {a.evidence}")
