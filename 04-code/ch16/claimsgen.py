"""Chapter 16: a generator of claim documents that look like Caldwell Mutual's intake.

STRUCTURE FROM DISCOVERY, CONTENT FROM A MODEL. A Profile holds the structure: which document types, channels,
senders, date styles, languages and exceptions occur, and how often. Discovery (Chapter 6), the customer's experts
and, once it exists, a label-free profile of the real sample supply it. The content (names, streets, narratives)
comes from a content model. On the build machine there are no model keys, so the content model is a
CONTENT-MODEL STAND-IN: seeded phrase pools, deterministic, labeled as such wherever it is used.

Everything here is fictional. The Caldwell "real sample" in standin_sample.py is itself a STAND-IN: the real 200
files never leave Caldwell's account, and no book can print them.

Fields are Anne Kessler's ten (Chapter 3). A field that a document does not state has gold value None.
"""
import random
from dataclasses import dataclass, field

FIELDS = ["policy_number", "claimant_name", "loss_date", "date_received", "loss_type", "loss_location",
          "injury_reported", "police_report_ref", "other_party", "intake_channel"]
DOC_TYPES = ["first notice of loss", "adjuster note", "repair estimate", "police report", "medical bill", "photo log"]
CHANNELS = ["email", "fax", "mail"]
EXCEPTIONS = ["faded scan", "no policy number", "agent sender", "forwarded chain", "short or written date",
              "Spanish-language", "not a first notice"]

FIRST = ["Emily", "Raymond", "Maria", "Kevin", "Dana", "Luis", "Grace", "Peter", "Aisha", "Thomas", "Rosa", "Brian",
         "Hannah", "Victor", "Carmen", "Derek", "Nadia", "Owen", "Julia", "Marcus", "Ines", "Colin", "Tanya", "Wesley"]
LAST = ["Carter", "Ortiz", "Doyle", "Whitcomb", "Alvarez", "Brennan", "Nguyen", "Kowalski", "Price", "Santos",
        "Fitzgerald", "Haddad", "Morales", "Lindqvist", "Okoro", "Delgado", "Pryor", "Castillo", "Mercer", "Rivera"]
TOWNS = ["Hartford", "West Hartford", "New Britain", "Manchester", "Glastonbury", "Wethersfield", "Bristol",
         "Enfield", "Middletown", "Meriden", "Newington", "Windsor"]
STREETS = ["Farmington Ave", "Maple Ridge Rd", "Main St", "Park Rd", "Berlin Tpke", "Prospect Ave", "Asylum St",
           "Elm St", "Church St", "Oak Ln", "Hillside Dr", "Summit Way"]
MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
          "November", "December"]
WEEKDAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
AGENCIES = ["Whitcomb Insurance Agency", "Farmington Valley Insurance", "Capitol Risk Partners"]
SHOPS = ["SHELDON AUTO BODY", "CEDAR COLLISION", "RT 6 AUTO REPAIR"]

# The content-model stand-in. "plain" is what a model gives when asked for claim narratives; "ambiguous" is the
# variety it adds; "field" are phrasings adjusters see that a model rarely writes; "es" are Spanish narratives.
NARRATIVES = {
    "AUTO-COLL": dict(plain=["I was rear-ended at the light", "my car collided with a pickup truck",
                             "a delivery van ran into my car"],
                      field=["the car in front stopped short and I couldn't stop in time",
                             "I backed out and clipped a parked SUV"],
                      es=["chocaron mi carro por detras"]),
    "AUTO-COMP": dict(plain=["a tree branch fell on my parked car", "someone vandalized my car",
                             "hail damaged the hood of my car"],
                      field=["somebody keyed the whole side of my car", "someone took the catalytic converter"],
                      es=["un arbol cayo sobre mi carro"]),
    "PROP-WATER": dict(plain=["a pipe burst in the basement", "the water heater leaked"],
                       field=["the upstairs toilet overflowed through the ceiling"],
                       es=["se revento una tuberia en la cocina"]),
    "PROP-FIRE": dict(plain=["a kitchen fire damaged the stove and cabinets"],
                      ambiguous=["water from the fire hoses soaked the basement after a kitchen fire"],
                      field=["the dryer vent caught and charred the laundry room"], es=["hubo un incendio en la cocina"]),
    "PROP-WIND": dict(plain=["high winds tore shingles off the roof", "a storm blew the fence down"],
                      ambiguous=["a storm brought a tree down on the roof"],
                      field=["a gust lifted the back porch roof"], es=["el viento arranco parte del techo"]),
    "PROP-THEFT": dict(plain=["our garage was broken into and tools were stolen"],
                       field=["someone got into the shed and took the snowblower"],
                       es=["entraron a robar al garaje"]),
    "LIAB-BI": dict(plain=["a visitor slipped on our icy front steps", "a guest tripped on the porch"],
                    field=["our dog bit the mail carrier"], es=["una visita se resbalo en la escalera"]),
}
INJURY_LOSS = {"LIAB-BI"}


