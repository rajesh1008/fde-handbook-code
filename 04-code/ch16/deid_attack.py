"""Listing 16.8: de-identification that holds against re-identification, tested by attacking it.

Release: the 200 documents' text plus a structured table (loss date, town, loss type) for the regression slice.
Attack 1: a known-value scan for identifiers the pattern scrub missed. Attack 2: k-anonymity on the table.
Attack 3: link the table to a stand-in public police blotter (date, town, incident type, name) and count unique
matches. Version 1 is the pattern scrub with the exact dates and towns; version 2 adds the known-value scrub,
a per-claim date shift reported as month only, town generalized to county, and suppression of groups under k."""
import random
import re
from collections import Counter
import _paths  # noqa: F401
from standin_sample import sample
from claimsgen import FIRST, LAST, TOWNS
from fieldkit.deid import (scrub_patterns, scrub_known, known_value_scan, k_anonymity, linkage_attack,
                           shift_days, ReleaseCheck)

K = 5
COUNTY = {t: "Hartford County" for t in TOWNS}
COUNTY.update({"Middletown": "Middlesex County", "Meriden": "New Haven County"})
real = sample()


def known(d):
    g = d["gold"]
    street = (g["loss_location"] or "").split(",")[0]
    return {"policy": g["policy_number"], "claimant_name": g["claimant_name"], "other_party_name": g["other_party"],
            "police_ref": g["police_report_ref"], "street": street if re.match(r"\d", street) else None}


def town(d):
    loc = d["gold"]["loss_location"]
    return loc.rsplit(", ", 1)[-1] if loc else None


rows = [dict(i=i, loss_date=d["gold"]["loss_date"], town=town(d), loss_type=d["gold"]["loss_type"], claim=d["id"])
        for i, d in enumerate(real) if town(d) and d["gold"]["loss_date"]]

# a stand-in public blotter: every police-attended loss in the sample, plus 400 unrelated entries
rng = random.Random(1616)
public = [dict(loss_date=real[r["i"]]["gold"]["loss_date"], town=r["town"], loss_type=r["loss_type"],
               identity=real[r["i"]]["gold"]["claimant_name"]) for r in rows if real[r["i"]]["gold"]["police_report_ref"]]
for _ in range(400):
    public.append(dict(loss_date=f"2026-0{rng.randint(1, 8)}-{rng.randint(1, 28):02d}", town=rng.choice(TOWNS),
                       loss_type=rng.choice(["AUTO-COLL", "PROP-THEFT", "AUTO-COMP"]),
                       identity=f"{rng.choice(FIRST)} {rng.choice(LAST)}"))


def check(texts, table, keys, label):
    leaks = sum(1 for d, t in zip(real, texts) if known_value_scan(t, known(d)))
    kmin, sizes = k_anonymity(table, keys)
    linked = linkage_attack(table, public, keys)
    rc = ReleaseCheck(leaks, len(texts), kmin, K, len(linked))
    print(label)
    print(rc.render())
    small = sum(n * c for n, c in sizes.items() if n < K)
    print(f"  rows in groups smaller than k: {small} of {len(table)}")
    return rc, leaks


# version 1
t1 = [scrub_patterns(d["text"]) for d in real]
rc1, _ = check(t1, rows, ["loss_date", "town", "loss_type"], "v1: pattern scrub, exact loss date and town")
kinds = Counter()
for d, t in zip(real, t1):
    for lab in {lab for lab, _v in known_value_scan(t, known(d))}:
        kinds[lab] += 1
print("  documents leaking each kind: " + ", ".join(f"{k} {v}" for k, v in kinds.most_common()))
for d, t in zip(real, t1):
    pol = known(d)["policy"]
    bent = [x for x in t.splitlines() if pol and known_value_scan(x, {"policy": pol})]
    if bent:
        print(f"  example ({d['id']}, policy {pol}): {bent[0].strip()[:80]}")
        break

# version 2
t2 = [scrub_known(scrub_patterns(d["text"]), known(d)) for d in real]
SECRET = "held-by-caldwell-privacy-office"   # the shift key never leaves Caldwell


def generalize(r, grain, shift=True):
    y, m, dd = (int(x) for x in r["loss_date"].split("-"))
    s = shift_days(r.get("claim", r["loss_date"]), SECRET) if shift else 0
    m2 = max(1, min(12, m + (1 if dd + s > 28 else -1 if dd + s < 1 else 0)))
    when = f"2026-{m2:02d}" if grain == "month" else f"2026-Q{(m2 - 1) // 3 + 1}" if grain == "quarter" else "dropped"
    return dict(loss_date=when, town=COUNTY[r["town"]], loss_type=r["loss_type"])


print("v2 options for the structured table (k=5): rows suppressed out of", len(rows))
best = None
for grain, keys in (("month", ["loss_date", "town", "loss_type"]), ("quarter", ["loss_date", "town", "loss_type"]),
                    ("quarter", ["loss_date", "loss_type"]), ("no date", ["town", "loss_type"])):
    gen = [generalize(r, grain) for r in rows]
    groups = Counter(tuple(g[k] for k in keys) for g in gen)
    kept = [g for g in gen if groups[tuple(g[k] for k in keys)] >= K]
    print(f"  {grain:<8} {'+'.join(k.replace('_', ' ') for k in keys):<28} suppressed {len(gen) - len(kept)}")
    if best is None or len(kept) > len(best[2]):
        best = (grain, keys, kept)
grain, keys, kept = best
public2 = [dict(generalize(p, grain, shift=False), identity=p["identity"]) for p in public]
public, public_raw = public2, public
print(f"  chosen: {grain}, {' + '.join(k.replace('_', ' ') for k in keys)} (the regression slice does not need a date)")
rc2, _ = check(t2, kept, keys, "v2: known-value scrub plus the chosen table; the attacker generalizes the blotter the same way")
