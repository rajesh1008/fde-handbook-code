"""Who pays for the integration tax, and for one more month, in each home.

Reference engagement: Caldwell-sized, from the Chapter 2 field estimate
(700 model hours, integration tax 1.2, so 840 integration hours; 175 FDE hours
in a month; loaded cost 150 dollars an FDE hour). The vendor rows reuse the
Chapter 2 lab unchanged. Integrator bill rate, lab share and consumption are
illustrative assumptions, labeled as such in the output.
"""
from __future__ import annotations

import pathlib
import sys
from dataclasses import dataclass

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "ch02"))
from contracts import CONTRACTS, FIELD_ESTIMATE  # noqa: E402  (Chapter 2 lab)
from margin import pilot_month_cost  # noqa: E402

LOADED = 150.0            # dollars per FDE hour, all homes (isolates the incentive)
BILL_RATE = 240.0         # integrator and partner bill rate, dollars an hour (illustrative)
LAB_SHARE = 0.25          # share of integration hours the lab's own FDEs carry (illustrative)
LAB_CONSUMPTION = 40_000  # lab revenue a month once in production (illustrative)


@dataclass(frozen=True)
class Split:
    home: str
    customer_pays: float      # cash out of the customer for these hours
    employer_cost: float      # the FDE's employer, loaded cost
    employer_revenue: float   # what the employer bills for these hours
    partner_net: float = 0.0  # a third party's margin on its share
    deferred: float = 0.0     # employer revenue pushed out by the month (extra-month only)

    @property
    def employer_net(self) -> float:
        return self.employer_revenue - self.employer_cost - self.deferred


def reference_hours():
    p = FIELD_ESTIMATE["caldwell"]
    return p.model_h, p.integration_h


def integration_tax_split(hours: float) -> list[Split]:
    lab_h, partner_h = hours * LAB_SHARE, hours * (1 - LAB_SHARE)
    return [
        Split("vendor, fixed fee", 0.0, hours * LOADED, 0.0),
        Split("integrator, T&M", hours * BILL_RATE, hours * LOADED, hours * BILL_RATE),
        Split("lab + partner", partner_h * BILL_RATE, lab_h * LOADED, 0.0,
              partner_net=partner_h * (BILL_RATE - LOADED)),
    ]


def extra_month_split() -> list[Split]:
    c, p = CONTRACTS["caldwell"], FIELD_ESTIMATE["caldwell"]
    d = pilot_month_cost(c, p)            # Chapter 2: 175 h, 26,250 + 3,000 run
    h = d["fde_hours"]
    g = pilot_month_cost(CONTRACTS["greystone"], FIELD_ESTIMATE["greystone"])
    lab_h, partner_h = h * LAB_SHARE, h * (1 - LAB_SHARE)
    return [
        Split("vendor, fixed fee (Caldwell)", 0.0, d["fde_cost"] + d["run"], 0.0),
        Split("vendor, subscription at production (Greystone)", 0.0,
              g["fde_cost"] + g["run"], 0.0, deferred=g["deferred_subscription"]),
        Split("integrator, T&M", h * BILL_RATE, h * LOADED, h * BILL_RATE),
        Split("lab + partner", partner_h * BILL_RATE, lab_h * LOADED, 0.0,
              partner_net=partner_h * (BILL_RATE - LOADED), deferred=LAB_CONSUMPTION),
    ]


def _table(rows: list[Split]):
    print(f"  {'home':<48}{'customer $':>11}{'employer cost $':>16}{'employer net $':>15}{'partner net $':>14}")
    for r in rows:
        print(f"  {r.home:<48}{r.customer_pays:>11,.0f}{r.employer_cost:>16,.0f}"
              f"{r.employer_net:>15,.0f}{r.partner_net:>14,.0f}")


def main():
    m, i = reference_hours()
    print(f"WHO PAYS THE INTEGRATION TAX  ({m:.0f} model h x tax {i/m:.1f} = {i:.0f} integration h;"
          f" loaded ${LOADED:.0f}/h)")
    _table(integration_tax_split(i))
    print("ONE MORE MONTH BEFORE PRODUCTION  (Caldwell staffing, 175 FDE h; Greystone row from Ch2)")
    _table(extra_month_split())
    print(f"illustrative: bill rate ${BILL_RATE:.0f}/h, lab share {LAB_SHARE:.0%},"
          f" lab consumption ${LAB_CONSUMPTION:,.0f}/month; vendor rows reuse 04-code/ch02")
    print("sign of one more month for the employer: vendor -, integrator +, lab -")


if __name__ == "__main__":
    main()
