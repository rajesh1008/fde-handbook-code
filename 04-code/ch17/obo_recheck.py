"""Day 62: the entitlement replay. Whose rights decide what an adjuster sees?

Replays 600 adjuster searches from one working day (claim numbers and access decisions only, no claim content)
against the claims-core read replica, run inside Caldwell's account by Ruth Calloway's team. Deterministic
stand-in: the claims, units and flags are generated; the rules are Caldwell's."""
import random
import _paths  # noqa: F401
from fieldkit.environment import AuditLog, Delegation, RightsGate

rng = random.Random(17)
UNITS = ["personal auto", "property", "commercial"]
claims = {}
for i in range(4000):
    restricted = rng.random() < 0.06                  # SIU, litigated, employee: out of the nightly view
    claims[f"CLM-{100000 + i}"] = dict(unit=rng.choice(UNITS), restricted_0200=restricted, flagged_at=None)
view = [c for c, v in claims.items() if not v["restricted_0200"]]          # the replica view, built at 02:00
for c in rng.sample(view, 60):                                              # flagged during the day
    claims[c]["flagged_at"] = rng.randint(8 * 60, 17 * 60)
adjusters = {f"adj{n:02d}": UNITS[n % 3] for n in range(12)}
adjusters["twhitfield"] = "property"


def can_read(user, claim, t):
    """Caldwell's rule, asked of claims-core's authorization service at time t (minutes after midnight)."""
    v = claims[claim]
    if v["restricted_0200"] or (v["flagged_at"] is not None and v["flagged_at"] <= t):
        return False
    return v["unit"] == adjusters[user]


queries = []
for q in range(600):
    user = rng.choice(sorted(adjusters))
    t = rng.randint(8 * 60, 17 * 60)
    same = [c for c in view if claims[c]["unit"] == adjusters[user]]
    other = [c for c in view if claims[c]["unit"] != adjusters[user]]
    results = rng.sample(same, 4) + ([rng.choice(other)] if rng.random() < 0.15 else rng.sample(same, 1))
    queries.append((user, t, results))

# design A: the service account svc-nl-claims-ro retrieves and returns
returned = sum(len(r) for _, _, r in queries)
bad_unit = sum(1 for u, t, r in queries for c in r if claims[c]["unit"] != adjusters[u])
bad_flag = sum(1 for u, t, r in queries for c in r if claims[c]["unit"] == adjusters[u]
               and claims[c]["flagged_at"] is not None and claims[c]["flagged_at"] <= t)
print("Design A: svc-nl-claims-ro retrieves and returns (the service account's rights decide)")
print(f"  searches {len(queries)}, results returned {returned}")
print(f"  results the adjuster may not read: {bad_unit + bad_flag} ({100 * (bad_unit + bad_flag) / returned:.1f}%)")
print(f"    other unit's claim file: {bad_unit}")
print(f"    flagged after the 02:00 view was built: {bad_flag}")

# design B: retrieve under the service account, release under the user's delegation, rechecked at return
log = AuditLog("Caldwell security operations")
gate = RightsGate(can_read, log)
rel = held = leaked = 0
for u, t, r in queries:
    d = Delegation(u, "nl-assist", "claim search", ("claims:read",), t, t + 15)
    a, b = gate.release(d, r, t + 1)
    rel += len(a); held += len(b)
    leaked += sum(1 for c in a if not can_read(u, c, t + 1))
print("\nDesign B: on-behalf-of delegation, rights rechecked with claims-core before return")
print(f"  results released {rel}, withheld {held}, released that the adjuster may not read: "
      f"{leaked}")
print(f"  withheld records in Caldwell's log: {len(log.query(kind='rights-recheck'))}, "
      f"each with user, agent, purpose and reason")
w = [x for x in log.records if x["user"] == "twhitfield"][:2]
for x in w:
    print(f"  e.g. seq {x['seq']}: user {x['user']} agent {x['agent']} {x['resource']} {x['action']} ({x['reason']})")
print(f"  recheck calls to claims-core: {returned}  (one per result, about {returned / 9 / 60:.1f} per minute)")
