"""Chapter 14: the Greystone scoping document as data, with a lint that refuses to sign.

Each line of the document is a Claim with one of the five statuses (Chapter 8 [CHECK ch08]). A line with a number
also carries a strip: measured, estimated or assumed. The lint encodes what Northlight will not sign:

    NO-STATUS         a line with no claim status
    NUMBER-NO-STRIP   a number with no measured / estimated / assumed strip
    DECISION-NO-OWNER a decision required with no named person
    DECISION-NO-DATE  a decision required with no due day
    UNBOUNDED-SCOPE   "all", "every" or "any" referrals in a scope line (scope is an inventory, not a quantifier)
    ACCURACY-NO-SCORER an accuracy or quality number with no named scorer
    DATE-NO-CALENDAR  a projected date that does not name the calendars it depends on
    EXCLUSION-NO-OWNER an out-of-scope line with nobody who owns what happens to it
    AUTONOMY-REFUSED  an autonomy line that gives the system an action Michael Hart refused on day 17
    UPGRADED-STATUS   a vendor position or proposed design carrying a "measured" strip
"""
from __future__ import annotations
import re
from dataclasses import dataclass, field

from question_bank import STATUSES

STRIPS = ("measured", "estimated", "assumed")
SECTIONS = ("scope", "out of scope", "success", "autonomy", "controls", "plan", "decisions")


@dataclass
class Claim:
    section: str
    text: str
    status: str = ""
    strip: str = ""
    owner: str = ""
    due_day: int | None = None
    scorer: str = ""
    depends: tuple = field(default_factory=tuple)


_NUM = re.compile(r"\b[Rr]elease \d\b")
REFUSED = re.compile(r"\bsubmits?\b|\bsets? urgency|\bdeclines?\b|\bmessages? (to )?patients?", re.I)
NEGATED = re.compile(r"\bnever\b|\bnot\b|\bno\b|\bdrafts?\b", re.I)


def lint(doc) -> list[str]:
    out = []
    for i, c in enumerate(doc, 1):
        tag = f"line {i:02d} [{c.section}]"
        if c.status not in STATUSES:
            out.append(f"NO-STATUS {tag}: {c.text}")
        if re.search(r"\d", _NUM.sub("", c.text)) and c.strip not in STRIPS:
            out.append(f"NUMBER-NO-STRIP {tag}: {c.text}")
        if c.status == "decision required" and not c.owner:
            out.append(f"DECISION-NO-OWNER {tag}: {c.text}")
        if c.status == "decision required" and c.due_day is None:
            out.append(f"DECISION-NO-DATE {tag}: {c.text}")
        if c.section == "scope" and re.search(r"\b(all|every|any)\b", c.text, re.I):
            out.append(f"UNBOUNDED-SCOPE {tag}: {c.text}")
        if re.search(r"accura|acceptable|quality", c.text, re.I) and re.search(r"\d", c.text) and not c.scorer:
            out.append(f"ACCURACY-NO-SCORER {tag}: {c.text}")
        if re.search(r"pilot (on|by) day|go-live", c.text, re.I) and not c.depends:
            out.append(f"DATE-NO-CALENDAR {tag}: {c.text}")
        if c.section == "out of scope" and not c.owner:
            out.append(f"EXCLUSION-NO-OWNER {tag}: {c.text}")
        if c.section == "autonomy" and REFUSED.search(c.text) and not NEGATED.search(c.text):
            out.append(f"AUTONOMY-REFUSED {tag}: {c.text}")
        if c.status in ("vendor position", "proposed design") and c.strip == "measured":
            out.append(f"UPGRADED-STATUS {tag}: {c.text}")
    return out


def render(doc, title: str, signatures=()) -> str:
    lines = [f"# {title}", ""]
    for sec in SECTIONS:
        rows = [c for c in doc if c.section == sec]
        if not rows:
            continue
        lines.append(f"## {sec}")
        for c in rows:
            meta = [c.status or "NO STATUS"]
            if c.strip:
                meta.append(c.strip)
            if c.owner:
                meta.append(f"owner {c.owner}")
            if c.due_day is not None:
                meta.append(f"due day {c.due_day}")
            if c.scorer:
                meta.append(f"scorer {c.scorer}")
            if c.depends:
                meta.append("depends on " + ", ".join(c.depends))
            lines.append(f"- {c.text} [{'; '.join(meta)}]")
        lines.append("")
    if signatures:
        lines.append("## signatures")
        lines += [f"- {s}" for s in signatures]
        lines.append("")
    return "\n".join(lines)


