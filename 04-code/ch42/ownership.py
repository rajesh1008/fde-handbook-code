"""Ownership and hand-over readiness through the first ninety days at Pennant (Chapter 42). Usage: python ownership.py
Two instruments. (1) Chapter 41's readiness score (fieldkit.handover.score over the twenty hand-over items, gated),
re-run on production evidence: 0.40 at go-live, then each event changes only the items a customer person actually
did. (2) fieldkit.liveops.OwnershipMap: the five ownership proofs plus five operational holdings, with holders and
deputies, the two-of-five rule, single points and orphans."""
import importlib.util
from pathlib import Path
import _paths  # noqa: F401
from world import CAL, GO_LIVE
from fieldkit.handover import score, without, Item
from fieldkit.liveops import OwnershipMap, PageRoute

_spec = importlib.util.spec_from_file_location("ch41world", Path(__file__).parent.parent / "ch41" / "world.py")
W41 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(W41)

J, R, D, K, G, T = "Jenna Ruiz", "Rosa Delgado", "Dana Whitaker", "Kofi Mensah", "Grant Holloway", "Tasha Greene"
A, N, CM, CPL = "Andre Willis", "Nadia Brooks", "Joanne Pruitt", "Pennant cloud platform lead"

# day, event, readiness item changes (only what a customer person did), ownership-map changes
EVENTS = [
    (CAL["jenna_last"], "Jenna Ruiz's last day in the sponsor role", {}, [("leave", J)]),
    (CAL["rosa_holds"], "Rosa Delgado accepts operations and override; RACI re-signed",
     {"C1": ("alone", (R, K, D))}, [("own-operations", R, None, False), ("own-override", R, None, False)]),
    (CAL["grant_accepts"], "Grant Holloway accepts the executive proof; signs the runbook owner list",
     {"R1": ("alone", (G, K))}, [("own-exec", G, None, False)]),
    (CAL["recal_signed"], "Dana Whitaker signs the re-calibration; monthly report produced by her team",
     {"T3": ("alone", (D, T)), "M3": ("alone", (D,))},
     [("own-gold-set", D, T, True), ("drift monitor read", D, None, False)]),
    (38, "incident: Andre Willis rolls back to shadow on Rosa Delgado's approval, FDE diagnosing",
     {"R3": ("assisted", (A, R)), "D2": ("assisted", (A, R))}, []),
    (CAL["runbook_change"], "runbook change: alerts and on-call move to Pennant platform",
     {"M1": ("alone", (K, A)), "M4": ("alone", (A,))},
     [("on-call primary", A, None, False), ("runbook executed", A, None, False)]),
    (CAL["account_moved"], "provider account moved to Kofi Mensah; monitors run as Pennant jobs",
     {"M2": ("alone", (K,))}, [("provider account", K, None, False)]),
    (CAL["migrate"], "EU model change run under change control by Pennant",
     {"T4": ("alone", (K, D)), "T2": ("assisted", (K,))}, [("own-model-risk", CM, None, True)]),
    (CAL["deputies"], "deputies named for operations and override; vendor only consulted",
     {"C2": ("alone", (R, K)), "E3": ("assisted", (D, K))},
     [("own-operations", R, T, True), ("own-override", R, D, True)]),
    (CAL["drill"], "Nadia Brooks runs the incident drill alone, rollback included",
     {"D1": ("alone", (N,)), "R2": ("alone", (N,)), "R3": ("alone", (N, R)), "D2": ("alone", (N, R))},
     [("on-call primary", A, N, True), ("runbook executed", A, N, True)]),
]


def at_go_live():
    m = OwnershipMap()
    m.add("own-exec", J)
    m.add("own-gold-set", D, exercised=True)
    m.add("own-operations", J, deputy=R)
    m.add("own-model-risk", CM, exercised=True)
    m.add("own-override", J, deputy=R)
    m.add("on-call primary", "Northlight")
    m.add("runbook executed", "Northlight")
    m.add("drift monitor read", "Northlight")
    m.add("change board", K, deputy=CPL, exercised=True)
    m.add("provider account", J)
    return m


def items(state):
    return [Item(i, d, t, state[i][0], state[i][1], g) for i, d, t, g in W41.ITEMS]


def timeline():
    st, m = dict(W41.PENNANT), at_go_live()
    s = score(items(st))
    out = [(0, "go-live, as handed over", s, m.orphans(), m.single_points())]
    for day, what, ch, own in EVENTS:
        for o in own:
            if o[0] == "leave":
                st = {i.id: (i.status, i.by) for i in without(items(st), o[1])}
                m.leave(o[1])
            else:
                m.add(o[0], o[1], deputy=o[2], exercised=o[3])
        st.update(ch)
        out.append((day, what, score(items(st)), m.orphans(), m.single_points()))
    return m, out


if __name__ == "__main__":
    m0 = at_go_live()
    print(f"OWNERSHIP AND READINESS  Pennant  production day 0 = engagement day {GO_LIVE}  (deterministic stand-in)")
    print(f"two-of-five rule at go-live: {m0.two_of_five() or 'passes'}")
    print(f"holdings with no deputy at go-live ({len(m0.single_points())}): " + "; ".join(m0.single_points()))
    route = PageRoute(primary="nl-pennant-oncall@northlight.example", secondary="FDE (pseudonymized view)",
                      rollback_approver=J, approver_is_role=False)
    m0.leave(J)
    print(f"page route lint, day {CAL['jenna_last']}: " + "; ".join(route.lint(m0)))
    print(f"orphaned on day {CAL['jenna_last']}: " + ", ".join(m0.orphans()))
    print("day  readiness  gates failing  orphans  no deputy  event")
    m, tl = timeline()
    for day, what, s, orph, sp in tl:
        cap = f"{s.gated:.2f}" + ("*" if s.capped else " ")
        print(f"{day:>3}   {cap:<8}  {','.join(s.failing_gates) or '-':<13}  {len(orph):>7}  {len(sp):>9}  {what}")
    print("* capped at 0.60 while a gate item is not done alone (raw score higher)")
    print("day 90 ownership map:")
    for h in m.holdings.values():
        print(f"  {h.item:<20} {h.holder or '-':<27} deputy {h.deputy or '-':<29} {'done alone' if h.exercised else ''}")
    fixed = PageRoute(primary="pennant-platform-oncall", secondary="fde-oncall@northlight.example",
                      rollback_approver="own-operations")
    print(f"page route lint on day 90: {'; '.join(fixed.lint(m)) or 'clean'}")
    print(f"still without a deputy on day 90: " + "; ".join(m.single_points()))
