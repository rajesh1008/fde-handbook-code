"""Playbook fit: does a play written in one home survive in another?

A play names the assets it requires and, if it depends on it, the sign of one
more month that it assumes. fit() returns one of four verdicts:
  OK       every required asset is present and the duration assumption holds
  BENT     a required asset is missing but the home has a named substitute
  BREAKS   a required asset is missing and nothing substitutes for it
  INVERTS  the play assumes the opposite incentive from the home's (on one more
           month of engagement, or on one more custom feature)
"""
from __future__ import annotations

from dataclasses import dataclass, field

from homes import HOMES, Home


@dataclass(frozen=True)
class Play:
    key: str
    text: str
    requires: frozenset = frozenset()
    assumes: tuple = ()                       # (("month"|"custom", sign), ...)
    substitutes: dict = field(default_factory=dict)  # missing asset -> substitute assets


@dataclass(frozen=True)
class Fit:
    play: Play
    verdict: str
    reason: str


def P(key, text, requires=(), assumes=(), substitutes=None):
    return Play(key, text, frozenset(requires), tuple(assumes), substitutes or {})


# Northlight AI's FDE playbook, version 1 (a product vendor's playbook)
VENDOR_PLAYBOOK = [
    P("configure-first", "map every requirement to native product configuration before writing code",
      ["product"], substitutes={"product": ("method_library", "reference_impls")}),
    P("gap-to-backlog", "file each missing capability in the product backlog with a reproduction",
      ["product_backlog"], substitutes={"product_backlog": ("method_library", "research_team")}),
    P("defend-roadmap", "decline custom features only one customer will use",
      ["product"], assumes=[("custom", -1)]),
    P("absorb-tax", "absorb integration hours in the services fee and recover them at renewal",
      ["subscription"]),
    P("keep-it-short", "staff to reach production fast; every month costs margin",
      assumes=[("month", -1)]),
    P("release-train", "ship field fixes on the product's release train",
      ["release_train"]),
    P("handover-support", "hand over to product support after the Live Stable gate",
      ["support_org"], substitutes={"support_org": ("run_service", "partner_network")}),
    P("deterministic-first", "deterministic first, model last"),
    P("in-boundary", "run inside the customer's boundary, under their controls",
      ["in_boundary_deploy"], substitutes={"in_boundary_deploy": ("partner_network",)}),
    P("price-from-ledger", "price the next deal from the hours ledger, not the deal sheet",
      ["hours_ledger"]),
]

# The integrator's translation of the same intents (the repair after the failure injection)
INTEGRATOR_PLAYBOOK = [
    P("configure-first", "map every requirement to the customer's platform services before writing code",
      ["platform_neutrality"]),
    P("gap-to-library", "file each reusable fix in the method library, client IP removed",
      ["method_library"]),
    P("scope-custom", "price custom features as change requests with an owner and an exit",
      ["billable_hours", "change_mgmt"], assumes=[("custom", +1)]),
    P("bill-tax", "estimate integration hours in the statement of work and bill them",
      ["billable_hours"]),
    P("cap-duration", "write an exit date and a hand-over gate into the statement of work",
      ["change_mgmt"]),
    P("customer-release", "ship on the customer's change calendar",
      ["change_mgmt"]),
    P("handover-run", "hand over to the customer's team or a priced run service",
      ["run_service"]),
    P("deterministic-first", "deterministic first, model last"),
    P("in-boundary", "run inside the customer's boundary, under their controls",
      ["in_boundary_deploy"]),
    P("price-from-ledger", "price the next deal from the hours ledger, not the deal sheet",
      ["hours_ledger"]),
]


def fit(play: Play, home: Home) -> Fit:
    for what, sign in play.assumes:
        actual = home.duration_sign if what == "month" else home.custom_sign
        if sign != actual:
            noun = "month" if what == "month" else "custom feature"
            want, got = ("costs", "earns") if sign < 0 else ("earns", "costs")
            return Fit(play, "INVERTS", f"assumes one more {noun} {want}; here it {got}")
    missing = sorted(play.requires - home.assets)
    if not missing:
        return Fit(play, "OK", "assets present")
    subs = {m: next((s for s in play.substitutes.get(m, ()) if s in home.assets), None)
            for m in missing}
    if all(subs.values()):
        return Fit(play, "BENT", "; ".join(f"no {m}, use {s}" for m, s in subs.items()))
    return Fit(play, "BREAKS", "no " + ", no ".join(missing))


def run(playbook, home: Home) -> list[Fit]:
    return [fit(p, home) for p in playbook]


def tally(fits):
    out = {"OK": 0, "BENT": 0, "BREAKS": 0, "INVERTS": 0}
    for f in fits:
        out[f.verdict] += 1
    return out


def report(title, playbook, home):
    fits = run(playbook, home)
    print(f"{title}  (run by: {home.name})")
    for f in fits:
        print(f"  {f.verdict:<8}{f.play.key:<21}{f.reason}")
    t = tally(fits)
    print("  tally: " + "  ".join(f"{k} {v}" for k, v in t.items()))
    return fits


def main():
    for k in ("vendor", "lab"):
        report("NORTHLIGHT PLAYBOOK v1", VENDOR_PLAYBOOK, HOMES[k])


if __name__ == "__main__":
    main()
