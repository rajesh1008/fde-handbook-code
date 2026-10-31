"""Listing 24.6: the day-117 rollback rehearsal. 42 pilot surfaces; decision at 10:00 (t=0). Client-side flag only,
then the flag enforced in the brain. Turns after the decision still run in shadow (deterministic stand-in)."""
import random
import _paths  # noqa: F401
from fieldkit.surface import ModeFlag

rng = random.Random(117)
N, POLL = 42, 300
clients = []
for i in range(N):
    stale = (i == 17)            # one surface with a cached manifest that does not poll for three hours
    clients.append(dict(phase=rng.uniform(0, POLL), stale=stale))
turns = []
for i in range(N):
    t = rng.uniform(-1800, 0)
    while t < 4 * 3600:
        t += rng.expovariate(1 / 360)
        if t > 0:
            turns.append((t, i))
turns.sort()


def client_sees_off(c, t):
    if c["stale"]:
        return t >= 3 * 3600
    first_poll = c["phase"]
    return t >= first_poll


def run(server_side):
    flag = ModeFlag("live", ttl_s=30); flag.set("off" if not server_side else "shadow", 0.0, "rehearsal")
    shown, last, shadow, times = 0, 0.0, 0, []
    for t, i in turns:
        if server_side:
            mode = flag.mode_at(t)
            if mode == "live":
                shown += 1; last = t; times.append(t)
            else:
                shadow += 1
        else:
            if not client_sees_off(clients[i], t):
                shown += 1; last = t; times.append(t)
    return shown, last, shadow, times


a = run(False); b = run(True)
print(f"turns after the decision (4 h): {len(turns)}")
print(f"client-side flag only: answers shown after decision {a[0]:>3}, last at +{a[1]/60:6.1f} min, brain evaluated 0 in shadow")
print(f"flag enforced in brain: answers shown after decision {b[0]:>3}, last at +{b[1]/60:6.1f} min, shadow turns {b[2]}")
MARKS = (0.5, 1, 2, 5, 10, 30, 60, 120, 180, 240)
for label, r in (("client-side", a), ("in brain", b)):
    print(f"cumulative answers shown, {label}: " + " ".join(f"{m}m={sum(1 for x in r[3] if x <= m*60)}" for m in MARKS))
print("rehearsal log, day 117 (minutes after decision):")
for m, step in ((0.0, "decision by Priya Natarajan (rehearsal script R-3)"), (1.5, "pre-approved standard change CHG-24-117 opened"),
                (2.2, "mode set to shadow in the brain's config"), (2.7, "brain answers stop; surfaces render the fallback card"),
                (3.6, "synthetic probe from a test surface returns mode=shadow"), (5.4, "pilot adjusters notified in the team channel"),
                (41.0, "shadow agreement still being recorded; roll forward rehearsed at +41 min")):
    print(f"  +{m:4.1f}  {step}")
