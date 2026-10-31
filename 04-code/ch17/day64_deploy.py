"""Day 64: the first deployment into Caldwell's team account, and the egress denial that proved the design.

Failure injection: image 0.9 ignores the Terraform's MODEL_BASE_URL and calls the provider directly, and its
tracing library exports to a vendor service. There is no route out, so every attempt is denied and logged in
Caldwell's log, which Caldwell's security operations team owns. Deterministic stand-in; no cloud is called."""
from collections import Counter
import account, runner
from fieldkit.environment import AuditLog


def clock(sec):  # seconds after 15:31:00 Eastern
    h, r = divmod(15 * 3600 + 31 * 60 + sec, 3600); m, s = divmod(r, 60)
    return f"{h:02d}:{m:02d}:{s:02d}"


tf = account.load()
p = account.plan(tf)
print(f"Day 64, 15:20 Eastern. Caldwell's pipeline applies the module in account {account.ACCOUNT} ({account.REGION}).")
print(f"plan: {p['add']} to add, 0 to change, 0 to destroy")
print(f"  internet gateways {p['igw']}, NAT gateways {p['nat']}, public IP on task: {p['public_ip']}")
print(f"  runner egress: {'; '.join(p['egress'])} (the VPC's own endpoints)")
print(f"  endpoints: {', '.join(p['endpoints'])}")

log = AuditLog("Caldwell security operations")
pol = account.egress_policy(tf, log)
env, secrets = account.container_env(tf)

# ---- run 1: image 0.9 --------------------------------------------------------------------------------------
print("\n--- run 1, image 0.9, 15:31 to 16:12 ---")
model_host, trace_host = runner.resolve("0.9", env)
seen, t, task = [], 0, 0
while t < 41 * 60:                         # the service restarts the task until the team stops it at 16:12
    task += 1
    start = t
    fails = 0
    for doc in range(3):                   # three documents, four attempts each, then the health check gives up
        for attempt, backoff in enumerate((0, 2, 4, 8)):
            t += backoff
            ok = pol.check(model_host, t=clock(t))
            t += 10                        # connect timeout: a dropped packet does not say why
            if not ok and len(seen) < 3:
                seen.append(f"  {clock(t)} task {task} doc {doc + 1} attempt {attempt + 1}: connect timeout after 10 s ({model_host}:443)")
            if ok: break
        fails += 1
    for k in range(0, t - start, 30):      # the tracing exporter flushes every 30 s
        if trace_host: pol.check(trace_host, t=clock(start + k))
    t += 90 + 60                           # health check fails, task stops, service starts a new one
    seen.append(f"  {clock(t - 150)} task {task}: 3 documents failed, health check failed, task stopped") if task <= 1 else None
print("runner log (what the runner saw):")
print("\n".join(seen))
print(f"  ... {task} tasks started and stopped before the service was scaled to zero at 16:12")

print("\nCaldwell egress log, query action=DENY source=nl-shadow-runner (what Caldwell saw):")
deny = log.query(action="DENY")
c = Counter(r["dest"] for r in deny)
print(f"  {'destination':36} {'denied':>6}  {'first':>8}  {'last':>8}")
for dest, n in c.most_common():
    ts = [r["t"] for r in deny if r["dest"] == dest]
    print(f"  {dest:36} {n:>6}  {min(ts):>8}  {max(ts):>8}")
print(f"  allowed: {len(log.query(action='ALLOW'))}   bytes that left the account: 0 (no route out)")
print(f"  chain check: {len(log.verify())} breaks in {len(log.records)} records")

# ---- run 2: image 0.9.1 ------------------------------------------------------------------------------------
print("\n--- run 2, image 0.9.1, 17:05: connectivity smoke test (no model call yet) ---")
before = len(log.records)
model_host, trace_host = runner.resolve("0.9.1", env)
for host, what in [(f"secretsmanager.{account.REGION}.amazonaws.com", "read GATEWAY_KEY from Caldwell's secret"),
                   (model_host, "TLS handshake and GET /health"),
                   ("caldwell-nl-sandbox-slices.s3.us-east-1.amazonaws.com", "list deidentified/ prefix"),
                   (f"logs.{account.REGION}.amazonaws.com", "write one log line")]:
    ok = pol.check(host, t="17:05")
    print(f"  {'ALLOW' if ok else 'DENY '} {host:52} {what}")
print(f"  tracing exporter: {'off' if trace_host is None else trace_host}")
new = log.records[before:]
print(f"  denied in run 2: {sum(r['action'] == 'DENY' for r in new)}   chain check: {len(log.verify())} breaks in {len(log.records)} records")
