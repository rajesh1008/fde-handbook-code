"""Where reusable field work goes in each home, and what closes it.

Six field fixes from Northlight's first month with its two new hires. Each is
routed three ways: as a product vendor (Northlight), an integrator and a lab
would route it. An item is closed only by the home's closing evidence, never by
a copy in a repository.
"""
from __future__ import annotations

from dataclasses import dataclass

from homes import HOMES


@dataclass(frozen=True)
class Fix:
    key: str
    customer: str
    what: str
    general: bool        # would a second customer use it?
    model_failure: bool  # is it a failure of the model rather than of the plumbing?
    accepted: bool       # Northlight product owner accepted it into the backlog by day 30
    released: bool       # shipped on the release train by day 30


FIXES = [
    Fix("layout-family", "Pennant Logistics", "carrier layout family detector (41 layouts -> 6 families)",
        True, False, True, False),
    Fix("referral-form", "Greystone Health", "new referral form type", True, False, True, True),
    Fix("sso-groups", "Greystone Health", "map customer directory groups to product roles", True, False, True, False),
    Fix("handwritten-dates", "Pennant Logistics", "handwritten delivery dates misread", False, True, False, False),
    Fix("fax-deskew", "Caldwell Mutual", "deskew fax pages before extraction", True, False, False, False),
    Fix("ledger-export", "Greystone Health", "export to the managed-service provider's ticket format", False, False, False, False),
]


def route(fix: Fix, home_key: str) -> tuple[str, str]:
    """Return (destination, status) for one fix in one home."""
    if home_key == "vendor":
        if not fix.general:
            if fix.model_failure:
                return "eval set + model choice review", "open: no upstream to send it to"
            return "engagement repo (custom code)", "open: support must carry it"
        if fix.released:
            return "product backlog", "closed: released"
        return "product backlog", "open: accepted, not released" if fix.accepted else "open: not accepted"
    if home_key == "integrator":
        if fix.general:
            return "method library", "open until reused on a second engagement"
        return "client deliverable", "closed at hand-over"
    if fix.model_failure:
        return "research feedback (eval case)", "open until the model team accepts it"
    return "partner or reference implementation", "outside the lab"


def main():
    print("REUSE ROUTING, DAY 30  (six field fixes x three homes)")
    for f in FIXES:
        print(f"  {f.key:<18}{f.customer}: {f.what}")
        for k in HOMES:
            dest, status = route(f, k)
            print(f"      {k:<11}{dest:<38}{status}")
    v = [route(f, "vendor")[1] for f in FIXES]
    print("NORTHLIGHT (vendor) DAY-30 COUNT")
    for label in ("closed: released", "open: accepted, not released", "open: not accepted",
                  "open: support must carry it", "open: no upstream to send it to"):
        print(f"  {label:<36}{v.count(label)}")


if __name__ == "__main__":
    main()
