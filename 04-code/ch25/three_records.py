"""Listing 25.5: the recommendation, the human response and the final outcome as three joinable records,
against one record that each step overwrites. Shadow week, days 111 to 115."""
import _paths  # noqa: F401
import random, statistics
from fieldkit.actions import ActionLedger, Recommendation, Response, Outcome
from sim import documents, FIELDS

docs = [d for day in range(111, 116) for d in documents(238, day, seed=day) if d["kind"] == "fnol"]
rng, led, single = random.Random(25), ActionLedger(), {}
secs = []
for d in docs:
    rid = f"R-{d['doc_id']}"
    led.recommend(Recommendation(rid, d["doc_id"], d["payload"], "intake-agent 0.9 / extract-2026-04", d["day"]))
    single[rid] = dict(d["payload"])
    r = rng.random()
    if d["error"]:
        verdict = "edited" if r < 0.80 else ("rejected" if r < 0.84 else "accepted")
    else:
        verdict = "accepted" if r < 0.95 else ("edited" if r < 0.975 else "rejected")
    pay = dict(d["gold"]) if verdict == "edited" else (dict(d["payload"]) if verdict == "accepted" else None)
    s = int(rng.gauss(95 if verdict != "accepted" else 48, 15)); secs.append(s)
    led.respond(Response(rid, "adjuster", verdict, pay, s, d["day"]))
    final = dict(d["gold"])
    if rng.random() < 0.012:                       # the production keyer's own slip
        final["zip"] = final["zip"][:-1] + "0"
    led.outcome(Outcome(d["doc_id"], "claims-core production extract, next morning", final, d["day"] + 1))
    single[rid] = pay or single[rid]               # the one-record design: the response overwrites...
    single[rid] = final                            # ...and the outcome overwrites again
sb = led.scoreboard(FIELDS)
n = sb["recommendations"]
print(f"three records: {n} recommendations, {sb['with_outcome']} outcomes joined by document")
print(f"  reviewer verdicts: accepted {sb['accepted']}  edited {sb['edited']}  rejected {sb['rejected']}")
print(f"  recommendation equals final record on all six fields: {sb['rec_matches_outcome']} "
      f"({sb['rec_matches_outcome'] / n:.1%})  scored by code against the production extract")
print(f"  accepted unchanged but final record differs: {sb['accepted_but_outcome_differs']}")
print(f"  edited and the edit equals final record: {sb['edit_matches_outcome']} of {sb['edited']}")
vs = [led.resps[f"R-{d['doc_id']}"] for d in docs]
print(f"  median review seconds: accepted {statistics.median(r.seconds for r in vs if r.verdict == 'accepted'):.0f}"
      f"  edited {statistics.median(r.seconds for r in vs if r.verdict == 'edited'):.0f}")
one = sum(1 for rid in single if single[rid] == led.outs[rid[2:]].payload)
print(f"one overwritten record: 'agent agrees with final' {one} of {n} ({one / n:.1%}); "
      f"rubber-stamped errors visible: 0")
missed = [r for r in led.join(FIELDS) if r["verdict"] == "accepted" and not r["rec_eq_out"]]
err_acc = sum(1 for r in missed if next(d for d in docs if d["doc_id"] == r["case"])["error"])
print(f"  of the accepted-but-different: agent error the reviewer missed {err_acc}, "
      f"production keyer slip {len(missed) - err_acc}")
