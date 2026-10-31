"""Listing 21.2: variability as a first-class problem. Layout volume, and the parser that
read 1.234,50 as 1.2345 without complaint."""
import _paths  # noqa: F401
from collections import Counter
from pennant import feed, layouts, volumes, COUNTRIES


def naive_amount(s: str) -> float:
    return float(s.replace(",", ""))


def locale_amount(s: str, sep: str) -> float:
    return float(s.replace(".", "").replace(",", ".")) if sep == "," else float(s.replace(",", ""))


if __name__ == "__main__":
    docs = feed()
    v = volumes()
    lay = layouts()
    order = sorted(range(41), key=lambda i: -v[i])
    top = sum(v[i] for i in order[:12])
    print(f"documents {len(docs)}, layouts {len(lay)}, kinds {len({l['kind'] for l in lay})}, countries {len({l['country'] for l in lay})}")
    print(f"top 12 layouts carry {top} documents ({top / len(docs):.1%}); the last 20 carry {sum(v[i] for i in order[21:])}")
    print("channels:", dict(Counter(d["channel"] for d in docs)))
    silent, loud, ok = Counter(), Counter(), Counter()
    for d in docs:
        sep = COUNTRIES[d["country"]][1]
        try:
            x = naive_amount(d["amount_text"])
        except ValueError:
            loud[d["country"]] += 1
            continue
        if abs(x - locale_amount(d["amount_text"], sep)) > 0.005:
            silent[d["country"]] += 1
        else:
            ok[d["country"]] += 1
    print("amounts, one parser for every layout:")
    for c in COUNTRIES:
        n = silent[c] + loud[c] + ok[c]
        print(f"  {c}: {n:>4} docs, silently wrong {silent[c]:>4}, failed loudly {loud[c]:>3}")
    print(f"  total silently wrong {sum(silent.values())} ({sum(silent.values()) / len(docs):.1%}), loud {sum(loud.values())}")
    fixed = sum(abs(locale_amount(d['amount_text'], COUNTRIES[d['country']][1]) - d['_printed']) > 0.005 for d in docs)
    print(f"amounts, parser chosen by the layout's registered locale: silently wrong {fixed}")
    amb = sum(1 for d in docs if d["date_order"] == "dmy" and d["day"] <= 12 and d["day"] != d["month"])
    bad = sum(1 for d in docs if d["date_order"] == "dmy" and d["day"] > 12)
    print(f"dates in day-first layouts read month-first: {amb} silently wrong, {bad} rejected as impossible")
