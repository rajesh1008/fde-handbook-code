"""Chapter 15, Try It Yourself. Run: python tryit.py a|b|c"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "fieldkit"))
from fieldkit.fixtures import caldwell_sample
from fieldkit.histories import (caldwell_history, caldwell_policy, caldwell_fields, greystone_history,
                                rung_reached_days)


def a():
    """Exercise A: the day-47 ask was sent and nothing happened. What do the rules say on day 60?"""
    h = caldwell_history()
    h.events = [e for e in h.events if not (e[1] == "claims-core-readonly" and e[0] > 47)]
    pol = caldwell_policy()
    pol.record("claims-core-readonly", 47, 1, "Daniel Reyes")
    esc, _, _ = pol.review(h.replay(60), 60)
    for e in esc:
        if e.key == "claims-core-readonly":
            print(e.note())
            print("rule:", e.reason)


def b():
    """Exercise B: the export includes the payee bank details the request said to redact."""
    rows = caldwell_sample()
    for r in rows:
        r["bank_account"] = "redacted?"
    res = caldwell_fields().assess("caldwell-claims-sample", rows, 41, 47)
    print(res.summary().split("\nFIELDS")[0])
    print("blocking:", "; ".join(res.blocking))


def c():
    """Exercise C: which Greystone delay set day 112? Move one event at a time and replay."""
    def sampled_day(edit):
        h = greystone_history()
        edit(h)
        return rung_reached_days(h.replay(200)).get("sampled")

    def our_answers_on_day_20(h):
        # our answers go back 27 days earlier; Sam Oakley's review then takes the same 29 days
        h.events = [(d - 27 if k == "azure-subscription" and d >= 47 else d, k, ch) for d, k, ch in h.events]

    def referral_filed_properly_on_day_10(h):
        h.events = [(d - 51 if k == "referral-sample" and d >= 61 else d, k, ch) for d, k, ch in h.events]

    rows = [("as it happened", lambda h: None),
            ("our 26 answers sent on day 20", our_answers_on_day_20),
            ("referral filed as a record on day 10", referral_filed_properly_on_day_10),
            ("both", lambda h: (our_answers_on_day_20(h), referral_filed_properly_on_day_10(h)))]
    for label, edit in rows:
        print(f"{label:<40}sampled rung on day {sampled_day(edit)}")


if __name__ == "__main__":
    {"a": a, "b": b, "c": c}[sys.argv[1] if len(sys.argv) > 1 else "a"]()
