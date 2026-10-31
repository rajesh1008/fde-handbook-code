"""Model versions you do not choose: the alias moves on day 77, and the aggregate hides the flips.

Deterministic stand-in: a 200-item gold set; correctness per item per version comes from a hash, not
from a model. The served-version ledger is real fieldkit code reading the gateway's version header.
"""
import _paths  # noqa: F401
from collections import Counter
from fieldkit.gateway import GatewayAdapter, DAY
from gateway_sim import SimGateway, SecretStore, Clock, fmt, h01

clock, store = Clock(76 * DAY), SecretStore()
gw = SimGateway(clock, store, alias_switch_day=77)
ad = GatewayAdapter(gw, store.read, app_id="nl-shadow", api_version="2025-04-01", clock=clock.now,
                    sleep=clock.sleep, source_ip="10.20.4.17", expected_versions={"extract-standard": "extract-2026-01"})
for hour in range(0, 48, 6):
    clock.t = 76 * DAY + hour * 3600
    ad.call("extract-standard", {"doc": hour})
for t, dep, old, new in ad.versions.changes:
    print(f"ledger: {fmt(t)} {dep} served {new} (was {old}); nobody announced it")

FIELDS = ["claim number", "policy number", "date of loss", "loss type", "total-loss flag"]


def correct(item, version):
    a = h01("A", item) < 0.92
    if version == "extract-2026-01":
        return a
    return (h01("lose", item) >= 0.06) if a else (h01("gain", item) < 0.78)


items = range(200)
old = sum(correct(i, "extract-2026-01") for i in items)
new = sum(correct(i, "extract-2026-04") for i in items)
cells = Counter((correct(i, "extract-2026-01"), correct(i, "extract-2026-04")) for i in items)
lost = Counter(FIELDS[int(h01("field", i) * 5)] for i in items
               if correct(i, "extract-2026-01") and not correct(i, "extract-2026-04"))
print(f"gold set 200 items: old version {old} correct ({old / 2:.1f}%), new version {new} ({new / 2:.1f}%)")
print(f"both correct {cells[(True, True)]}, gained {cells[(False, True)]}, lost {cells[(True, False)]}, "
      f"both wrong {cells[(False, False)]}")
print("lost items by field: " + ", ".join(f"{k} {v}" for k, v in lost.most_common()))
