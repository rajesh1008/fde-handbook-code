"""Synthetic v2: a profile measured from the 200-file sample, plus Tom Whitfield's field phrasings.

Only aggregate counts leave the sample: shares of document types, channels, exception tags, date styles, the
OCR confidence column of the day-47 manifest (numbers, no text) and the location styles the adjusters keyed. No sentence from a real
file is copied into the generator; the narrative phrasings come from a list Whitfield wrote out on day 54.
"""
from collections import Counter
from claimsgen import Profile
from features import features
from fieldkit.fixtures import caldwell_sample


def mix(counter):
    n = sum(counter.values())
    return {k: round(v / n, 3) for k, v in sorted(counter.items())}


def profile_from_sample(docs):
    fnol = [d for d in docs if d["doc_type"] == "first notice of loss"]
    emails = [d for d in fnol if d["channel"] == "email"]
    fwd = sum("forwarded chain" in d["tags"] for d in emails)
    agent = sum("agent sender" in d["tags"] for d in emails)
    dates = Counter(features(d)["date style"] for d in fnol if "Spanish-language" not in d["tags"])
    ds = {"mdy4": dates.get("mm/dd/yyyy", 0), "mdy2": dates.get("mm/dd/yy", 0), "written": dates.get("written", 0)}
    locs = Counter("highway" if "I-84" in (d["gold"]["loss_location"] or "") else
                   "landmark" if " lot on " in (d["gold"]["loss_location"] or "") else "street"
                   for d in fnol if d["gold"]["loss_location"])
    parties = Counter("parenthetical" if "other driver (" in d["text"] else "labeled"
                      for d in fnol if d["gold"]["other_party"])
    return Profile(
        name="synthetic v2 (profile from the 200, Whitfield phrasings)",
        doc_type=mix(Counter(d["doc_type"] for d in docs)),
        channel=mix(Counter(d["channel"] for d in fnol)),
        ocr=("list", sorted(r["ocr_confidence"] for r in caldwell_sample())),   # the day-47 manifest column
        scanned_below=0.80,
        agent_sender=round(agent / max(len(emails) - fwd, 1), 3),
        forwarded=round(fwd / max(len(emails), 1), 3),
        date_style=mix(Counter({k: v for k, v in ds.items() if v})),
        spanish=round(sum("Spanish-language" in d["tags"] for d in fnol) / len(fnol), 3),
        no_policy=round(sum("no policy number" in d["tags"] for d in fnol) / len(fnol), 3),
        narrative_pools=("plain", "ambiguous", "field"), pool_weights=(0.45, 0.10, 0.45),
        location_style=mix(locs),
        party_style=mix(parties) if parties else {"labeled": 1.0},
        injury_style={"plain": 0.7, "field": 0.3})
