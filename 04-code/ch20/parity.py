"""Listing 20.x: the fourteen parity checks on each estate, replayed through the deployment log."""
import _paths  # noqa: F401
from deploy import check_line
from estate_configs import CALDWELL, GREYSTONE, PENNANT_EU, with_
from fieldkit.estates import ModelPin, CHECKS

TIMELINE = {
    "Caldwell (AWS)": (CALDWELL, [(100, "reference deployment, the Chapter 18 configuration", {})]),
    "Pennant EU (Google Cloud)": (PENNANT_EU, [
        (102, "first deploy, copied from the Caldwell layout",
         dict(credential="person", region="us-central1", log_sink="vendor")),
        (106, "service account, Pennant log bucket, EU region, model left at latest",
         dict(credential="workload", region="europe-west4", log_sink="customer", model="extract@latest",
              console_changes=["egress rule 0.0.0.0/0 added in console"])),
        (109, "console rule removed through IaC; resolve_pin refuses 2026-04",
         dict(console_changes=[])),
        (116, "recorded model change: EU pin extract-2026-01, validated in region",
         dict(model="extract-2026-01", pin=ModelPin("extract", "extract-2026-01", ("europe-west4",), "EU gold, day 114"))),
    ]),
    "Greystone (Azure)": (GREYSTONE, [
        (113, "first deploy from Northlight's sandbox template",
         dict(credential="static_key", secret_at_call=False, public_access=True, tags_complete=False,
              api_version="2024-06-01")),
        (117, "managed identity; storage module swapped by the repair loop",
         dict(credential="workload", secret_at_call=True, public_access=False, tags_complete=True,
              api_version="2026-03-01", diagnostics=False, log_sink="none")),
        (120, "diagnostic settings restored to Greystone's workspace",
         dict(diagnostics=True, log_sink="customer")),
    ]),
}

if __name__ == "__main__":
    print("checks: " + "  ".join(c for c, _, _ in CHECKS))
    final = {}
    for estate, (cfg, events) in TIMELINE.items():
        print(f"--- {estate} ---")
        for day, what, change in events:
            cfg = with_(cfg, **change)
            n, failing, res, rep = check_line(cfg)
            print(f"day {day:3d}  {n:2d}/14  failing {' '.join(failing) or '-':22s} {what}")
        final[estate] = res
    print("--- final state, every check ---")
    for (cid, port, name) in CHECKS:
        cells = [next(d for c, ok, d in final[e] if c == cid) for e in final]
        flags = ["pass" if next(ok for c, ok, d in final[e] if c == cid) else "FAIL" for e in final]
        print(f"{cid} {name:50s} " + "  ".join(flags))
