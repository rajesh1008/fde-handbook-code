"""Infrastructure as code the customer can read: render each estate in the customer's own tool, scan it
with stand-ins for the customer's policy rules, and show why a repair loop must rescan everything."""
import _paths  # noqa: F401
LOGGED = {"storage_account", "log_sink", "runner"}
TAGS = {"owner", "cost-center", "data-class"}


def render(cfg):
    """The estate's resources as data. Names follow each cloud's resource types (abbreviated)."""
    c, key = cfg["cloud"], cfg["credential"] == "static_key"
    tags = {"owner": "northlight-fde", "cost-center": "cc-4410", "data-class": "restricted"}
    if not cfg["tags_complete"]:
        tags = {"owner": "northlight-fde"}
    diag = "customer" if cfg["diagnostics"] else None
    kinds = {"aws": [("identity", "aws_iam_role.suite_task"), ("endpoint", "aws_vpc_endpoint.gateway"),
                     ("log_sink", "aws_cloudwatch_log_group.suite"), ("runner", "aws_ecs_task_definition.suite")],
             "azure": [("identity", "userAssignedIdentities/suite"), ("endpoint", "privateEndpoints/pe-openai"),
                       ("storage_account", "storageAccounts/suitereports"), ("runner", "containerApps/jobs/suite")],
             "gcp": [("identity", "google_service_account.suite"), ("endpoint", "google_compute_forwarding_rule.psc"),
                     ("log_sink", "google_logging_project_sink.suite"), ("runner", "google_cloud_run_v2_job.suite")],
             "onprem": [("identity", "host.service_account"), ("endpoint", "lb.internal_inference"),
                        ("log_sink", "syslog.siem_forwarder"), ("runner", "systemd.suite_runner")]}[c]
    out = []
    for kind, name in kinds:
        r = dict(type=kind, name=name, region=cfg["region"], tags=dict(tags))
        if kind == "identity":
            r["key_based"] = key
        if kind in ("endpoint", "storage_account"):
            r["public_network_access"] = cfg["public_access"]
        if kind in LOGGED:
            r["diagnostics"] = diag
        out.append(r)
    return out


def rules(allowed):
    return [("public network access disabled", lambda r: not r.get("public_network_access", False)),
            ("diagnostics to the customer's log sink", lambda r: r["type"] not in LOGGED or r.get("diagnostics") == "customer"),
            ("required tags present", lambda r: TAGS <= set(r.get("tags", {}))),
            ("region inside the residency rule", lambda r: r.get("region") in allowed),
            ("no key-based credential", lambda r: not r.get("key_based", False))]


def scan(resources, allowed, only=None):
    found = []
    for name, ok in rules(allowed):
        if only is not None and name not in only:
            continue
        found += [(name, r["name"]) for r in resources if not ok(r)]
    return found


def fix(resources, finding):
    rule, name = finding
    out = []
    for r in resources:
        r = dict(r, tags=dict(r["tags"]))
        if r["name"] == name:
            if rule == "public network access disabled":
                # the "private storage" module swap: public access off, and its diagnostics block is gone
                r["public_network_access"] = False
                r.pop("diagnostics", None)
            elif rule == "required tags present":
                r["tags"].update({"cost-center": "cc-4410", "data-class": "restricted"})
            elif rule == "diagnostics to the customer's log sink":
                r["diagnostics"] = "customer"
        out.append(r)
    return out


def repair_loop(resources, allowed, full_rescan, max_iter=5):
    trace, failing = [], None
    for i in range(1, max_iter + 1):
        findings = scan(resources, allowed, only=None if (full_rescan or failing is None) else failing)
        trace.append((i, len(findings), sorted({f[0] for f in findings})))
        if not findings:
            break
        failing = {f[0] for f in findings}
        for f in findings:
            resources = fix(resources, f)
    return resources, trace


def to_text(cfg, resources):
    """A short excerpt in the customer's tool, so the reader sees what the customer's reviewers read."""
    r = next(x for x in resources if x["type"] in ("storage_account", "endpoint"))
    if cfg["iac"] == "bicep":
        return "\n".join([f"resource suitereports 'Microsoft.Storage/storageAccounts@2025-01-01' = {{",
                          f"  location: '{r['region']}'",
                          f"  properties: {{ publicNetworkAccess: '{'Enabled' if r.get('public_network_access') else 'Disabled'}' }}",
                          f"  tags: {r['tags']}", "}"])
    return "\n".join([f'resource "{r["name"].split(".")[0]}" "{r["name"].split(".")[1]}" {{',
                      f'  region              = "{r["region"]}"',
                      f'  model_pin           = "{cfg["pin"].version}"   # changed only by a recorded model change',
                      f'  public_access       = {str(r.get("public_network_access", False)).lower()}', "}"])


if __name__ == "__main__":
    from estate_configs import CALDWELL, GREYSTONE, PENNANT_EU, with_
    print("--- each estate rendered in the customer's own tool, scanned by the customer's rules (stand-ins) ---")
    for label, cfg in (("Caldwell / AWS / Terraform", CALDWELL), ("Greystone / Azure / Bicep", GREYSTONE),
                       ("Pennant EU / Google Cloud / Terraform", PENNANT_EU)):
        res = render(cfg)
        print(f"{label:40s} resources {len(res)}  findings {len(scan(res, cfg['allowed_regions']))}")
    g0 = with_(GREYSTONE, public_access=True, tags_complete=False)
    res = render(g0)
    print("--- Greystone, first render from Northlight's sandbox template ---")
    print(to_text(g0, res))
    for f in scan(res, g0["allowed_regions"]):
        print(f"  finding: {f[0]:40s} {f[1]}")
    for mode, full in (("rescan failing rules only", False), ("rescan every rule", True)):
        final, trace = repair_loop(res, g0["allowed_regions"], full)
        print(f"--- repair loop, {mode} ---")
        for i, n, names in trace:
            print(f"  iteration {i}: findings {n}  {', '.join(names) if names else 'clean'}")
        print(f"  declared clean at iteration {trace[-1][0]}; full scan of the result: "
              f"{len(scan(final, g0['allowed_regions']))} finding(s)")
    print("--- Pennant EU, the pin as the customer reads it ---")
    from fieldkit.estates import ModelPin
    eu = with_(PENNANT_EU, pin=ModelPin("extract", "extract-2026-01", ("europe-west4",), "EU-lane comparison, day 116"))
    print(to_text(eu, render(eu)))
