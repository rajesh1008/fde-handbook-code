"""Listings 49.7 and 49.8: fieldkit configured for a fourth customer, and the gate that does not exist there.

The fourth customer here is a LAB FIXTURE, not a story character: a wholesale distributor's supplier-invoice
desk, an industry with no model-risk function. Names are fixtures. Deterministic stand-in; no model calls.

Failure injection (mode 'naive'): the Caldwell gate plan is copied whole. 'Model-Risk Approval' has no owner in
this industry, so the project lead finds someone to sign it, and the fieldkit tracker reports five gates passed.
Mode 'checked' maps every template gate to an authority the customer actually has (role register), refuses a
signer who holds no such authority, and lists local gates the template lacks.
"""
import sys
import _paths  # noqa: F401
from fieldkit.gates import Tracker, GateRecord, Criterion, Measurement, GATES

TEMPLATE_OWNER = {"Architecture Review": "enterprise architect", "Build Complete": "operations owner",
                  "Shadow Exit": "operations owner", "Model-Risk Approval": "model-risk officer",
                  "Live Stable": "accountable executive"}

# The fourth customer's role register: who holds which authority (fixture names).
REGISTER = {
    "enterprise architect": ("Elena Sorensen", "architecture standards"),
    "operations owner": ("Marcus Hale", "accounts-payable operations"),
    "accountable executive": ("Rhea Coleman", "finance operations budget and risk acceptance"),
    "IT service manager": ("Tom Becker", "service desk and change scheduling"),
    "SOX control owner": ("Alana Pierce", "invoice-approval key control"),
}
INDUSTRY_GATES = {"model-risk officer": None}            # no such function in wholesale distribution
LOCAL_GATES = [("SOX control owner sign-off", "SOX control owner",
                "invoice approval is a key financial control; a change to it needs the control owner")]

SIGNED = {"Architecture Review": ("Elena Sorensen", 40), "Build Complete": ("Marcus Hale", 120),
          "Shadow Exit": ("Marcus Hale", 150), "Model-Risk Approval": ("Tom Becker", 152),
          "Live Stable": ("Rhea Coleman", 240)}


def role_of(person):
    return next((r for r, (p, _) in REGISTER.items() if p == person), None)


def build(signers):
    t = Tracker("fourth customer (lab fixture)")
    for g in GATES:
        who, day = signers[g]
        c = Criterion("agree", "decisions match the clerk", 0.85, owner="Marcus Hale")
        t.add(GateRecord(g, entry=[("previous gate evidence", "pack")], criteria=[c],
                         measurements=[Measurement("agree", 1_790, 2_000, measured_by="Marcus Hale",
                                                   on="2,000 invoices in shadow", day=day)],
                         signer=who, decided=day))
    return t


def check(signers, mapping):
    problems, rows = [], []
    for g in GATES:
        want = mapping.get(g, TEMPLATE_OWNER[g])
        holder = REGISTER.get(want)
        who, day = signers[g]
        if want in INDUSTRY_GATES and INDUSTRY_GATES[want] is None:
            problems.append(f"{g}: owner role '{want}' does not exist in this industry; map it or replace it")
            rows.append((g, want, "no such role", who))
            continue
        if holder is None:
            problems.append(f"{g}: owner role '{want}' has no named person in the register")
            rows.append((g, want, "unfilled", who))
            continue
        if holder[0] != who:
            problems.append(f"{g}: signed by {who} ({role_of(who)}), who holds no authority for it; "
                            f"the authority sits with {holder[0]} ({want})")
        rows.append((g, want, holder[0], who))
    for name, role, why in LOCAL_GATES:
        if role not in mapping.values() and name not in mapping:
            problems.append(f"local gate missing from the template: {name} ({REGISTER[role][0]}); {why}")
    return rows, problems


def show(t):
    for g, st, day, note in t.effective():
        print(f"  {g:22s} {st:24s} {'' if day is None else 'day ' + str(day):8s} {note}")


if __name__ == "__main__":
    mode = sys.argv[1]
    if mode == "naive":
        print("fieldkit gate plan copied from Caldwell to the fourth customer (lab fixture), no check")
        t = build(SIGNED)
        show(t)
        print(f"tracker: {sum(1 for r in t.effective() if r[1].startswith('passed'))} of 5 gates passed; "
              "Live Stable effective day 240")
        print("nobody at this customer can accept model risk; the signature on Model-Risk Approval is a")
        print("service desk manager's, and the tracker cannot tell")
    else:
        print("fieldkit gate plan with the industry map and role register checked")
        rows, probs = check(SIGNED, {})
        print("before the map:")
        for p in probs:
            print("  REFUSED " + p)
        mapping = {"Model-Risk Approval": "accountable executive", "SOX control owner sign-off": "SOX control owner"}
        fixed = dict(SIGNED)
        fixed["Model-Risk Approval"] = ("Rhea Coleman", 152)
        rows, probs = check(fixed, mapping)
        print("after the map (Model-Risk Approval -> risk acceptance by the accountable executive, with an")
        print("independent validation report as entry evidence; SOX control owner sign-off added):")
        for g, want, holder, who in rows:
            print(f"  {g:22s} owner role {want:22s} holder {holder:18s} signed {who}")
        print(f"  SOX control owner sign-off owner role SOX control owner      holder {REGISTER['SOX control owner'][0]}")
        print(f"problems: {len(probs)}")
        t = build(fixed)
        show(t)
