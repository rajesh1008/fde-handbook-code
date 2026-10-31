"""Figure 29.14: Signature 12 after the first month, days 141 to 170 (Listing 29.9)."""
from _common import S, js  # noqa: F401  (sets paths)
import signature12
m = js("month")["out"]
t = lambda n: (f"{m[n]['median']:.0f} s" if m[n]["median"] < 120 else f"{m[n]['median'] / 60:.0f} min")
signature12.STATES.setdefault("ch29-month", dict(
    version="Caldwell days 141 to 170",
    rows=[("unit", f"{m['1']['runs']} runs", t("1") + " · $0"), ("component", f"{m['2']['runs']} runs", t("2") + f" · ${m['2']['cost']:.2f}"),
          ("integration", f"{m['3']['runs']} runs", t("3") + f" · ${m['3']['cost']:.2f}"),
          ("system", f"{m['4']['runs']} runs", t("4") + f" · ${m['4']['cost']:.2f}"), ("operational", "30 days", "daily · $1.35")],
    foot="blocked 2: #212 at L2, #231 at L1", changed=(1, 2, "gate")))
signature12.render("ch29-month", "fig29-14", __file__)