@dataclass
class Profile:
    """The structure of a document set: categorical mixes and exception rates. No content, no identifiers."""
    name: str
    doc_type: dict
    channel: dict
    ocr: tuple = ("uniform", 0.90, 0.99)          # or ("beta", a, b) or ("list", [values])
    agent_sender: float = 0.0                      # share of emails sent by an agency for its client
    forwarded: float = 0.0                         # share of emails that are forwarded chains
    date_style: dict = field(default_factory=lambda: {"mdy4": 1.0})
    spanish: float = 0.0
    no_policy: float = 0.0
    narrative_pools: tuple = ("plain", "ambiguous")
    pool_weights: tuple = (0.85, 0.15)
    location_style: dict = field(default_factory=lambda: {"street": 1.0})
    party_style: dict = field(default_factory=lambda: {"labeled": 1.0})
    injury_style: dict = field(default_factory=lambda: {"plain": 1.0})
    scanned_below: float = 0.0                     # files with OCR below this arrive as fax or mail scans


def pick(rng, mix):
    keys = list(mix)
    return rng.choices(keys, weights=[mix[k] for k in keys])[0]


def name(rng):
    return f"{rng.choice(FIRST)} {rng.choice(LAST)}"


def mdy(d, style):
    y, m, dd = d
    if style == "mdy2":
        return f"{m}/{dd}/{y % 100:02d}"
    if style == "written":
        return f"the {dd}{'th' if 10 < dd < 20 else {1: 'st', 2: 'nd', 3: 'rd'}.get(dd % 10, 'th')}"
    if style == "dmy_es":
        return f"{dd:02d}/{m:02d}/{y}"
    return f"{m:02d}/{dd:02d}/{y}"


def iso(d):
    return f"{d[0]:04d}-{d[1]:02d}-{d[2]:02d}"


def add_days(d, n):
    import datetime as dt
    x = dt.date(*d) + dt.timedelta(days=n)
    return (x.year, x.month, x.day)


def weekday(d):
    import datetime as dt
    return WEEKDAYS[dt.date(*d).weekday()]


CONFUSE = {"0": "O", "O": "0", "1": "l", "l": "1", "5": "S", "S": "5", "8": "B", "B": "8", "H": "N", "I": "1",
           "e": "c", "a": "o", "2": "Z", "6": "b"}


def ocr_noise(text, conf, rng, k=0.5):
    """Character confusions a fax or mailroom scan produces; p per eligible character grows as confidence falls."""
    p = max(0.0, min(0.45, (0.985 - conf) * k))
    out = []
    for ch in text:
        if ch in CONFUSE and rng.random() < p:
            out.append(CONFUSE[ch])
        else:
            out.append(ch)
    return "".join(out)


def draw_ocr(rng, spec):
    kind = spec[0]
    if kind == "uniform":
        return round(rng.uniform(spec[1], spec[2]), 3)
    if kind == "beta":
        return round(rng.betavariate(spec[1], spec[2]), 3)
    return rng.choice(spec[1])


def gold_record(rng, doc_type, channel, loss_type, policy, loss_d, recv_d, loc, party, police, injured, claimant):
    g = dict(policy_number=policy, claimant_name=claimant, loss_date=iso(loss_d), date_received=iso(recv_d),
             loss_type=loss_type, loss_location=loc, injury_reported="yes" if injured else "no",
             police_report_ref=police, other_party=party, intake_channel=channel)
    # What each non-FNOL document actually states (Anne's rule: a field it does not state is None).
    if doc_type == "repair estimate":
        g.update(loss_type=None, loss_location=None, injury_reported=None, police_report_ref=None, other_party=None)
    elif doc_type == "medical bill":
        g.update(loss_date=None, loss_type=None, loss_location=None, injury_reported="yes", police_report_ref=None,
                 other_party=None, policy_number=None)
    elif doc_type == "photo log":
        g.update(policy_number=None, claimant_name=None, loss_date=None, loss_type=None, loss_location=None,
                 injury_reported=None, police_report_ref=None, other_party=None)
    elif doc_type == "police report":
        g.update(policy_number=policy)
    return g


