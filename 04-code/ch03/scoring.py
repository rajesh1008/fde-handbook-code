"""Field-level scoring against the customer's expert, and a first-pass cause for every miss."""
import re
from caldwell_docs import FIELDS


def norm(v):
    if v is None:
        return ""
    return re.sub(r"[^A-Z0-9]", "", str(v).upper())


def correct(pred, gold):
    return norm(pred) == norm(gold)


def cause(field, doc, pred, gold):
    """The FDE's first reading of why a field missed. A heuristic, written on day two, checked by Anne."""
    if field in ("date_received", "intake_channel"):
        return "definition: Caldwell's meaning differs"
    if field == "injury_reported" and pred == "yes" and gold == "no":
        return "negation read as a mention"
    if field == "loss_type":
        return "vocabulary: demo words, not Caldwell codes"
    if field == "claimant_name" and pred:
        if re.search(r"POLICY|P0LICY", str(pred), re.I):
            return "scan text: layout or OCR noise"
        return "wrong person: sender or insured, not claimant"
    if pred and field.endswith("date"):
        return "date convention"
    if doc["channel"] in ("fax", "mail"):
        return "scan text: layout or OCR noise"
    return "phrasing the demo never saw"


def score(docs, extract):
    rows = []
    for d in docs:
        pred = extract(d)
        for f in FIELDS:
            ok = correct(pred[f], d["gold"][f])
            rows.append(dict(doc=d["id"], channel=d["channel"], field=f, pred=pred[f], gold=d["gold"][f],
                             ok=ok, cause=None if ok else cause(f, d, pred[f], d["gold"][f])))
    return rows
