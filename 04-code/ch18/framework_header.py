"""The error that only happened without the framework.

The provider SDK added api-version to every request. The plain call did not, so the gateway applied its
default (2024-06-01), which rejects response_format. A contract test pins the header, not the SDK.
"""
import _paths  # noqa: F401
from gateway_sim import SimGateway, SecretStore, Clock

clock, store = Clock(60 * 86400), SecretStore()
gw = SimGateway(clock, store)
key = store.read()[1]
body = {"doc": 1, "text": "claim", "response_format": {"type": "json_schema"}}
sdk_headers = {"authorization": f"Bearer {key}", "x-app-id": "nl-shadow", "api-version": "2025-04-01"}
plain_headers = {"authorization": f"Bearer {key}", "x-app-id": "nl-shadow"}
for name, h in (("through the SDK", sdk_headers), ("plain HTTP call", plain_headers)):
    r = gw("POST", "/v2/deployments/extract-standard/chat", h, body, "10.20.4.17", clock.now())
    print(f"{name:<16} -> {r.status} {r.body.get('error', 'ok')}")

CONTRACT = [("api-version present", lambda h: "api-version" in h),
            ("x-app-id present", lambda h: "x-app-id" in h),
            ("bearer key, not a query string", lambda h: h.get("authorization", "").startswith("Bearer "))]
for name, h in (("SDK headers", sdk_headers), ("plain headers", plain_headers)):
    fails = [c for c, test in CONTRACT if not test(h)]
    print(f"contract test, {name}: {'pass' if not fails else 'FAIL ' + '; '.join(fails)}")