def render(rng, doc_type, channel, g, ctx):
    """Turn a gold record into document text in the house style of one channel and document type."""
    s = ctx
    pol = g["policy_number"]
    if doc_type == "first notice of loss":
        if s["spanish"]:
            body = (f"Hola, mi poliza es {pol}. " if pol else "Hola, no tengo el numero de poliza a mano. ") + \
                   f"El {s['loss_txt']} {s['narr']} en {s['loc_txt']}. " + \
                   ("Hay heridos. " if g["injury_reported"] == "yes" else "No hubo heridos. ") + \
                   (f"Reporte de policia {g['police_report_ref']}. " if g["police_report_ref"] else "")
        else:
            body = (f"My policy is {pol}. " if pol else "I don't have my policy number handy. ") + \
                   f"On {s['loss_txt']} {s['narr']} {s['loc_txt']}. " + s["party_txt"] + s["injury_txt"] + \
                   (f"Police came, report number {g['police_report_ref']}. " if g["police_report_ref"] else "")
        if channel == "email":
            return email_wrap(rng, g, s, body)
        if channel == "fax":
            if s["fax_form"]:
                return (f"{s['fax_hdr']} FROM:{s['fax_from']} 860 555 01{rng.randint(10, 99)} P.1/1\n"
                        f"CALDWELL MUTUAL  FIRST NOTICE OF LOSS\nPOLICY NO: {pol or 'NONE'}\n"
                        f"CLAIMANT: {g['claimant_name']}\nDATE OF LOSS: {s['loss_txt']}\n"
                        f"LOCATION: {g['loss_location']}\nDESCRIPTION: {s['narr']}\n"
                        f"INJURIES: {'YES' if g['injury_reported'] == 'yes' else 'NO'}\n"
                        f"POLICE REPORT: {g['police_report_ref'] or 'NONE'}\nOTHER PARTY: {g['other_party'] or 'NONE'}\n")
            return f"{s['fax_hdr']} FROM:{s['fax_from']} 860 555 01{rng.randint(10, 99)} P.1/2\n{body}\n{g['claimant_name']}\n"
        return (f"RECEIVED {s['stamp']} CALDWELL MUTUAL MAILROOM\n{rng.randint(10, 999)} {rng.choice(STREETS)}\n"
                f"Dear Caldwell Mutual,\n{body}\nSincerely,\n{g['claimant_name']}\n")
    if doc_type == "repair estimate":
        return (f"{s['fax_hdr']} FROM:{rng.choice(SHOPS)}\n{rng.choice(SHOPS)}  ESTIMATE OF RECORD\n"
                f"ESTIMATE DATE: {mdy(s['est_d'], 'mdy4')}\nCUSTOMER: {g['claimant_name']}\n"
                f"INSURANCE: CALDWELL MUTUAL {('POLICY ' + pol) if pol else ''}\nDATE OF LOSS: {s['loss_txt']}\n"
                f"VEHICLE: 2019 Honda CR-V  FRONT BUMPER, HOOD\nTOTAL: ${rng.randint(900, 9800):,}.00\n")
    if doc_type == "police report":
        return (f"{s['fax_hdr']} FROM:HARTFORD PD RECORDS\nHARTFORD POLICE DEPARTMENT  ACCIDENT REPORT\n"
                f"REPORT NO: {g['police_report_ref']}\nDATE: {s['loss_txt']}  TIME: {rng.randint(6, 22)}:{rng.randint(10, 59)}\n"
                f"LOCATION: {g['loss_location']}\nOPERATOR 1: {g['claimant_name']}  INS: CALDWELL MUTUAL {pol or ''}\n"
                f"OPERATOR 2: {g['other_party'] or 'NONE'}\nINJURIES: {'YES' if g['injury_reported'] == 'yes' else 'NONE REPORTED'}\n")
    if doc_type == "medical bill":
        return (f"RECEIVED {s['stamp']} CALDWELL MUTUAL MAILROOM\nCAPITOL REGION MEDICAL GROUP  PATIENT STATEMENT\n"
                f"STATEMENT DATE: {mdy(s['est_d'], 'mdy4')}\nPATIENT: {g['claimant_name']}\n"
                f"DATE OF SERVICE: {mdy(s['svc_d'], 'mdy4')}\nCLAIM REF: {s['claim_id']}\nAMOUNT DUE: ${rng.randint(120, 4800):,}.00\n")
    if doc_type == "adjuster note":
        return email_wrap(rng, g, s, f"ADJ NOTE {s['claim_id']} {mdy(s['est_d'], 'mdy2')} TW: spoke w/ insd "
                          f"{g['claimant_name']} re {s['narr']} {mdy(s['loss_d'], 'mdy2')}. "
                          f"{'clmt injured' if g['injury_reported'] == 'yes' else 'no inj'}. "
                          f"{('PR# ' + g['police_report_ref']) if g['police_report_ref'] else ''}", internal=True)
    # photo log
    return email_wrap(rng, g, s, f"PHOTO LOG {s['claim_id']}\nIMG_0{rng.randint(100, 999)}.jpg front\n"
                      f"IMG_0{rng.randint(100, 999)}.jpg rear\nIMG_0{rng.randint(100, 999)}.jpg interior\n", internal=True)


