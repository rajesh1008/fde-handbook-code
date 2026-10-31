"""Deploy the evaluation suite to one estate and collect the evidence for the fourteen parity checks."""
import _paths  # noqa: F401
import suite
from adapters import ADAPTERS
from fieldkit.estates import Evidence, conformance, passed
from iac_check import render, scan
from sim_clouds import Credentials, Network, Sinks, items


def deploy(cfg):
    creds, sinks = Credentials(), Sinks()
    egress = tuple(cfg["egress_allow"]) + (("pypi.org",) if any("0.0.0.0/0" in c for c in cfg["console_changes"]) else ())
    net = Network(cfg["private_endpoint"], cfg["public_access"], egress)
    port = ADAPTERS[cfg["cloud"]](cfg, creds, net, sinks)
    ids = items(cfg["customer"], cfg["gold_n"], cfg.get("gold_tag", "gold"))
    rep = suite.run(port, cfg["customer"], ids, cfg["pin"].version, rotate_at=len(ids) // 2, rotate=creds.rotate)
    pr = port.probe()
    ev = Evidence(credential=cfg["credential"], secret_at_call=cfg["secret_at_call"],
                  rotation_ok=rep["failures"] == 0, region=cfg["region"], allowed_regions=cfg["allowed_regions"],
                  served=rep["served"], pinned=cfg["pin"].version, deprecations_red=getattr(port, "deprecations", 0),
                  foreign_log_records=len(sinks.vendor), calls=rep["calls"],
                  records_with_tokens=sum(1 for r in sinks.customer if r["tokens_in"] > 0),
                  suite_ran=rep["failures"] == 0 and len(sinks.customer) == rep["calls"] > 0,
                  scanner_findings=sorted({f[0] for f in scan(render(cfg), cfg["allowed_regions"])}),
                  drift=list(cfg["console_changes"]), **pr)
    return ev, rep, sinks


def check_line(cfg):
    ev, rep, _ = deploy(cfg)
    res = conformance(ev)
    return passed(res), [c for c, ok, _ in res if not ok], res, rep
