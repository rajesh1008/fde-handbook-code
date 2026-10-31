"""EXTRACTOR STAND-IN (deterministic; no model is called). The build machine has no model keys, and a model's
answers vary between runs, so the chapter's pipeline is represented by fixed rules written the way the FDE's
prompts and post-processing were tuned: against synthetic v1, six weeks of clean first-notice documents.

`v1` is the pipeline as it stood on day 44. `v2` is the day-58 revision after the representativeness report
(it reads agency letters, forwarded chains, two-digit years, labels on other document types and Spanish keywords).
"""
import re

MONTHS = ["january", "february", "march", "april", "may", "june", "july", "august", "september", "october",
          "november", "december"]
KEYWORDS = [("AUTO-COLL", r"rear-ended|collided|hit by|crash|ran into"),
            ("AUTO-COMP", r"tree|branch|vandal|hail|windshield"),
            ("PROP-WATER", r"pipe|water|leak|flood"),
            ("PROP-FIRE", r"fire|smoke"),
            ("PROP-WIND", r"wind|shingle|storm"),
            ("PROP-THEFT", r"broken into|stolen|burglar|theft"),
            ("LIAB-BI", r"slipped|tripped|fell|bitten")]
KEYWORDS_V2 = [("PROP-WIND", r"storm brought a tree|gust|viento"),
               ("PROP-FIRE", r"fire hoses|incendio|caught and charred"),
               ("AUTO-COLL", r"rear-ended|collided|hit by|crash|ran into|stopped short|clipped|chocaron"),
               ("AUTO-COMP", r"tree|branch|vandal|hail|windshield|keyed|catalytic|arbol"),
               ("PROP-WATER", r"pipe|water|leak|flood|overflow|tuberia"),
               ("PROP-FIRE", r"fire|smoke"),
               ("PROP-WIND", r"wind|shingle|storm"),
               ("PROP-THEFT", r"broken into|stolen|burglar|theft|took the|robar"),
               ("LIAB-BI", r"slipped|tripped|fell|bitten|\bbit\b|resbalo")]
DATE4 = re.compile(r"\b(\d{1,2})/(\d{1,2})/(\d{4})\b")
DATE2 = re.compile(r"\b(\d{1,2})/(\d{1,2})/(\d{2})\b")
WRITTEN = re.compile(r"\b(" + "|".join(m.capitalize() for m in MONTHS) + r") (\d{1,2}), (\d{4})")


def _iso(m, d, y):
    m, d, y = int(m), int(d), int(y)
    if y < 100:
        y += 2000
    if not (1 <= m <= 12 and 1 <= d <= 31):
        return None
    return f"{y:04d}-{m:02d}-{d:02d}"


def _sent(line):
    m = WRITTEN.search(line)
    return _iso(MONTHS.index(m.group(1).lower()) + 1, m.group(2), m.group(3)) if m else None


def _label(text, label):
    m = re.search(rf"^{label}:\s*(.+?)\s*$", text, re.M)
    if not m:
        return None
    v = m.group(1).strip()
    return None if v.upper() in ("NONE", "NONE REPORTED", "") else v


