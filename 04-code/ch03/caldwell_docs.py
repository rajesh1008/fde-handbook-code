"""Chapter 3 fixtures: the ten documents Anne Kessler brought to the day-two demo, with her corrections,
and the ten documents of Northlight's own demo set.

Everything here is fictional and generated for the book. The Caldwell documents imitate what arrives at a
claims intake desk after the mailroom scanner or the fax server has turned paper into text: line breaks in
odd places, letters read as digits, labels that differ from form to form. They came from one week's intake
(4 email, 3 fax, 3 mail), the week before the engagement started.

Ten fields per document, as Anne defines them (Caldwell's meanings, not the demo's):
  policy_number      Caldwell policy, two letters and six digits; None if the sender did not give one
  claimant_name      the person making the claim (not the sender, not the insured if they differ)
  loss_date          the date of the loss, ISO
  date_received      the date the document reached Caldwell (email sent time, fax header, mailroom stamp);
                     the acknowledgement clock starts here
  loss_type          Caldwell's loss code: AUTO-COLL, AUTO-COMP, PROP-WATER, PROP-FIRE, PROP-WIND,
                     PROP-THEFT, LIAB-BI
  loss_location      where the loss happened, as an adjuster would key it
  injury_reported    "yes" or "no"
  police_report_ref  police or fire incident reference, None if none given
  other_party        the other person involved, None if none
  intake_channel     email, fax or mail
"""

FIELDS = ["policy_number", "claimant_name", "loss_date", "date_received", "loss_type", "loss_location",
          "injury_reported", "police_report_ref", "other_party", "intake_channel"]

# The day the notebook ran (engagement day 2). The demo stamps this as date_received.
RUN_DATE = "2026-08-04"

