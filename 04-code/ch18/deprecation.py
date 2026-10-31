"""The endpoint that was being decommissioned: Deprecation and Sunset headers as a register.

Deterministic stand-in. The platform added the headers to the v1 path on day 69 and set the sunset to
day 118; the documentation page still shows v1. One call a day is enough to find it.
"""
import _paths  # noqa: F401
from fieldkit.gateway import GatewayAdapter, GatewayStop, DAY
from gateway_sim import SimGateway, SecretStore, Clock, fmt
from naive_adapter import NaiveAdapter

clock, store = Clock(68 * DAY), SecretStore()
gw = SimGateway(clock, store, v1_deprecated_day=69, v1_sunset_day=118, rotate=False)
kw = dict(app_id="nl-shadow", api_version="2025-04-01", clock=clock.now, sleep=clock.sleep, source_ip="10.20.4.17")
ad, naive = GatewayAdapter(gw, store.read, **kw), NaiveAdapter(gw, store.read, **kw)
V1 = "/v1/deployments/extract-standard/chat"
for day in (68, 69, 70, 88, 100, 112, 118):
    clock.t = day * DAY + 10 * 3600
    try:
        ad.call("extract-standard", {"doc": day}, path=V1)
        status = "200"
    except GatewayStop as e:
        status = f"stopped ({e.kind})"
    try:
        naive.call("extract-standard", {"doc": day}, path=V1)
        nstatus = "200"
    except RuntimeError as e:
        nstatus = str(e).split(": ", 1)[1]
    rep = ad.deprecations.report(clock.t)
    line = "no headers" if not rep else f"{rep[0][1]} days left, level {rep[0][2]}, successor {rep[0][3]}"
    print(f"{fmt(clock.t)}  fieldkit {status:<18} naive {nstatus:<28} register: {line}")
