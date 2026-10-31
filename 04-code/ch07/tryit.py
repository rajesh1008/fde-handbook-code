"""Try It Yourself, Chapter 7. python tryit.py a|b|c"""
import sys
import caldwell_bank as cb
from questionbank import Bank, Question as Q, Answer as A, acting_for_gaps

def a():
    """Half the hour: which design-changing questions does a 30-minute prep sheet drop?"""
    b = cb.build(); r = b.reconcile(); changing = {q.qid for q, _ in r.design_changes}
    for mins in (60, 45, 30, 20):
        asked, dropped = b.prep("data owner", mins)
        lost = [q.qid for q in dropped if q.qid in changing]
        print(f"{mins:2d} min: {len(asked):2d} asked, {len(dropped):2d} dropped, design changes lost: {len(lost)} {' '.join(lost)}")

def b():
    """Greystone Health: an agent drafting prior-authorization requests for a referral coordinator."""
    g = Bank("Greystone Health")
    S = "security lead"
    g.add(Q("G01", "identity", S, "Which referrals may a coordinator open?", "decides what the drafting agent may read",
            "every referral in the group", "vendor position", "Northlight", ("other clinics' referrals",), "read scope", 3, True, 0.75))
    g.add(Q("G02", "identity", S, "Does minimum necessary limit the notes a draft may quote?", "decides which note sections reach the model",
            "no; the whole note is needed", "proposed design", "Northlight", ("psychotherapy notes", "substance-use records"), "masking", 3, False, 2.0))
    g.add(Q("G03", "data", S, "Is the fax receipt time the referral's received date?", "decides the clock for urgent referrals",
            "yes", "vendor position", "Northlight", ("faxes after 17:00",), "date rule", 2, True, 0.75))
    g.add(Q("G04", "audit", S, "Must every read name the coordinator it serves?", "decides what the gateway logs for every read",
            "yes", "direct customer fact", S, ("batch drafts",), "logging", 2, True, 0.75))
    needs = ("read own clinic referrals", "read other clinics' referrals", "read clinical notes", "read payer policy")
    grants = ("read own clinic referrals", "read clinical notes", "read payer policy")
    for q in g.questions.values():
        print(f"{q.qid} weight {q.weight():.1f}  {q.text}  (expect: {q.expected}; {q.status})")
    print("acting-for gaps for a referral coordinator:", acting_for_gaps(needs, grants))

def c():
    """The wrong person: record the data platform lead's day-9 answer to Q14 as if it settled the question."""
    b = cb.build()
    b.answers["Q14"] = A("Q14", 9, "data platform lead", "platform", "confirmed", "the mart is fine for duplicates", 0.5)
    r = b.reconcile()
    print(f"design changes now: {len(r.design_changes)} (was 9); answers set aside as not from the owner: {len(r.wrong_person)}")
    for q, a in r.wrong_person:
        print(f"  {q.qid}: answered by {a.who} ({a.role}); owner is the {q.audience}; question stays open")

{"a": a, "b": b, "c": c}[sys.argv[1] if len(sys.argv) > 1 else "a"]()
