"""Label-free features of a Caldwell document, for the representativeness report. Nothing here reads gold values."""
import re


def kind(text):
    if "ESTIMATE OF RECORD" in text:
        return "repair estimate"
    if "ACCIDENT REPORT" in text:
        return "police report"
    if "PATIENT STATEMENT" in text:
        return "medical bill"
    if "PHOTO LOG" in text:
        return "photo log"
    if "ADJ NOTE" in text:
        return "adjuster note"
    return "first notice"


def date_style(text):
    body = "\n".join(x for x in text.splitlines() if not x.startswith("Sent:"))
    if re.search(r"\b\d{1,2}/\d{1,2}/\d{4}\b", body):
        return "mm/dd/yyyy"
    if re.search(r"\b\d{1,2}/\d{1,2}/\d{2}\b", body):
        return "mm/dd/yy"
    if re.search(r"\bthe \d{1,2}(st|nd|rd|th)\b|\b(January|February|March|April|May|June|July|August)\b", body):
        return "written"
    return "none found"


def ocr_bin(c):
    if c is None:
        return "born digital"
    return "<0.80" if c < 0.80 else ("0.80-0.90" if c < 0.90 else ">=0.90")


def features(doc):
    t = doc["text"]
    n = len(t.split())
    return {
        "channel": doc["channel"],
        "document kind": kind(t),
        "ocr band": ocr_bin(doc.get("ocr_confidence")),
        "length band": "<40 words" if n < 40 else ("40-80 words" if n < 80 else "80+ words"),
        "forwarded": "yes" if "-----Original Message-----" in t else "no",
        "sender": "agency" if "@agency.example" in t else ("internal" if "@caldwellmutual" in t.split("\n")[0] else "claimant or other"),
        "date style": date_style(t),
        "language": "es" if re.search(r"\b(Hola|poliza|heridos)\b", t) else "en",
        "policy number": "present" if re.search(r"\b[HN]P[0-9OolSBZb]{6}\b", t) else "absent",
    }
