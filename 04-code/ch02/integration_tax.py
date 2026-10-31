"""Listing 2.2 driver: Pennant's margin as the integration tax rises. Model work held constant."""
from contracts import CONTRACTS, FIELD_ESTIMATE
from margin import year_one, with_


def main():
    c, base = CONTRACTS["pennant"], FIELD_ESTIMATE["pennant"]
    print("INTEGRATION TAX SENSITIVITY  Pennant Logistics  fixed price, model work 500 h")
    print(f"{'tax':>5}{'integ h':>9}{'months':>8}{'hours':>7}{'margin':>9}")
    for tax in (0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 4.0):
        p = with_(base, integration_tax=tax)
        y = year_one(c, p)
        print(f"{tax:>5.1f}{p.integration_h:>9,.0f}{p.months_to_production:>8.1f}{y.hours:>7,.0f}{y.margin:>9.1%}")
    for floor in (0.60, 0.40):
        hit = [t / 10 for t in range(0, 60) if year_one(c, with_(base, integration_tax=t / 10)).margin >= floor]
        print(f"highest tax that keeps margin at or above {floor:.0%}: "
              + (f"{max(hit):.1f}" if hit else "none, even at zero integration"))


if __name__ == "__main__":
    main()
