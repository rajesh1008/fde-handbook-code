"""Greystone Health, day 89: the environment design under Sam Oakley's review, with the managed-service provider.

Azure subscription approved day 76. Four checks, four required changes. Deterministic stand-in: the design is
written as data; no Azure resource is read."""
import _paths  # noqa: F401
from fieldkit.environment import Answer, EgressPolicy, EgressRule, EnvironmentDoc, KeyRecord, key_findings

G = "Greystone"
design = dict(
    identity=KeyRecord("nl-ambulatory app registration secret", "Northlight", G, "Northlight CI variables", 730,
                       "runner sign-in to Greystone's tenant"),
    egress=[EgressRule("model", "*.openai.azure.com", owner="Erin Walsh (Greystone)", reason="model endpoint"),
            EgressRule("keyvault", "kv-nl-amb.vault.azure.net", owner="Erin Walsh (Greystone)", reason="secrets")],
    dns_zone=("privatelink.openai.azure.com", "created by the template in Greystone's subscription"),
    release=("draft letters", "app identity", None),       # (output, released under, recheck against)
)
changes = []
for f in key_findings([design["identity"]], G):
    changes.append(("identity", f, "use a managed identity in Greystone's tenant; no secret exists to hold",
                    "Sam Oakley"))
for f in EgressPolicy("nl-ambulatory", design["egress"]).lint():
    changes.append(("network", f, "allow the one private endpoint by name, through the provider's change process",
                    "managed-service provider"))
zone, how = design["dns_zone"]
changes.append(("network", f"private DNS zone {zone} {how}",
                "link to the provider's hub zone; the template creates no DNS", "managed-service provider"))
out, under, recheck = design["release"]
if recheck is None:
    changes.append(("identity", f"{out} released under the {under}, no recheck of the coordinator's clinics",
                    "on-behalf-of the coordinator; recheck clinic access in the EHR before release", "Michael Hart"))

doc = EnvironmentDoc(G, "Northlight", [
    Answer(q, p, "Greystone subscription, centralus; readers: three named; retention 120 days", "subscription grh-nl-amb", G)
    for q in ("where", "identity", "logs") for p in ("production", "pre-production")])
print(f"three-questions lint: {len(doc.lint())} findings (logs moved to Greystone's workspace, Chapter 16)")
print(f"review result, day 89: CHANGES REQUIRED ({len(changes)})")
for i, (area, finding, fix, who) in enumerate(changes, 1):
    print(f"  {i}. [{area}] {finding}\n     change: {fix}\n     signs off: {who}")