def sent_line(d, rng):
    return f"Sent: {weekday(d)}, {MONTHS[d[1] - 1]} {d[2]}, {d[0]} {rng.randint(7, 11)}:{rng.randint(10, 59)} AM"


def email_wrap(rng, g, s, body, internal=False):
    to = "claims@caldwellmutual.example"
    if internal:
        return f"From: Tom Whitfield <twhitfield@caldwellmutual.example>\n{sent_line(s['recv_d'], rng)}\nTo: {to}\n\n{body}\n"
    first = (g["claimant_name"] or "x").split()[0]
    if s["forwarded"]:
        inner = add_days(s["recv_d"], -rng.randint(2, 6))
        return (f"From: {s['agent']} <{s['agent'].split()[0].lower()}@agency.example>\n{sent_line(s['recv_d'], rng)}\n"
                f"To: {to}\nSubject: FW: claim\n\nPlease see below from our client.\n-----Original Message-----\n"
                f"From: {g['claimant_name']} <{first.lower()}@example.net>\n{sent_line(inner, rng)}\n\n{body}\nThanks, {first}\n")
    if s["agent_sender"]:
        return (f"From: {s['agent']} <{s['agent'].split()[0].lower()}@agency.example>\n{sent_line(s['recv_d'], rng)}\n"
                f"To: {to}\nSubject: New loss\n\nOur client {g['claimant_name']} reports the following. {body}\n"
                f"{s['agent']} | {rng.choice(AGENCIES)}\n")
    return (f"From: {g['claimant_name']} <{first.lower()}@example.net>\n{sent_line(s['recv_d'], rng)}\nTo: {to}\n"
            f"Subject: Claim\n\nHi, {body}\nThanks, {first}\n")


