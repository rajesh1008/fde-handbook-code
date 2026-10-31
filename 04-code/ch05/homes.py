"""The three homes for the FDE role as comparison data (Chapter 5).

Each Home records what does not bend, how the employer is paid, who pays for an
integration hour, where reusable field work goes and what closes it, how the
engagement ends, and which way one more month of engagement moves the employer's
P&L. All values are the chapter's model of each home, not a survey of any company.
"""
from __future__ import annotations

import pathlib
import sys
from dataclasses import dataclass

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "fieldkit"))
import fieldkit  # noqa: E402  (fieldkit 0.1.0, unchanged)
from fieldkit.fixtures import CUSTOMERS  # noqa: E402

assert fieldkit.__version__ == "0.1.0", fieldkit.__version__


@dataclass(frozen=True)
class Home:
    key: str
    name: str
    fixed: str                 # the thing that does not bend
    paid_by: str               # how the employer earns from the engagement
    tax_payer: str             # who pays for one integration hour
    reuse_route: str           # where reusable field work goes
    reuse_closes: str          # the evidence that closes a reuse item
    exit: str                  # how the engagement ends
    duration_sign: int         # +1: one more month earns the employer more; -1: it costs
    custom_sign: int           # +1: one more custom feature earns the employer more; -1: it costs
    rewarded: str              # what the employer measures the FDE on
    assets: frozenset          # what the home owns that a playbook may assume


VENDOR = Home(
    key="vendor", name="Product vendor",
    fixed="the product",
    paid_by="subscription, plus a fixed or capped services fee",
    tax_payer="the vendor's margin, recovered at renewal",
    reuse_route="product backlog",
    reuse_closes="a released feature used by a second customer",
    exit="Live Stable gate, then the vendor's product support",
    duration_sign=-1, custom_sign=-1,
    rewarded="time to production and renewal",
    assets=frozenset({"product", "product_backlog", "release_train", "support_org",
                      "subscription", "in_boundary_deploy", "hours_ledger"}),
)

INTEGRATOR = Home(
    key="integrator", name="Systems integrator",
    fixed="the customer's platform",
    paid_by="billable hours or a fixed-price statement of work",
    tax_payer="the customer, by the hour",
    reuse_route="method library and accelerators",
    reuse_closes="an asset reused on a second engagement, with the client's IP removed",
    exit="contract end, or a run-state managed service",
    duration_sign=+1, custom_sign=+1,
    rewarded="utilization, margin per hour and follow-on work",
    assets=frozenset({"method_library", "bench", "billable_hours", "change_mgmt",
                      "platform_neutrality", "run_service", "in_boundary_deploy",
                      "hours_ledger"}),
)

LAB = Home(
    key="lab", name="Model lab",
    fixed="the model",
    paid_by="a usage commitment and consumption",
    tax_payer="a partner, billed to the customer; the lab funds the first slice",
    reuse_route="research feedback, evals and reference implementations",
    reuse_closes="an eval case or failure accepted by the model team",
    exit="hand-over to the customer's team or a partner after the first use case",
    duration_sign=-1, custom_sign=-1,
    rewarded="consumption, flagship deployments and model feedback",
    assets=frozenset({"model", "research_team", "commitment", "partner_network",
                      "reference_impls", "hours_ledger"}),
)

HOMES = {h.key: h for h in (VENDOR, INTEGRATOR, LAB)}
NORTHLIGHT = VENDOR  # Northlight AI is a product vendor
CUSTOMER_NAMES = {k: v["name"] for k, v in CUSTOMERS.items()}

FIELDS = [("fixed", "what does not bend"), ("paid_by", "how the employer is paid"),
          ("tax_payer", "who pays an integration hour"), ("reuse_route", "where reuse goes"),
          ("reuse_closes", "what closes a reuse item"), ("exit", "how it ends"),
          ("rewarded", "what the FDE is measured on")]


def main():
    for attr, label in FIELDS:
        print(label.upper())
        for h in HOMES.values():
            print(f"  {h.name:<20}{getattr(h, attr)}")
    print("ONE MORE MONTH OF ENGAGEMENT")
    for h in HOMES.values():
        print(f"  {h.name:<20}{'earns the employer more' if h.duration_sign > 0 else 'costs the employer'}")


if __name__ == "__main__":
    main()
