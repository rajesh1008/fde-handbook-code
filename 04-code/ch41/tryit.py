"""Try It Yourself. a: remove the gate cap; b: what moves Pennant; c: reroute A-09 to a Northlight address."""
import sys
from dataclasses import replace
import world as W
from fieldkit import handover as H
p = sys.argv[1]
if p == "a":
    it = W.items(W.CALDWELL_BEFORE)
    print(f"Caldwell day 176 with gates: {H.score(it).gated:.2f}")
    print(f"Caldwell day 176 without gates (raw credit): {H.score([replace(i, gate=False) for i in it]).gated:.3f}")
    print("the alert that reached Northlight is worth 1 item of 20 without a gate")
elif p == "b":
    st = dict(W.PENNANT)
    print(f"Pennant now: {H.score(W.items(st)).gated:.2f}")
    for k, v, why in [("M4", ("alone", ("Kofi Mensah", "Pennant integration rota")), "customer on-call rota from 01:30"),
                      ("M1", ("alone", ("Kofi Mensah",)), "alerts rerouted to the rota"),
                      ("D1", ("alone", ("Pennant integration rota", "Kofi Mensah")), "drill passed alone"),
                      ("R3", ("alone", ("Jenna Ruiz", "Dana Whitaker")), "second person can switch modes")]:
        st[k] = v
        it = W.items(st)
        print(f"+ {why:<36} {H.score(it).gated:.2f}  without Jenna Ruiz {H.score(H.without(it, 'Jenna Ruiz')).gated:.2f}")
else:
    al = [replace(a, dest=W.NL) if a.id == "A-09" else a for a in W.ALERTS_V2]
    print("A-09 rerouted to " + W.NL)
    print("routing check: " + ", ".join(a.id for a in H.route_check(al, W.CW)))
    rb = [r for r in W.RUNBOOKS_V2 if r.id == "RB-02"][0]
    print(f"runbook lint RB-02: {H.lint_runbook(rb, W.CW_PEOPLE, al) or 'ok'} (lint checks the trigger exists, not where it goes)")