def make_doc(i, rng, p, base=None):
    """One document. `base` (from a sample manifest row) fixes doc type, policy, loss date and OCR confidence."""
    base = dict(base or {})
    doc_type = base.get("doc_type") or pick(rng, p.doc_type)
    if "ocr_confidence" not in base and p.scanned_below:
        base["ocr_confidence"] = draw_ocr(rng, p.ocr)
        if base["ocr_confidence"] < p.scanned_below:
            base["channel"] = "fax" if rng.random() < 0.7 else "mail"
    channel = base.get("channel") or pick(rng, p.channel)
    if "channel" not in base:   # a manifest channel (a scanned low-OCR file) wins over the usual routing
        if doc_type in ("photo log", "adjuster note"):
            channel = "email"
        if doc_type in ("police report", "repair estimate") and channel == "email":
            channel = "fax"
        if doc_type == "medical bill":
            channel = "mail"
    loss_type = pick(rng, {k: 1 for k in NARRATIVES}) if doc_type != "police report" else "AUTO-COLL"
    if doc_type == "repair estimate":
        loss_type = "AUTO-COLL"
    if "loss_date" in base:
        y, m, d = (int(x) for x in base["loss_date"].split("-"))
        loss_d = (y, m, d)
    else:
        loss_d = (2026, rng.randint(1, 8), rng.randint(1, 28))
    recv_d = add_days(loss_d, rng.randint(1, 9))
    if "policy_number" in base:
        policy = base["policy_number"] or None
    else:
        policy = None if rng.random() < p.no_policy else f"HP{rng.randint(100000, 999999)}"
    claimant = base.get("claimant") if base.get("claimant", "").count(" ") == 1 and not base.get("claimant", "").startswith("claimant") else name(rng)
    street = f"{rng.randint(10, 2400)} {rng.choice(STREETS)}"
    town = rng.choice(TOWNS)
    lstyle = pick(rng, p.location_style)
    loc = f"{street}, {town}" if lstyle == "street" else (f"I-84 near exit {rng.randint(39, 61)}, {town}" if lstyle == "highway"
                                                          else f"the Stop and Shop lot on {rng.choice(STREETS)}, {town}")
    loc_txt = (f"at {loc}" if lstyle == "street" else f"on {loc}" if lstyle == "highway" else f"in {loc}")
    auto = loss_type.startswith("AUTO")
    party = name(rng) if auto and loss_type == "AUTO-COLL" else None
    police = (f"HPD-26-{rng.randint(100000, 999999)}" if (auto and rng.random() < 0.7) or doc_type == "police report" else None)
    injured = loss_type in INJURY_LOSS or (auto and rng.random() < 0.2) or doc_type == "medical bill"
    spanish = rng.random() < p.spanish and doc_type == "first notice of loss"
    pools = list(p.narrative_pools)
    pool = rng.choices(pools, weights=list(p.pool_weights))[0]
    opts = NARRATIVES[loss_type].get("es" if spanish else pool) or NARRATIVES[loss_type]["plain"]
    narr = rng.choice(opts)
    g = gold_record(rng, doc_type, channel, loss_type, policy, loss_d, recv_d, loc, party, police, injured, claimant)
    ds = "dmy_es" if spanish else (pick(rng, p.date_style) if doc_type == "first notice of loss" else "mdy4")
    pstyle = pick(rng, p.party_style)
    party_txt = ""
    if party:
        party_txt = (f"The other driver, {party}, admitted fault. " if pstyle == "labeled"
                     else f"The other driver ({party}) gave me his insurance card. ")
    istyle = pick(rng, p.injury_style)
    if injured:
        injury_txt = ("My passenger hurt her neck and went to the ER. " if istyle == "plain"
                      else "My back has been sore ever since. ")
    else:
        injury_txt = "No one was hurt. " if istyle == "plain" else "Nobody needed an ambulance. "
    ocr = base.get("ocr_confidence") if "ocr_confidence" in base else draw_ocr(rng, p.ocr)
    est_d = add_days(recv_d, rng.randint(0, 3))
    ctx = dict(spanish=spanish, loss_txt=mdy(loss_d, ds), loss_d=loss_d, narr=narr, loc_txt=loc_txt,
               party_txt=party_txt, injury_txt=injury_txt,
               fax_hdr=f"{MONTHS[recv_d[1] - 1][:3].upper()}-{recv_d[2]:02d}-{recv_d[0]} {rng.randint(7, 18)}:{rng.randint(10, 59)}",
               fax_from=rng.choice(["FRONT DESK", "KINKOS 4471", "HOME FAX"]), fax_form=rng.random() < 0.6,
               stamp=f"{MONTHS[recv_d[1] - 1][:3].upper()} {recv_d[2]:02d} {recv_d[0]}", recv_d=recv_d,
               est_d=est_d, svc_d=add_days(loss_d, rng.randint(0, 2)),
               claim_id=base.get("claim_id", f"CM-{2026_00000 + i:010d}"),
               forwarded=channel == "email" and doc_type == "first notice of loss" and rng.random() < p.forwarded,
               agent_sender=False, agent=name(rng))
    if channel == "email" and doc_type == "first notice of loss" and not ctx["forwarded"]:
        ctx["agent_sender"] = rng.random() < p.agent_sender
    text = render(rng, doc_type, channel, g, ctx)
    if channel in ("fax", "mail"):
        text = ocr_noise(text, ocr, rng)
    tags = []
    if channel in ("fax", "mail") and ocr < 0.80:
        tags.append("faded scan")
    if doc_type == "first notice of loss" and not policy:
        tags.append("no policy number")
    if ctx["agent_sender"]:
        tags.append("agent sender")
    if ctx["forwarded"]:
        tags.append("forwarded chain")
    if ds in ("mdy2", "written") and doc_type == "first notice of loss":
        tags.append("short or written date")
    if spanish:
        tags.append("Spanish-language")
    if doc_type != "first notice of loss":
        tags.append("not a first notice")
    return dict(id=f"D{i:04d}", doc_type=doc_type, channel=channel, ocr_confidence=ocr if channel != "email" else None,
                text=text, gold=g, tags=tags)


def generate(p, n, seed):
    rng = random.Random(seed)
    return [make_doc(i, rng, p) for i in range(n)]


# Synthetic v1: what the FDE built in weeks one to six from discovery notes and the claims-system schema.
V1 = Profile(name="synthetic v1 (discovery schema, happy path)",
             doc_type={"first notice of loss": 1.0}, channel={"email": 0.4, "fax": 0.3, "mail": 0.3})
