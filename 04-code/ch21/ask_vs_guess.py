"""Listing 21.4: request missing information instead of guessing it."""
import _paths  # noqa: F401
from fieldkit.quality import request_for
from pennant import feed, COUNTRIES, u
from checks import scorer, MEANINGS

if __name__ == "__main__":
    docs = feed()
    for d in docs:   # the day-64 sample had a batch of invoices with no currency printed
        if d["kind"] in ("commercial invoice", "freight invoice", "customs declaration") and d["country"] != "US" and u(d["doc_id"], "nocur") < 0.12:
            d["currency"] = None
    s = scorer()
    held = [(d, s.score(d)) for d in docs if d["currency"] is None and d["kind"] in ("commercial invoice", "freight invoice", "customs declaration")]
    wrong = sum(1 for d, _ in held if COUNTRIES[d["country"]][0] != d["_true_currency"])
    usd_value = sum(d["total"] for d, _ in held if COUNTRIES[d["country"]][0] != d["_true_currency"])
    print(f"documents with no currency printed: {len(held)}")
    print(f"guess (currency of the country): wrong on {wrong} ({wrong / len(held):.0%}), face value misstated {usd_value:,.2f}")
    answered = [d for d, _ in held if u(d["doc_id"], "answer") < 0.80]
    hours = sorted(4 + 40 * u(d["doc_id"], "hrs") for d in answered)
    print(f"ask (request to sender): answered {len(answered)} ({len(answered) / len(held):.0%}), wrong 0, "
          f"median wait {hours[len(hours) // 2]:.0f} h, still open {len(held) - len(answered)}")
    print("example request:")
    print("  " + request_for(held[0][1], "ap@harborline.example", MEANINGS).replace("\n", "\n  "))
