# Chapter 22 lab: Pennant's paper and EDI feed

**Deterministic stand-in.** No Pennant document, carrier, booking or model is used here. `week.py` generates a seeded shadow week (days 124 to 130, 2,100 documents across EDI 210, flatbed scans and phone photos, 780 bookings, 11 carriers) with known defects and known discrepancies, so every number in the chapter can be regenerated exactly. The "vision reader" and "OCR layer" are functions that reproduce the behaviors the chapter discusses (a vision reader that fills an occluded identifier from context; an OCR layer that reports low zone confidence); they are not models.

Run everything: `bash make_outputs.sh` (writes `output/*.txt`, runs `test_ch22.py` and the fieldkit tests).

| File | What it is |
|---|---|
| `week.py` | the seeded feed: channels, kinds, defects, discrepancies, bookings with sibling shipments, versioned FX rows, X12 210 text |
| `pipeline.py` | door (scorer `pennant-qs-1.0` / `pennant-qs-1.1`), linkage (`first key` / `two keys`), rules R1 to R6, routing, lineage, grading against the reconciliation team's ruling |
| `shadow_week.py` | Listing 22.1: the week, `v1` (as run) or `v2` (day-133 fix) |
| `thumb.py` | failure injection: a bill of lading photographed with a thumb over the container number |
| `steps.py` | the fifteen steps N01 to N15 against the Chapter 9 design |
| `routing.py` | queues, owners and one exception packet |
| `scorecard.py` | three definitions of matched, the scorecard by channel, lineage totals |
| `tryit.py` | the three Try It Yourself exercises (`a`, `b`, `c`) |
| `breakdown.py` | the per-day and per-channel counts the figures plot |
| `test_ch22.py` | five tests, including "the thumb case never matches" |

Uses fieldkit as of Chapter 21 (`quality`, `lineage`, `connectors`, `autonomy`); no new module.