CALDWELL_DOCS = [
    dict(id="C01", channel="email", text="""From: Emily Carter <ecarter@example.net>
Sent: Monday, July 27, 2026 7:12 AM
To: claims@caldwellmutual.example
Subject: Car accident Saturday

Hi, my policy is HP402913. On Saturday 07/25/2026 I was rear-ended at the light outside
1450 Farmington Ave, Hartford. The other driver, Kevin Doyle, admitted it was his fault. No one was hurt.
Police came, report number HPD-26-118734.
Thanks, Emily""",
         gold=dict(policy_number="HP402913", claimant_name="Emily Carter", loss_date="2026-07-25",
                   date_received="2026-07-27", loss_type="AUTO-COLL",
                   loss_location="1450 Farmington Ave, Hartford", injury_reported="no",
                   police_report_ref="HPD-26-118734", other_party="Kevin Doyle", intake_channel="email")),

    dict(id="C02", channel="email", text="""From: Dana Whitcomb <dana@whitcombagency.example>
Sent: Tuesday, July 28, 2026 9:48 AM
To: claims@caldwellmutual.example
Subject: New loss - Ortiz - HP518220

Good morning. Our client Raymond Ortiz, policy HP518220, had a supply line under the kitchen sink fail
on 7/27/2026 at the insured residence, 14 Maple Ridge Rd, West Hartford. Water reached the finished
basement; nobody was down there at the time. Plumber's invoice to follow.
Dana Whitcomb | Whitcomb Insurance Agency""",
         gold=dict(policy_number="HP518220", claimant_name="Raymond Ortiz", loss_date="2026-07-27",
                   date_received="2026-07-28", loss_type="PROP-WATER",
                   loss_location="14 Maple Ridge Rd, West Hartford", injury_reported="no",
                   police_report_ref=None, other_party=None, intake_channel="email")),

    dict(id="C03", channel="fax", text="""JUL-29-2026 16:42 FROM:SHELDON AUTO BODY 860 555 0147 P.1/2
CALDWELL MUTUAL  FIRST NOTICE OF LOSS
INSURED: PATRICK HSU
POLICY NO: HP 3O7745
DATE OF LOSS: 07/28/26
DESCRIPTION: VEH STRUCK DEER RT 4 FARMINGTON. FRONT END DMG. NO INJ.
REPAIR FACILITY: SHELDON AUTO BODY""",
         gold=dict(policy_number="HP307745", claimant_name="Patrick Hsu", loss_date="2026-07-28",
                   date_received="2026-07-29", loss_type="AUTO-COMP", loss_location="Route 4, Farmington",
                   injury_reported="no", police_report_ref=None, other_party=None, intake_channel="fax")),

    dict(id="C04", channel="email", text="""From: Luis Ferreira <lferreira77@example.com>
Sent: Thursday, July 30, 2026 6:05 AM
To: claims@caldwellmutual.example
Subject: my car was stolen

Someone stole my 2021 Honda CR-V out of my driveway last night at 52 Hillcrest Dr, Wethersfield.
Policy HP661038. I filed with Wethersfield PD, case number 26-4471. Nobody was hurt, I just need
a rental to get to work.""",
         gold=dict(policy_number="HP661038", claimant_name="Luis Ferreira", loss_date="2026-07-29",
                   date_received="2026-07-30", loss_type="AUTO-COMP",
                   loss_location="52 Hillcrest Dr, Wethersfield", injury_reported="no",
                   police_report_ref="26-4471", other_party=None, intake_channel="email")),

    dict(id="C05", channel="email", text="""From: Susan Albright <s.albright@example.org>
Sent: Thursday, July 30, 2026 2:31 PM
To: claims@caldwellmutual.example
Subject: Tree on roof, policy HP245187

During the storm on 07/29/2026 a large oak came down on our roof at 7 Birch Hollow Ln, Avon.
There is a hole over the back bedroom and rain is getting in. Nobody was home. We have a tarp on it.
Susan Albright""",
         gold=dict(policy_number="HP245187", claimant_name="Susan Albright", loss_date="2026-07-29",
                   date_received="2026-07-30", loss_type="PROP-WIND",
                   loss_location="7 Birch Hollow Ln, Avon", injury_reported="no",
                   police_report_ref=None, other_party=None, intake_channel="email")),

    dict(id="C06", channel="fax", text="""07/30/2026 11:15  RIVERSIDE RESTORATION  P.1
INSURED: MARGARET ELLIS            P0LICY N0: HP6l2O48
LOSS LOCATION: 88 Prospect St, Wethersfield
DATE OF LOSS: 07/29/2026
KITCHEN FIRE, STOVE TOP. FD ON SCENE, INCIDENT 26-0912.
FF TREATED INSURED FOR SMOKE INHALATION AT SCENE.
BOARD-UP COMPLETE, PLS ADVISE ON MITIGATION AUTH""",
         gold=dict(policy_number="HP612048", claimant_name="Margaret Ellis", loss_date="2026-07-29",
                   date_received="2026-07-30", loss_type="PROP-FIRE",
                   loss_location="88 Prospect St, Wethersfield", injury_reported="yes",
                   police_report_ref="26-0912", other_party=None, intake_channel="fax")),

    dict(id="C07", channel="fax", text="""JUL-30-2026 15:03 FROM:CAPITOL COLLISION CTR P.1/3
INSURED: ANDREA KOVACS
POLICY NO: HP790356
DATE OF LOSS: 07/30/2026
LOCATION: Main St & Park Rd, West Hartford
OTHER PARTY: L. NGUYEN
POLICE REPORT # WHPD 2026-33817
INJURIES: DRIVER COMPLAINS OF NECK PAIN, SEEN AT URGENT CARE""",
         gold=dict(policy_number="HP790356", claimant_name="Andrea Kovacs", loss_date="2026-07-30",
                   date_received="2026-07-30", loss_type="AUTO-COLL",
                   loss_location="Main St & Park Rd, West Hartford", injury_reported="yes",
                   police_report_ref="WHPD 2026-33817", other_party="L. Nguyen", intake_channel="fax")),

    dict(id="C08", channel="mail", text="""RECEIVED  AUG 03 2026  CALDWELL MUTUAL MAILROOM
Dear Sir or Madam,
I am writing about my fall on the front steps of 23 Oak St, Bloomfield, the home of your
insured Harold Brennan, on July 24. The top step is loose. I broke my wrist and went to
Saint Francis hospital. Please tell me who to send the bills to.
Sincerely,
Gloria Pratt""",
         gold=dict(policy_number=None, claimant_name="Gloria Pratt", loss_date="2026-07-24",
                   date_received="2026-08-03", loss_type="LIAB-BI", loss_location="23 Oak St, Bloomfield",
                   injury_reported="yes", police_report_ref=None, other_party=None, intake_channel="mail")),

    dict(id="C09", channel="mail", text="""RECEIVED  AUG 03 2026  CALDWELL MUTUAL MAILROOM
July 28, 2026
Re: Policy HP538804, Unit 4B, 410 Asylum St, Hartford
To whom it may concern,
On 07/26/2026 water came through my bathroom ceiling from the unit above, which belongs to
Peter Lindqvist. Building management shut off the water. The ceiling and vanity are damaged.
No one was injured.
Yours, Naomi Brandt""",
         gold=dict(policy_number="HP538804", claimant_name="Naomi Brandt", loss_date="2026-07-26",
                   date_received="2026-08-03", loss_type="PROP-WATER",
                   loss_location="410 Asylum St, Unit 4B, Hartford", injury_reported="no",
                   police_report_ref=None, other_party="Peter Lindqvist", intake_channel="mail")),

    dict(id="C10", channel="mail", text="""RECEIVED  AUG 03 2026  CALDWELL MUTUAL MAILROOM
CALDWELL MUTUAL INSURANCE CO.   PROPERTY LOSS NOTICE   FORM CM-114 (REV. 1998)
POLICY #  HP 1 5 7 6 2 9        NAME OF INSURED  WALTER  OKAFOR
DATE OF LOSS  07 / 29 / 2026
ADDRESS OF LOSS  31 Cedar Ter, Newington
KIND OF LOSS  [ ] FIRE  [ ] WATER  [X] THEFT  [ ] WIND  [ ] OTHER
GARAGE BROKEN INTO, TOOLS AND BICYCLES TAKEN
INJURIES  [ ] YES  [X] NO
POLICE NOTIFIED  [X] YES   REPORT NO. NPD-26-2208""",
         gold=dict(policy_number="HP157629", claimant_name="Walter Okafor", loss_date="2026-07-29",
                   date_received="2026-08-03", loss_type="PROP-THEFT",
                   loss_location="31 Cedar Ter, Newington", injury_reported="no",
                   police_report_ref="NPD-26-2208", other_party=None, intake_channel="mail")),
]

