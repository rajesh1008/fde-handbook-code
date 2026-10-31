"""Listing 14.1 driver: the five-day fieldkit run at Greystone, days 15 to 19.

Each day produces a named output. The engagement repository (fieldkit v0, Chapter 3) holds the notes, decisions,
requests and evidence; the question bank, decision tree and scoping document are chapter-local modules.
Pass --no-fax to see the week as planned, before the coordinator's question on Friday morning.
"""
import sys

import _path  # noqa: F401
from fieldkit.engagement import EngagementRepo
from fieldkit.fixtures import greystone_tracker

import pipeline as pl
import projection as pj
import question_bank as qb
import scoping_doc as sd
from decision_tree import CLASSES, SHORT, split, share

PLAN = {
    15: ("Michael's room and the floor", "workflow walked at two clinics; backlog by referral type"),
    16: ("Sam's room", "controls answered; gate calendar with days"),
    17: ("the pipeline, step by step", "every step classified; Michael's allowed and refused list"),
    18: ("the scoping document", "draft with claim statuses; lint run"),
    19: ("read-back and signature", "signed scope, exclusions with owners, projected pilot day"),
}


def line(d, label, text):
    print(f"day {d} | {label:<9}| {text}")


def run(fax_found=True):
    repo = EngagementRepo("Greystone Health")
    tracker = greystone_tracker()
    print("Greystone Health: five days on site (days 15 to 19). Deterministic stand-in: no model calls.")
    print("Before Monday:", "; ".join(f"{r.key} {r.status}" for r in tracker.requests.values())
          if hasattr(tracker, "requests") else "")
    print(f"Question bank lint, Friday draft (day 12): {len(qb.lint(qb.DRAFT_DEFECTS))} problems in "
          f"{len(qb.DRAFT_DEFECTS)} questions; bank as taken on site: {len(qb.lint(qb.BANK))} problems in "
          f"{len(qb.BANK)} questions")
    print()
    for d in range(15, 20):
        room, out = PLAN[d]
        t = qb.tally(qb.BANK if fax_found else [q for q in qb.BANK if q.key not in ("S15",)], d)
        line(d, "room", room)
        line(d, "output", out)
        line(d, "bank", f"{t['answered']} of {t['asked']} answered; blocking open {t['blocking_open']}")
        if d == 15:
            repo.note(15, "Michael Hart", "fact", "Backlog 31 days, concentrated in specialty referrals needing "
                      "prior authorization.", source="Michael's room")
            repo.decision("scorer", "Who scores a draft as acceptable?", "Michael Hart", 15, 16)
        if d == 16:
            repo.decide("scorer", 16, "two coordinators from different clinics; Michael breaks ties")
            repo.note(16, "Sam Oakley", "fact", "Privacy board monthly; complete submissions ten days ahead.",
                      source="Sam's room")
            repo.request("arch-review", "Architecture Review slot", "Sam Oakley", 16, "requested",
                         blocks="network change, data")
            repo.measure("volume-2clinics", "Referrals received at two clinics, four days",
                         f"{pl.VOLUME['electronic']} electronic" + (f", {pl.VOLUME['fax']} fax" if fax_found else ""),
                         "referral coordinator", "two clinic tally sheets, days 15 to 18, 4 days", 18,
                         kind="stand-in", caveat="two of 140 clinics")
        if d == 17:
            sp = split(pl.ELECTRONIC)
            line(d, "tree", ", ".join(f"{SHORT[c]} {sp[c]}" for c in CLASSES) +
                 f"; deterministic {share(pl.ELECTRONIC):.0%}")
            drafts = sum(1 for s in pl.ELECTRONIC if s.michael == "draft only")
            line(d, "Michael", f"{drafts} steps draft only; {len(pl.REFUSED)} actions refused; "
                 f"{sum(1 for s in pl.ELECTRONIC if s.michael == 'allowed')} allowed as built")
            repo.decision("red-flags", "Written red-flag list per specialty", "Michael Hart", 17, 40)
        if d == 18:
            v03 = sd.draft_v03()
            problems = sd.lint(v03)
            line(d, "lint v0.3", f"{len(problems)} refusal{'' if len(problems) == 1 else 's'} in {len(v03)} lines")
            for pr in problems:
                print(f"         - {pr}")
        if d == 19:
            steps = pl.ELECTRONIC + (pl.FAX if fax_found else [])
            if fax_found:
                line(d, "09:40", "coordinator: 'Do the faxes count?' Fax path walked by 11:30.")
                repo.note(19, "referral coordinator", "finding", "Outside referrals arrive by fax to clinic inboxes "
                          "and are re-keyed; 38% of the two-clinic count.", source="read-back")
                repo.decision("fax-path", "Fax path: fund as release 2, move outside referrals to the portal, or both",
                              "VP ambulatory operations", 19, 33)
                line(d, "inventory", f"{len(pl.ELECTRONIC)} -> {len(steps)} steps; deterministic "
                     f"{share(pl.ELECTRONIC):.0%} -> {share(steps):.0%}")
            p = pj.project(pl.ELECTRONIC)
            inv = dict(electronic=pl.VOLUME["electronic"], fax=pl.VOLUME["fax"] if fax_found else 0,
                       steps_e=len(pl.ELECTRONIC), steps_f=len(pl.FAX),
                       det_e=split(pl.ELECTRONIC)[CLASSES[0]],
                       model_e=split(pl.ELECTRONIC)[CLASSES[2]] + split(pl.ELECTRONIC)[CLASSES[3]])
            doc = sd.signed_v10(p, inv)
            if not fax_found:
                doc = [c for c in doc if "fax" not in c.text.lower()]
            problems = sd.lint(doc)
            line(d, "lint v1.0", f"{len(problems)} refusal{'' if len(problems) == 1 else 's'} in {len(doc)} lines")
            line(d, "projected", f"data day {p['data']}, pilot day {p['pilot']} (critical path: {p['critical']}, "
                 f"slack {p['slack']} days)")
            line(d, "signed", "; ".join(s.split(":")[0] for s in sd.SIGNATURES))
        print()
    print("Engagement repo lint, day 19:", repo.lint(19) or "clean")
    print("Open decisions:", ", ".join(f"{x.key} (owner {x.owner}, due day {x.due_day})"
                                       for x in repo.decisions if x.status == "open"))
    return repo


if __name__ == "__main__":
    run(fax_found="--no-fax" not in sys.argv)
