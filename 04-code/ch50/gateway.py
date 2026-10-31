"""Listing 50.6b: every model call goes through the bank's model gateway. Audits a call trace for route, pinned
version and streaming (CL-17: the gateway does not stream). Lab-local; deterministic stand-in traces."""
import sys
GATEWAY = "hl-gateway.internal/v1"
INVENTORY = {"H03": "layout-2026-06", "H05": "general-2026-07", "H08": "general-2026-07", "H10": "general-2026-07",
             "H11": "general-2026-07", "H12": "general-2026-07", "H09": "embed-2026-03"}
TRACES = {
    "build (day 118)": [("H03", GATEWAY, "layout-2026-06", False), ("H05", GATEWAY, "general-2026-07", False),
                        ("H08", GATEWAY, "general-2026-07", False), ("H10", GATEWAY, "general-2026-07", False),
                        ("H11", GATEWAY, "general-2026-07", True), ("H12", "api.provider.example/v1", "general-latest", False),
                        ("H09", GATEWAY, "embed-2026-03", False)],
    "go-live (day 171)": [(c, GATEWAY, v, False) for c, v in INVENTORY.items()],
}


def audit(trace):
    out = []
    for cid, route, version, stream in trace:
        p = []
        if route != GATEWAY:
            p.append(f"bypasses the gateway ({route})")
        if version != INVENTORY[cid]:
            p.append(f"version {version} is not the inventoried {INVENTORY[cid]}")
        if stream:
            p.append("requests streaming; the gateway does not stream (CL-17)")
        out.append((cid, p))
    return out


if __name__ == "__main__":
    for name, tr in TRACES.items():
        res = audit(tr)
        bad = [r for r in res if r[1]]
        print(f"{name}: {len(tr)} calls, {len(bad)} findings")
        for cid, p in bad:
            print(f"  {cid}: " + "; ".join(p))