# Northlight's demo set: clean typed forms in the layout the demo was built on. Uploaded through the demo
# app, so date_received is the upload date and the channel is "upload".
_DEMO = [
    ("D01", "HP100231", "Jordan Lee", "03/02/2026", "Rear-end collision", "120 Main St, Springfield",
     "None", "SPD-26-0101", "Chris Moore (other driver)"),
    ("D02", "HP100488", "Alex Rivera", "03/04/2026", "Burst pipe, water damage", "9 Elm St, Springfield",
     "None", "", ""),
    ("D03", "HP100752", "Sam Patel", "03/05/2026", "Kitchen fire", "44 Oak Ave, Springfield",
     "Minor burn, treated at hospital", "FD-26-0042", ""),
    ("D04", "HP101006", "Taylor Brooks", "03/07/2026", "Vehicle stolen from lot", "Lot B, 300 Market St, Springfield",
     "None", "SPD-26-0177", ""),
    ("D05", "HP101329", "Morgan Diaz", "03/09/2026", "Wind damage to roof", "18 Pine Rd, Springfield",
     "None", "", ""),
    ("D06", "HP101544", "Casey Nguyen", "03/10/2026", "Two-vehicle collision", "Main St and 5th St, Springfield",
     "Passenger injured, ambulance called", "SPD-26-0203", "Pat Kim"),
    ("D07", "HP101870", "Riley Chen", "03/12/2026", "Basement water damage", "61 Lake Dr, Springfield",
     "None", "", ""),
    ("D08", "HP102115", "Jamie Fox", "03/13/2026", "Garage break-in, theft", "7 Hill St, Springfield",
     "None", "SPD-26-0240", ""),
    ("D09", "HP102398", "Drew Wilson", "03/16/2026", "Backed into parked car", "200 Bay Rd, Springfield",
     "No injuries", "", "Lee Grant"),
    ("D10", "HP102661", "Quinn Adams", "03/18/2026", "Hail damage to roof", "5 Ridge Ln, Springfield",
     "None", "", ""),
]
_DEMO_GOLD_TYPE = {"D01": "AUTO-COLL", "D02": "PROP-WATER", "D03": "PROP-FIRE", "D04": "AUTO-COMP",
                   "D05": "PROP-WIND", "D06": "AUTO-COLL", "D07": "PROP-WATER", "D08": "PROP-THEFT",
                   "D09": "AUTO-COLL", "D10": "PROP-WIND"}


def _iso(mdy):
    m, d, y = mdy.split("/")
    return f"{y}-{int(m):02d}-{int(d):02d}"


def demo_docs():
    out = []
    for (i, pol, name, dol, typ, loc, inj, pol_ref, other) in _DEMO:
        text = (f"NORTHLIGHT DEMO CLAIM FORM\nPolicy Number: {pol}\nInsured: {name}\nDate of Loss: {dol}\n"
                f"Type of Loss: {typ}\nLocation: {loc}\nInjuries: {inj}\nPolice Report #: {pol_ref}\n"
                f"Other Party: {other}\n")
        gold = dict(policy_number=pol, claimant_name=name, loss_date=_iso(dol), date_received="2026-03-20",
                    loss_type=_DEMO_GOLD_TYPE[i], loss_location=loc,
                    injury_reported="no" if inj in ("None", "No injuries") else "yes",
                    police_report_ref=pol_ref or None, other_party=(other.split(" (")[0] or None), intake_channel="upload")
        out.append(dict(id=i, channel="upload", text=text, gold=gold, uploaded="2026-03-20"))
    return out


def caldwell_docs():
    return [dict(d, uploaded=RUN_DATE) for d in CALDWELL_DOCS]