def status_mix(doc) -> dict:
    return {s: sum(1 for c in doc if c.status == s) for s in STATUSES}


DF, RA, VP, PD, DR = STATUSES
H, O, OPS = "Michael Hart", "Sam Oakley", "VP ambulatory operations"


def draft_v03():
    """Thursday night, day 18: what two tired engineers wrote first."""
    return [
        Claim("scope", "Release 1 automates referral intake for all referrals at Greystone clinics.", DF),
        Claim("scope", "Drafts prior-authorization letters and referral summaries for coordinators.", PD),
        Claim("success", "Draft accuracy of 90% or better.", PD, "assumed"),
        Claim("success", "Backlog falls from 31 days to under 10 days.", PD),
        Claim("autonomy", "The system submits routine prior-authorization requests.", PD),
        Claim("controls", "All processing stays in Greystone's Azure tenant.", DF, owner=O),
        Claim("controls", "Managed-service provider change takes 18 days.", VP, "measured"),
        Claim("plan", "Pilot on day 120.", PD, "estimated"),
        Claim("decisions", "Which two clinics run the pilot.", DR),
        Claim("out of scope", "Patient-facing messages."),
    ]


def signed_v10(p: dict, inv: dict):
    """Friday afternoon, day 19, after the fax path was found and carved out."""
    e, f = inv["electronic"], inv["fax"]
    share = round(100 * e / (e + f))
    return [
        Claim("scope", f"Release 1 covers the electronic referral path: {inv['steps_e']} steps, {share}% of referrals "
              f"counted at two clinics on days 15 to 18 ({e} of {e + f}).", DF, "measured", owner=OPS),
        Claim("scope", "Outputs are drafts: a referral summary for the receiving clinician and a prior-authorization "
              "letter for the coordinator.", DF, owner=H),
        Claim("scope", f"{inv['det_e']} of {inv['steps_e']} steps are deterministic services; models are used in "
              f"{inv['model_e']} steps.", PD, "estimated", owner="Northlight"),
        Claim("out of scope", f"The fax path: {f} of {e + f} referrals in the count, {inv['steps_f']} more steps; "
              "backlog is concentrated there.", DF, "measured", owner=OPS),
        Claim("out of scope", "Submission to payers, urgency decisions, declining referrals, patient messages.",
              DF, owner=H),
        Claim("success", "A draft is acceptable when both scoring coordinators accept it with edits under three "
              "minutes; target 80% on 200 sampled referrals.", PD, "assumed", scorer="two coordinators; Michael "
              "Hart breaks ties"),
        Claim("success", "Zero red-flag referrals routed without clinician review in shadow.", DF, owner=H,
              scorer="Michael Hart"),
        Claim("autonomy", "Every red-flag term goes to a clinician; the system never sets urgency.", DF, owner=H),
        Claim("controls", "Processing stays in Greystone's Azure tenant; managed identity; just-in-time access for "
              "named engineers.", DF, owner=O),
        Claim("controls", "Managed-service provider change takes about 18 days.", VP, "estimated",
              owner="managed-service provider lead"),
        Claim("plan", f"Data on day {p['data']}; pilot on day {p['pilot']} (draft-only shadow, two clinics).",
              PD, "estimated", owner="Northlight",
              depends=(f"Architecture Review day 94", f"privacy board day {p['board']}",
                       "managed-service provider change")),
        Claim("plan", f"Privacy board submission complete by day {p['board'] - 10}.", PD, "assumed", owner="Michael Hart", due_day=p["board"] - 10),
        Claim("decisions", "Fax path: fund as release 2, move outside referrals to the e-referral portal, or both.",
              DR, owner=OPS, due_day=33),
        Claim("decisions", "Which two clinics run the shadow pilot.", DR, owner=H, due_day=26),
        Claim("decisions", "Written red-flag list per specialty, owned and dated.", DR, owner=H, due_day=40),
    ]


SIGNATURES = ("Michael Hart, CMIO: clinical rules and draft-only behavior, day 19",
              "VP ambulatory operations: scope, exclusions and operational ownership, day 19",
              "Sam Oakley, Security Lead: no objection to the controls section, day 19",
              "Northlight: projection and design lines, day 19")
