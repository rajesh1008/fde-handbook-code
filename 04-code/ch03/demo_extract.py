"""DEMO MODEL STAND-IN (deterministic; no model is called).

The day-two demo ran a hosted model behind a notebook. There are no model keys on the machine that builds
this book, and a model's answers would change between runs anyway, so this module stands in for the demo:
a fixed set of rules that reproduces the demo's *behavior* on the layout it was built for, a clean
typed claim form with labels such as "Policy Number:" and "Date of Loss:".

The rules are the honest part. Each one is something the demo actually relied on:
  * labels from Northlight's own demo form,
  * the sender's display name when there is no "Insured:" label,
  * US numeric dates with a four-digit year,
  * the upload time as the received date (the demo app's meaning, not Caldwell's),
  * a keyword map from the demo's loss vocabulary to Caldwell's codes, written on day two,
  * an "Injuries:" value of "None" or "No ..." means no injury; with no such label, "injur", "hurt",
    "ambulance" or "hospital" anywhere in the text means an injury was reported,
  * an "email" channel only when there is a From: line with an address; everything else is "upload".
"""
import re

STAND_IN_LABEL = "DEMO MODEL STAND-IN (deterministic; no model called)"

_LOSS_MAP = [  # first match wins, in the order the demo author wrote them
    (r"rear-end|collision|struck|hit ", "AUTO-COLL"),
    (r"vehicle stolen|car stolen", "AUTO-COMP"),
    (r"stolen|stole|theft|break-in|broken into", "PROP-THEFT"),
    (r"fire", "PROP-FIRE"),
    (r"water|pipe|leak", "PROP-WATER"),
    (r"wind|storm|hail|tree", "PROP-WIND"),
]


def _label(text, *labels):
    for lab in labels:
        m = re.search(rf"^{lab}\s*[:#]?\s*(.+)$", text, re.M | re.I)
        if m and m.group(1).strip():
            return m.group(1).strip()
    return None


def _date(text, label_first=True):
    val = _label(text, "Date of Loss") if label_first else None
    src = val if val else text
    m = re.search(r"\b(\d{1,2})\s*/\s*(\d{1,2})\s*/\s*(\d{2,4})\b", src)
    if not m:
        return None
    mo, d, y = (int(g) for g in m.groups())
    return f"{y:04d}-{mo:02d}-{d:02d}"  # a two-digit year comes out as year 0026


def extract(doc):
    t = doc["text"]
    out = {}
    pol = re.search(r"\b[A-Z]{2}\d{6}\b", t)
    out["policy_number"] = pol.group(0) if pol else None

    name = _label(t, "Insured")
    if not name:
        frm = re.search(r"^From:\s*([^<\n]+?)\s*<", t, re.M)
        name = frm.group(1) if frm else None
    out["claimant_name"] = name

    out["loss_date"] = _date(t)
    out["date_received"] = doc["uploaded"]

    low = t.lower()
    typ = _label(t, "Type of Loss")
    hay = (typ or low).lower()
    out["loss_type"] = next((code for pat, code in _LOSS_MAP if re.search(pat, hay)), "OTHER")

    loc = _label(t, "Location", "Loss Location")
    if not loc:
        m = re.search(r"\b(\d+ [A-Z][a-z]+(?: [A-Z][a-z]+)* (?:St|Ave|Rd|Dr|Ln|Ter)\b,? [A-Z][a-z]+(?: [A-Z][a-z]+)?)", t)
        loc = m.group(1) if m else None
    out["loss_location"] = loc

    inj = _label(t, "Injuries")
    if inj is not None:
        out["injury_reported"] = "no" if re.match(r"(none|no\b)", inj, re.I) else "yes"
    else:
        out["injury_reported"] = "yes" if re.search(r"injur|hurt|ambulance|hospital", low) else "no"

    ref = _label(t, "Police Report")
    if not ref:
        m = re.search(r"report number\s+(\S+?)[.,\s]", t, re.I)
        ref = m.group(1) if m else None
    out["police_report_ref"] = ref

    out["other_party"] = _label(t, "Other Party")
    out["intake_channel"] = "email" if re.search(r"^From:.*@", t, re.M) else "upload"
    return out
