"""Greystone Health fixtures: the kickoff map (day 2), the working map (day 12), champions, design changes."""
from stakeholders import Person, StakeholderMap
from champions import Champion, Ask

# Day 2: drawn from the deal sheet and the kickoff attendee list. Looks 80 percent complete.
KICKOFF = StakeholderMap("Greystone", 2, [
    Person("hart", "Michael Hart", "CMIO", ("sponsor", "approver"), 2, source="kickoff"),
    Person("oakley", "Sam Oakley", "Security Lead", ("blocker",), 2, source="kickoff"),
    Person("bell", "Marcus Bell", "Procurement", ("owner",), 2, source="kickoff"),
])

OAKLEY_REASONS = (
    "PHI must not leave the tenant boundary I sign for",
    "every model output that reaches a chart needs an audit trail I can show a regulator",
    "the last vendor's pilot ran on a shared account for nine months",
)

# Day 12: after shadowing, one-to-ones and Sam's 41 questions at the day 5 working session.
DAY12 = StakeholderMap("Greystone", 12, [
    Person("hart", "Michael Hart", "CMIO", ("sponsor", "approver"), 10, source="own words"),
    Person("oakley", "Sam Oakley", "Security Lead", ("blocker", "approver"), 11, reasons=OAKLEY_REASONS, source="own words"),
    Person("alvarez", "Denise Alvarez", "VP Ambulatory Operations", ("owner",), 11, source="own words"),
    Person("monroe", "Keisha Monroe", "Referral coordinator lead, suburban clinic", ("operator",), 9, champion=True, source="observed"),
    Person("ortega", "Luis Ortega", "Referral coordinator, downtown clinic", ("operator",), 8, source="observed"),
    Person("bell", "Marcus Bell", "Procurement", ("approver",), 9, source="own words"),
    Person("shah", "Ravi Shah", "Integration engineer", (), 10, champion=True, source="observed"),
])

# Last direct contact as of day 40, the day the escalation email went to Michael without Sam (Chapter 15).
CONTACT_DAY40 = {"hart": 26, "oakley": 40, "alvarez": 33, "monroe": 37, "ortega": 19, "bell": 9, "shah": 22}


def at_day(m, contacts, day):
    people = [Person(p.key, p.name, p.title, p.roles, contacts.get(p.key, p.last_contact), p.champion, p.reasons, p.source)
              for p in m.people]
    return StakeholderMap(m.customer, day, people)


CHAMPIONS = [
    Champion("monroe", "Keisha Monroe", "her coordinators retype the same referral fields into three screens",
             can=("introduce us to coordinators at other clinics", "explain the fax queue", "test drafts on real cases"),
             cannot=("approve a workflow change", "speak for the downtown clinics", "accept clinical risk"),
             asks=[Ask(6, "introduce us to coordinators at two clinics", "introduce"),
                   Ask(9, "walk us through the fax queue at 7 am", "explain"),
                   Ask(12, "confirm coordinators may send draft letters without clinician review", "approve", "Michael Hart")]),
    Champion("shah", "Ravi Shah", "he has wanted to retire the referral interface scripts for two years",
             can=("explain the interface engine", "relay questions to the managed-service provider"),
             cannot=("grant access", "change a firewall rule", "answer for security"),
             asks=[Ask(7, "explain how referrals arrive from the EHR", "explain"),
                   Ask(10, "get us read access to the interface engine this week", "decide", "Sam Oakley")]),
]

# Design changes found days 3-19, by who surfaced them. Hours are the fix at design time (stand-in estimates).
DESIGN_CHANGES = [
    (4, "coordinator", "referrals arrive by fax at 9 of 11 clinics we asked about", 6),
    (5, "security", "no PHI in prompts sent outside the tenant", 8),
    (6, "coordinator", "payer portal session times out after 15 minutes", 3),
    (6, "coordinator", "urgency is set by the clinician, never by staff", 2),
    (7, "clinical", "drafts must cite the note line they came from", 5),
    (8, "coordinator", "two clinics keep a paper log the EHR never sees", 4),
    (9, "coordinator", "denied requests are reworked from a separate queue", 4),
    (9, "security", "service account per environment, no shared login", 3),
    (10, "coordinator", "coordinators batch work at 7 am and 2 pm", 2),
    (11, "clinical", "patient messages are out of scope", 1),
    (13, "coordinator", "specialty codes differ by payer in 30 percent of cases", 6),
    (15, "operations", "fax path needs an owner decision", 2),
    (17, "coordinator", "downtown clinic routes referrals through a shared inbox", 5),
    (19, "coordinator", "the 9:40 read-back question: faxed referrals with no order", 4),
]
