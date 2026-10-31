"""Listing 20.x: the injected failure. Pennant's EU documents must stay in the EU region, which does not
offer the version validated in the US. An unpinned deployment passes its suite on a different model."""
import _paths  # noqa: F401
from collections import Counter
from deploy import deploy
from estate_configs import PENNANT_US, PENNANT_EU, GREYSTONE, with_
from fieldkit.estates import ModelPin, VersionUnavailable, resolve_pin
from sim_clouds import LAG, NOW, catalog, items, extract, FIELDS, FAMILY

PASS_LINE = 0.85
print(f"--- where extract-2026-04 is offered, {NOW} days after its first release (stand-in catalog) ---")
for cloud, regions in LAG.items():
    for region, vs in regions.items():
        lag = vs["extract-2026-04"]
        print(f"{cloud:6s} {region:13s} {'not offered' if lag is None else f'offered from day {lag}':20s}"
              f" latest here: {max(catalog(cloud)[region][FAMILY])}")

print("--- the naive deployment: Pennant EU project, model 'extract@latest' ---")
ev, rep, _ = deploy(with_(PENNANT_EU, model="extract@latest"))
verdict = "PASS" if rep["accuracy"] >= PASS_LINE else "FAIL"
print(f"suite report: field accuracy {rep['accuracy']:.1%} on {rep['attempted']} EU-lane documents "
      f"(pass line {PASS_LINE:.0%})  {verdict}")
print(f"what the report did not print: served versions {dict(rep['served'])}")
us_ev, us, _ = deploy(PENNANT_US)
print(f"validated in us-central1 on extract-2026-04: {us['accuracy']:.1%} on the US-lane gold set")

print("--- the comparison you are allowed to run: 200 synthetic EU-lane documents, both versions ---")
syn = items("pennant", 200, "synthetic")
acc, ok = {}, {}
for v in ("extract-2026-04", "extract-2026-01"):
    res = {i: extract("pennant", i, v) for i in syn}
    ok[v] = {i: {f: res[i][f] == f"{i}:{f}" for f in FIELDS["pennant"]} for i in syn}
    acc[v] = sum(sum(x.values()) for x in ok[v].values()) / (200 * len(FIELDS["pennant"]))
lost = Counter(f for i in syn for f in FIELDS["pennant"] if ok["extract-2026-04"][i][f] and not ok["extract-2026-01"][i][f])
gained = Counter(f for i in syn for f in FIELDS["pennant"] if ok["extract-2026-01"][i][f] and not ok["extract-2026-04"][i][f])
items_clean = {v: sum(all(ok[v][i].values()) for i in syn) for v in ok}
print(f"field accuracy  2026-04 {acc['extract-2026-04']:.1%}   2026-01 {acc['extract-2026-01']:.1%}")
print(f"documents with every field right  2026-04 {items_clean['extract-2026-04']}   2026-01 {items_clean['extract-2026-01']}")
print(f"field flips  lost {sum(lost.values())}  gained {sum(gained.values())}")
for f in FIELDS["pennant"]:
    print(f"  {f:12s} lost {lost[f]:3d}  gained {gained[f]:3d}")
hyp = sum(sum(v == f"{i}:{f}" for f, v in extract("pennant", i, "extract-2026-04").items())
          for i in items("pennant", 120, "eu")) / 960
print(f"stand-in only (not observable in the field): EU gold set on 2026-04 would score {hyp:.1%}")

print("--- fieldkit: resolve the pin before deploying ---")
try:
    resolve_pin(PENNANT_EU["pin"], catalog("gcp"))
except VersionUnavailable as e:
    print(f"REFUSED: {e}")
    print(f"offered elsewhere: {', '.join(e.elsewhere)} (outside the residency rule P-02)")
    for name, what in e.options():
        print(f"  option {name:15s} {what}")
print("decision (Pennant, recorded): change the pin for the EU project to extract-2026-01, validated in region")
pin_eu = ModelPin("extract", "extract-2026-01", ("europe-west4",), "EU-lane gold set, in region")
print(f"resolve_pin -> {resolve_pin(pin_eu, catalog('gcp'))}")
ev2, rep2, _ = deploy(with_(PENNANT_EU, model="extract-2026-01", pin=pin_eu))
print(f"EU project on its own pin: {rep2['accuracy']:.1%}, served {dict(rep2['served'])}, pin matched on every call")

print("--- the same check at Greystone: the failover region ---")
print(f"primary {resolve_pin(GREYSTONE['pin'], catalog('azure'))}")
try:
    resolve_pin(ModelPin("extract", GREYSTONE["pin"].version, ("centralus",)), catalog("azure"))
except VersionUnavailable as e:
    print(f"failover only: REFUSED: {e}")
