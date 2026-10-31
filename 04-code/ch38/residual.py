"""Residual risk, in writing. A finding that stays open after the fixes becomes a residual risk only when the
customer's accountable person accepts it on paper with the compensating controls, a review day, the triggers
that void the acceptance, and the vendor's commitment. The register lint refuses anything less."""
import sys
from dataclasses import dataclass, field
import _paths  # noqa: F401
from fieldkit.security import is_person
import world as W

CUSTOMER = {"Sam Oakley", "Michael Hart", "Denise Alvarez", "Marcus Bell", "Erin Walsh"}


@dataclass
class Residual:
    id: str
    finding: str
    risk: str
    inherent: tuple          # (likelihood, impact) 1 to 5
    residual: tuple
    controls: list
    accepted_by: list        # customer people who sign
    vendor_owner: str
    review_day: int | None
    triggers: list = field(default_factory=list)
    signed_day: int | None = None

    def lint(self):
        p = []
        if not self.accepted_by or any(not is_person(n) for n in self.accepted_by):
            p.append(f"{self.id}: accepted by '{', '.join(self.accepted_by) or 'nobody'}', not a named person")
        elif not set(self.accepted_by) <= CUSTOMER:
            p.append(f"{self.id}: accepted by someone outside Greystone ({', '.join(set(self.accepted_by) - CUSTOMER)})")
        if self.review_day is None:
            p.append(f"{self.id}: no review day; an acceptance with no end date is a waiver")
        if not self.triggers:
            p.append(f"{self.id}: no trigger that voids the acceptance")
        if len(self.controls) < 2:
            p.append(f"{self.id}: fewer than two compensating controls")
        if self.residual[0] * self.residual[1] >= 12:
            p.append(f"{self.id}: residual score {self.residual[0] * self.residual[1]} is high; fix, do not accept")
        if not is_person(self.vendor_owner):
            p.append(f"{self.id}: vendor owner '{self.vendor_owner}' is not a person")
        return p


REGISTER = [
    Residual("RR-01", "F-13", "an instruction in a scanned letter changes a draft's summary wording",
             (4, 4), (2, 3),
             ["draft only, no write tools", "coordinator reads and edits every draft before copying",
              "draft label on every copy", "output guardrail flags drafts that differ from the source summary"],
             ["Sam Oakley", "Michael Hart"], "Sofia Brennan", 190,
             ["a draft with injected wording reaches a payer", "a new document channel, such as patient upload",
              "any write tool added", "attack success above 1 in 20 on the monthly rerun"], 129),
    Residual("RR-02", "F-21", "a westus3 outage stops drafting until a recorded model change runs in centralus",
             (2, 3), (2, 2),
             ["drafting pauses; referrals continue by hand", "outage drill EV-25", "recorded model change, owner Erin Walsh"],
             ["Sam Oakley", "Denise Alvarez"], "Callum Reid", 190,
             ["a pin offered in centralus", "an outage longer than two working days", "pilot scope beyond two clinics"], 129),
]

if __name__ == "__main__":
    for r in REGISTER:
        i, s = r.inherent[0] * r.inherent[1], r.residual[0] * r.residual[1]
        print(f"{r.id} ({r.finding}) {r.risk}")
        print(f"   inherent {r.inherent[0]}x{r.inherent[1]}={i}, residual {r.residual[0]}x{r.residual[1]}={s}; "
              f"accepted by {' and '.join(r.accepted_by)} day {r.signed_day}; vendor owner {r.vendor_owner}; review day {r.review_day}")
        print(f"   controls: {'; '.join(r.controls)}")
        print(f"   void if: {'; '.join(r.triggers)}")
    print(f"register lint: {sum(len(r.lint()) for r in REGISTER)} problems")
    if "--inject" in sys.argv:
        bad = Residual("RR-03", "F-19", "image links fetched by the panel", (3, 4), (3, 4),
                       ["panel renders text only"], ["Northlight security team"], "Callum Reid", None, [])
        print("first draft of an acceptance, as a vendor would write it:")
        for p in bad.lint():
            print(f"   {p}")