def extract(doc, version="v1"):
    t = doc["text"]
    lines = t.splitlines()
    out = dict(intake_channel=doc["channel"])          # channel comes from the intake system, not the text
    v2 = version == "v2"
    # policy number
    m = re.search(r"\bHP\d{6}\b", t)
    if m:
        out["policy_number"] = m.group(0)
    else:
        f = re.search(r"(?i)policy(?:\s+(?:no\.?|number))?[:\s]+([A-Za-z0-9-]{2,})", t)
        out["policy_number"] = f.group(1) if f and not v2 else None
        if v2:
            n = re.search(r"\b[HN][P][0-9OolSBZb]{6}\b", t)
            out["policy_number"] = None if not n else "HP" + n.group(0)[2:].translate(str.maketrans("OolSBZb", "0015826"))
    # claimant
    claimant = _label(t, "CLAIMANT") or _label(t, "CUSTOMER") or _label(t, "PATIENT")
    op1 = re.search(r"^OPERATOR 1:\s*(.+?)\s+INS:", t, re.M)
    claimant = claimant or (op1.group(1) if op1 else None)
    if v2:
        c = re.search(r"Our client ([A-Z][a-z]+ [A-Z][a-z]+)", t) or re.search(r"insd ([A-Z][a-z]+ [A-Z][a-z]+)", t)
        if c:
            claimant = c.group(1)
        if "-----Original Message-----" in t:
            inner = t.split("-----Original Message-----", 1)[1]
            fm = re.search(r"^From: ([^<\n]+?) <", inner, re.M)
            claimant = fm.group(1) if fm else claimant
        if "PHOTO LOG" in t:
            claimant = None
    if not claimant:
        fm = re.search(r"^From: ([^<\n]+?) <", t, re.M)
        if fm and not (v2 and "Whitfield" in fm.group(1)):
            claimant = fm.group(1)
    if not claimant and "Sincerely," in t:
        i = lines.index("Sincerely,")
        claimant = lines[i + 1].strip() if i + 1 < len(lines) else None
    if not claimant and lines and lines[0].startswith(("JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP")):
        claimant = lines[-1].strip() or None
    out["claimant_name"] = claimant
    # loss date
    ld = _label(t, "DATE OF LOSS") or (_label(t, "DATE").split("  ")[0] if v2 and _label(t, "DATE") else None)
    loss = None
    if ld:
        m4 = DATE4.search(ld) or (DATE2.search(ld) if v2 else None)
        loss = _iso(*m4.groups()) if m4 else None
    else:
        body = "\n".join(x for x in lines if not x.startswith(("Sent:", "STATEMENT DATE", "ESTIMATE DATE")) or not v2)
        if v2 and ("PATIENT STATEMENT" in t or "PHOTO LOG" in t):
            body = ""
        m4 = DATE4.search(body)
        if m4:
            loss = _iso(*m4.groups())
            if v2 and "Hola" in t:
                loss = _iso(m4.group(2), m4.group(1), m4.group(3))
        elif v2 and DATE2.search(body):
            ds = DATE2.findall(body)
            loss = _iso(*ds[-1]) if ds else None
        else:
            w = WRITTEN.search("\n".join(x for x in lines if not x.startswith("Sent:")))
            loss = _iso(MONTHS.index(w.group(1).lower()) + 1, w.group(2), w.group(3)) if w else None
    out["loss_date"] = loss
    # date received
    sent = [x for x in lines if x.startswith("Sent:")]
    if sent:
        out["date_received"] = _sent(sent[0] if v2 else sent[-1])
    else:
        h = re.search(r"\b(JAN|FEB|MAR|APR|MAY|JUN|JUL|AUG|SEP|OCT|NOV|DEC)[- ](\d{2})[- ](\d{4})", t)
        out["date_received"] = _iso([m[:3].upper() for m in MONTHS].index(h.group(1)) + 1, h.group(2), h.group(3)) if h else None
    # loss type
    lt = None
    if not (v2 and ("ESTIMATE OF RECORD" in t or "PATIENT STATEMENT" in t or "PHOTO LOG" in t)):
        low = t.lower()
        for code, pat in (KEYWORDS_V2 if v2 else KEYWORDS):
            if re.search(pat, low):
                lt = code
                break
    if v2 and "ACCIDENT REPORT" in t:
        lt = "AUTO-COLL"
    out["loss_type"] = lt
    # location
    loc = _label(t, "LOCATION")
    if not loc:
        m = re.search(r"\b(?:at|outside) (\d+ [A-Z][a-z]+ (?:St|Ave|Rd|Dr|Ln|Way|Tpke)), ([A-Z][a-z]+(?: [A-Z][a-z]+)?)", t)
        loc = f"{m.group(1)}, {m.group(2)}" if m else None
        if v2 and not loc:
            m = re.search(r"\b(?:on|in|en) ((?:I-84 near exit \d+|the Stop and Shop lot on \d* ?[A-Z][a-z]+ (?:St|Ave|Rd|Dr|Ln|Way|Tpke)|\d+ [A-Z][a-z]+ (?:St|Ave|Rd|Dr|Ln|Way|Tpke)), [A-Z][a-z]+(?: [A-Z][a-z]+)?)", t)
            loc = m.group(1) if m else None
    out["loss_location"] = loc
    # injury
    inj = _label(t, "INJURIES")
    if inj:
        out["injury_reported"] = "yes" if inj.upper().startswith("YES") else "no"
    elif v2 and ("ESTIMATE OF RECORD" in t or "PHOTO LOG" in t):
        out["injury_reported"] = None
    elif v2 and "PATIENT STATEMENT" in t:
        out["injury_reported"] = "yes"
    else:
        low = t.lower()
        pos = re.search(r"hurt|injur|\ber\b|hospital|heridos\.|clmt injured" + (r"|sore" if v2 else ""), low)
        neg = re.search(r"no one was hurt|nobody was hurt|no injur|not injured|no hubo heridos|no inj\b", low)
        out["injury_reported"] = "yes" if pos and not neg else "no"
    # police report
    m = re.search(r"\b[A-Z]{2,4}-\d{2}-\d{6}\b", t)
    if not m and v2:
        m = re.search(r"\b[HN]PD-[0-9OolSBZb]{2}-[0-9OolSBZb]{6}\b", t)
    out["police_report_ref"] = (m.group(0) if not v2 else "HPD-" + m.group(0)[4:].translate(str.maketrans("OolSBZb", "0015826"))) if m else None
    # other party
    op = _label(t, "OTHER PARTY") or _label(t, "OPERATOR 2")
    if not op:
        m = re.search(r"other driver,? ([A-Z][a-z]+ [A-Z][a-z]+)", t) or (
            re.search(r"other driver \(([A-Z][a-z]+ [A-Z][a-z]+)\)", t) if v2 else None)
        op = m.group(1) if m else None
    out["other_party"] = op
    return out
