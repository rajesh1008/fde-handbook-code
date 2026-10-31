"""Listings 46.6 and 46.7: the claims-intake playbook harvested from Caldwell, and the transfer check.

Failure injection (mode 'naive'): the credit for reuse is taken for every step, including PB-04, which pulls
each claim's document list through a document API that only Caldwell's claims core has. Mode 'checked'
compares each step's prerequisites with the target customer's discovery inventory first.
"""
import sys
import _paths  # noqa: F401
from dataclasses import dataclass


@dataclass(frozen=True)
class Step:
    id: str
    name: str
    bucket: str
    caldwell_h: int        # hours the step took at Caldwell (ledger tags)
    replay_h: int          # hours to replay it where it transfers
    requires: tuple        # capabilities the step assumes the customer has

    @property
    def credit(self):
        return self.caldwell_h - self.replay_h


PLAYBOOK = [
    Step("PB-01", "discovery script and stakeholder map", "discovery", 80, 40, ()),
    Step("PB-02", "access checklist, questionnaire answers", "access", 140, 70, ("sso_groups",)),
    Step("PB-03", "gateway onboarding, 7-day key rotation", "integration", 110, 40, ("gateway_rotation_api",)),
    Step("PB-04", "document list via claims-core document API", "integration", 150, 30, ("claims_core_doc_api",)),
    Step("PB-05", "parsers for the loss-notice form family", "integration", 210, 90, ("loss_notice_forms",)),
    Step("PB-06", "exceptions queue mapping", "integration", 160, 100, ("exceptions_export",)),
    Step("PB-07", "evaluation suite and gold set", "model", 220, 120, ("two_adjudicators",)),
    Step("PB-08", "shadow sizing at 30 adjudications a day", "gates", 60, 20, ("adjudication_30_a_day",)),
    Step("PB-09", "five-gate evidence pack templates", "gates", 240, 140, ()),
    Step("PB-10", "hand-over runbooks and failure drill", "handover", 200, 120, ("customer_on_call",)),
]

INVENTORY = {   # what discovery found at each customer
    "caldwell":     {"sso_groups", "gateway_rotation_api", "claims_core_doc_api", "loss_notice_forms", "exceptions_export",
                     "two_adjudicators", "adjudication_30_a_day", "customer_on_call"},
    "greystone":    {"sso_groups", "two_adjudicators", "customer_on_call"},       # MSP change tickets, referrals, 12 a day
    "pennant":      {"sso_groups", "gateway_rotation_api", "exceptions_export"},
    "next insurer": {"sso_groups", "gateway_rotation_api", "loss_notice_forms", "exceptions_export", "two_adjudicators",
                     "adjudication_30_a_day", "customer_on_call"},                 # documents arrive as a nightly file export
}


def check(target, mode="checked"):
    have = INVENTORY[target]; rows = []
    for s in PLAYBOOK:
        missing = [r for r in s.requires if r not in have]
        ok = (mode == "naive") or not missing
        rows.append((s, ok, missing))
    return rows


def credit(target, mode="checked", bucket=None):
    return sum(s.credit for s, ok, _ in check(target, mode) if ok and (bucket is None or s.bucket == bucket))


def main(mode="checked", target="next insurer"):
    print(f"playbook claims-intake v1 (from Caldwell), target: {target}, mode: {mode}")
    for s, ok, missing in check(target, mode):
        flag = "transfers" if ok else "NO, needs " + ", ".join(missing)
        print(f"  {s.id} {s.name:<44} {s.credit:>4} h  {flag}")
    print(f"credit taken: {credit(target, mode):,} h (integration {credit(target, mode, 'integration'):,} h)")
    if mode == "naive":
        print("no prerequisite check: the price assumes every step replays as it did at Caldwell")
    if mode == "matrix":
        pass


def matrix():
    print("transfer matrix: steps that transfer, and the credit they carry")
    for t in INVENTORY:
        rows = check(t)
        print(f"  {t:<13} {sum(ok for _, ok, _ in rows):>2} of {len(rows)} steps   credit {credit(t):>4} h   "
              + " ".join(s.id[-2:] if ok else "--" for s, ok, _ in rows))


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "checked"
    if mode == "matrix":
        matrix()
    else:
        main(mode, sys.argv[2] if len(sys.argv) > 2 else "next insurer")
