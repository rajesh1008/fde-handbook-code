"""Runs one referral through the input, output, action and budget guardrails and returns its disposition."""
import _paths  # noqa: F401
from fieldkit.guardrails import Decision, GuardrailSuite
from rules import CARDS, version
from checks import checks

DRAFT_GATES = {"A-12", "A-13"}


def suite(v="v3", cards=None):
    return GuardrailSuite(version(cards or CARDS, v), checks(v), version=v)


def run(s, ref, draft, actions, budget_stop=None, pre=None):
    ctx = dict(ref=ref)
    if pre is not None and pre(ref):
        return dict(disp="refused by keyword guard", fired=["KW"], denied=[], flags=[], repairs=[])
    din = s.run("input", ctx)
    flags = [v.rid for v in din.failed if v.effect == "flag"]
    if din.effect in ("block", "route"):
        return dict(disp=("blocked, to " if din.effect == "block" else "routed to ") + (din.route_to or "coordinator"), fired=[v.rid for v in din.failed],
                    denied=[], flags=flags, repairs=[])
    ctx.update(draft=draft, actions=actions or [], budget_stop=budget_stop or {})
    out, act, bud = s.run("output", ctx), s.run("action", ctx), s.run("budget", ctx)
    denied = [v.rid for v in act.failed if v.rid not in DRAFT_GATES]
    d = Decision.of(out.verdicts + bud.verdicts + [v for v in act.verdicts if v.rid in DRAFT_GATES])
    flags += [v.rid for v in d.failed if v.effect == "flag"]
    repairs = [v.rid for v in d.failed if v.effect == "repair"]
    if d.effect in ("block", "route"):
        disp = ("blocked, to " if d.effect == "block" else "routed to ") + (d.route_to or "coordinator")
    elif d.effect == "repair":
        disp = "queued after repair"
    elif d.effect == "flag":
        disp = "queued with flag"
    else:
        disp = "queued"
    return dict(disp=disp, fired=[v.rid for v in d.failed] + denied, denied=denied, flags=flags, repairs=repairs)


def queued(res):
    return res["disp"].startswith("queued")
