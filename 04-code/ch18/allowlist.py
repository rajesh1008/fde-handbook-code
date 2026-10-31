"""IP allowlists: a new build-runner address meets the gateway, naive retries against fieldkit's stop.

Deterministic stand-in for Pennant. The gateway raises a security alert at 100 denied requests per hour.
"""
import _paths  # noqa: F401
from fieldkit.gateway import GatewayAdapter, GatewayStop, ACTIONS
from gateway_sim import SimGateway, SecretStore, Clock
from naive_adapter import NaiveAdapter

for kind in ("naive", "fieldkit"):
    clock, store = Clock(40 * 86400), SecretStore()
    gw = SimGateway(clock, store, allowlist=("10.40.0.0/16", "34.120.8.0/24"))
    kw = dict(app_id="nl-ci", api_version="2025-04-01", clock=clock.now, sleep=clock.sleep, source_ip="34.120.9.17")
    ad = NaiveAdapter(gw, store.read, **kw) if kind == "naive" else GatewayAdapter(gw, store.read, **kw)
    stopped = None
    for test in range(40):
        try:
            ad.call("extract-standard", {"doc": test})
        except RuntimeError:
            continue
        except GatewayStop as e:
            stopped = e
            break
    alert = "security alert raised" if gw.denied >= 100 else "no alert"
    print(f"{kind:<9} denied requests {gw.denied:>3}; {alert}")
    if stopped:
        print(f"          stopped at first denial: {ACTIONS[stopped.kind]}")
        print("          ticket: source 34.120.9.17 (new CI runner) not in 10.40.0.0/16 or 34.120.8.0/24; owner: network")
