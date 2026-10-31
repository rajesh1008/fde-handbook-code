"""Live-incident drill against the replay (Chapter 42). Usage: python drill.py v0|v2
The machine side is simulated minute by minute: the 02:00 TMS file (batch deadline 03:30, Memphis time), a
per-minute model quota of 120 calls after a platform cost change, workers autoscaling from 4 to 12 as on every weekday night,
three model calls per document, and a reconciliation queue with strict order per carrier.
v0 (the night of production day 38): synchronized retries capped at 2 s with no jitter, Retry-After ignored,
     five attempts before an error message joins the reconciliation queue at the head of its carrier, a
     throughput alert, the runbook as handed over, a rollback approver named as a person.
v2 (the drill of production day 70): the day-43 runbook change: a shared, jittered token bucket at 80% of the
     configured quota, Retry-After honored, dead-letter after three attempts, a 429-ratio alert and a queue-age
     alert, rollback approver = the own-operations role. Injected failure: the quota is cut and the quota-change
     hook does not fire, so the bucket still believes the old quota of 240.
Human step durations are scenario inputs (v0 from the day-38 incident record); every machine time is computed."""
import sys
import _paths  # noqa: F401
from fieldkit.liveops import Incident, hhmm

mode = sys.argv[1] if len(sys.argv) > 1 else "v2"
QUOTA, PER_WORKER, CALLS, PLAN = 120, 20, 3, 40     # calls/min; calls/worker/min; calls/document; documents/min
BATCH, START, DEADLINE = 2140, 120, 210
workers = lambda t: 4 if t < 122 else 6 if t < 124 else 8 if t < 126 else 10 if t < 128 else 12
inc = Incident(f"Pennant drill {mode}")
left, done, exhausted, stalled, recon_q, recon = BATCH, 0, 0, False, 0, 0
budget = 0.8 * 240                                     # v2: the bucket still believes the old quota
streak, rows, rolled = 0, [], None
if mode == "v0":
    steps = [(4, "ack: Northlight support on-call (primary on the page route)"),
             (5, "runbook step 1: check the provider status page (green)"),
             (5, "runbook step 2: 'on 429, wait and retry'; no change"),
             (7, "escalate to the FDE; FDE joins on the pseudonymized view"),
             (9, "FDE finds the stall: reconciliation queue flat, error messages at the head of three carriers"),
             (9, "rollback approval: runbook names Jenna Ruiz; no answer"),
             (9, "Rosa Delgado reached, briefed, approves rollback to shadow"),
             (6, "Andre Willis (Pennant platform) rolls back to shadow")]
else:
    steps = [(2, "ack: Nadia Brooks, Pennant platform on-call (primary)"),
             (4, "runbook 4.2: read the quota from the gateway (120); set the bucket to 96"),
             (6, "runbook 4.3: verify 429 ratio under 5% and queue age falling for 5 minutes")]
si, step_end = -1, None
for t in range(START, 240):
    if mode == "v0":
        attempts = min(workers(t) * PER_WORKER, CALLS * left)
    else:
        attempts = min(workers(t) * PER_WORKER, int(budget), CALLS * left)
    ok = attempts if attempts <= QUOTA else int(QUOTA * QUOTA / attempts)
    p = ok / attempts if attempts else 1.0
    docs = min(left, int(ok / CALLS * p)) if attempts > QUOTA else min(left, ok // CALLS)
    tries = 5 if mode == "v0" else 3
    lost = int((attempts / CALLS - docs) * (1 - p) ** tries) if attempts > QUOTA else 0
    left -= docs
    done += docs
    exhausted += lost
    if lost and mode == "v0":
        stalled = True                                # error messages hold the head of the biggest carriers
    recon_q += docs
    drain = min(recon_q, 1 if stalled else 60)          # the blocked carriers hold 1 in 60 slots open
    recon_q -= drain; recon += drain
    if attempts > ok and inc.first("start") is None:
        inc.log(t, "start", f"first 429s: {attempts - ok} of {attempts} calls rejected ({workers(t)} workers)")
    if mode == "v0":
        streak = streak + 1 if docs < 0.4 * PLAN else 0
        fire = streak >= 5
        rule = "page: documents completed below 40% of plan for 5 minutes"
    else:
        streak = streak + 1 if attempts and (attempts - ok) / attempts > 0.05 else 0
        fire = streak >= 3
        rule = "page: 429 ratio over 5% for 3 minutes"
    if fire and inc.first("detect") is None:
        inc.log(t, "detect", rule)
        step_end = t
    if step_end is not None and t >= step_end and si + 1 < len(steps):
        si += 1
        dur, what = steps[si]
        step_end = t + dur
        inc.log(t + dur, "ack" if si == 0 else "step", what)
        if mode == "v2" and si == 1:
            budget_at = t + dur
        if mode == "v2" and si == len(steps) - 1:
            inc.log(t + dur, "mitigate", "mitigated: 429 ratio under 5%, queue age falling; no rollback needed")
        if mode == "v0" and si == len(steps) - 1:
            rolled = t + dur
            inc.log(t + dur, "mitigate", "mitigated by rollback to shadow; live writes stopped")
    if mode == "v2" and si >= 1 and t >= budget_at:
        budget = 0.8 * QUOTA
    if t % 5 == 0 or t == 124:
        rows.append((t, workers(t), attempts, attempts - ok, done, exhausted, recon_q, recon))
    if (rolled and t >= rolled) or (left == 0 and recon_q == 0):
        rows.append((t, workers(t), attempts, attempts - ok, done, exhausted, recon_q, recon))
        break
print(f"LIVE-INCIDENT DRILL  Pennant  mode {mode}  ({'night of production day 38' if mode == 'v0' else 'drill on production day 70'}; "
      f"deterministic stand-in; Memphis time)")
print("time   workers  calls   429s  docs done  exhausted  recon queue  reconciled")
for t, w, a, f, d, e, q, r in rows:
    print(f"{hhmm(t)}  {w:>6}  {a:>5}  {f:>5}  {d:>9}  {e:>9}  {q:>11}  {r:>10}")
print("timeline:")
for m, k, txt in sorted(inc.events, key=lambda e: e[0]):
    print(f"  {hhmm(m)}  {k:<8} {txt}")
mt = inc.metrics()
print(f"time to detect {mt['ttd']} min   time to acknowledge {mt['tta']} min   time to mitigate {mt['ttm']} min")
end = rows[-1][0]
if mode == "v0":
    print(f"documents not reconciled when live writes stopped: {BATCH - recon} of {BATCH} (to the clerks at the 06:00 shift)")
else:
    print(f"batch reconciled by {hhmm(end)} (deadline 03:30); dead-lettered after 3 attempts, replayed at 03:15 under the bucket: {exhausted}")
