"""The three signed contracts and two plans for each: the deal sheet Graham Lowell sold from, and the
field estimate Laura Finch's team builds once the work is itemized. Illustrative figures, labeled."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "fieldkit"))
from fieldkit.fixtures import CUSTOMERS
from margin import Contract, Plan

CONTRACTS = {
    "caldwell": Contract(CUSTOMERS["caldwell"]["name"], acv=1_600_000, billing="fixed", services_fee=200_000),
    "greystone": Contract(CUSTOMERS["greystone"]["name"], acv=2_400_000, billing="tm", bill_rate=260,
                          tm_cap=450_000, subscription_starts="production"),
    "pennant": Contract(CUSTOMERS["pennant"]["name"], acv=740_000, billing="fixed", services_fee=120_000),
}

DEAL_SHEET = {
    "caldwell": Plan("deal sheet", fde_fte=2.0, discovery_h=80, access_h=60, model_h=700, integration_tax=0.4,
                     gates_h=80, handover_h=60),
    "greystone": Plan("deal sheet", fde_fte=2.5, discovery_h=100, access_h=80, model_h=900, integration_tax=0.4,
                      gates_h=100, handover_h=80, run_pilot=4000, run_prod=12000),
    "pennant": Plan("deal sheet", fde_fte=1.5, discovery_h=60, access_h=40, model_h=500, integration_tax=0.5,
                    gates_h=50, handover_h=50, run_pilot=2500, run_prod=6000),
}

FIELD_ESTIMATE = {
    "caldwell": Plan("field estimate", fde_fte=2.5, discovery_h=220, access_h=260, model_h=700, integration_tax=1.2,
                     gates_h=380, handover_h=200, wait_months=1.5),
    "greystone": Plan("field estimate", fde_fte=3.0, discovery_h=260, access_h=420, model_h=900, integration_tax=1.0,
                      gates_h=560, handover_h=240, wait_months=3.0, run_pilot=4000, run_prod=12000),
    "pennant": Plan("field estimate", fde_fte=2.0, discovery_h=200, access_h=160, model_h=500, integration_tax=2.0,
                    gates_h=200, handover_h=160, wait_months=0.5, run_pilot=2500, run_prod=6000),
}
