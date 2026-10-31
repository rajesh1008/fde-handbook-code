"""The three estates as configuration the customer can read. Changing an estate means changing this,
and the IaC rendered from it, never the core."""
from fieldkit.estates import ModelPin

PIN = "extract-2026-04"
BASE = dict(credential="workload", secret_at_call=True, private_endpoint=True, public_access=False,
            log_sink="customer", diagnostics=True, tags_complete=True, api_version="2026-03-01", console_changes=[])

CALDWELL = dict(BASE, customer="caldwell", cloud="aws", iac="terraform", region="us-east-1",
                allowed_regions=("us-east-1", "us-west-2"), egress_allow=("gateway.caldwell.internal",),
                model=PIN, pin=ModelPin("extract", PIN, ("us-east-1", "us-west-2"), "Chapter 18 gold set, day 77"),
                gold_n=200)
GREYSTONE = dict(BASE, customer="greystone", cloud="azure", iac="bicep", region="westus3",
                 allowed_regions=("westus3", "centralus"), egress_allow=("login.greystone.internal",),
                 deployments={"nl-extract": PIN}, model="nl-extract",
                 pin=ModelPin("extract", PIN, ("westus3", "centralus"), "300-packet sample, day 112"), gold_n=300)
PENNANT_US = dict(BASE, customer="pennant", cloud="gcp", iac="terraform", project="pennant-docai-us",
                  region="us-central1", allowed_regions=("us-central1",), egress_allow=(), model=PIN,
                  pin=ModelPin("extract", PIN, ("us-central1",), "US-lane gold set"), gold_n=120)
PENNANT_EU = dict(PENNANT_US, project="pennant-docai-eu", region="europe-west4", allowed_regions=("europe-west4",),
                  pin=ModelPin("extract", PIN, ("europe-west4",), "US-lane gold set (not EU)"), gold_tag="eu")


def with_(cfg, **kw):
    d = dict(cfg)
    d.update(kw)
    return d
