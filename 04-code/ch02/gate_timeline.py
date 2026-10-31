"""Listing 2.6 driver: planned day for each of the five gates, per customer, deal sheet and field estimate."""
from contracts import CONTRACTS, DEAL_SHEET, FIELD_ESTIMATE
from margin import gate_days, GATES


def main():
    print("GATE TIMELINE  planned engagement day per gate")
    print(f"{'customer':<18}{'plan':<16}" + "".join(f"{g.split()[0][:9]:>10}" for g in GATES))
    for k, c in CONTRACTS.items():
        for plans in (DEAL_SHEET, FIELD_ESTIMATE):
            d = gate_days(plans[k])
            print(f"{c.customer:<18}{plans[k].label:<16}" + "".join(f"{d[g]:>10}" for g in GATES))
    print("nine-month line: day 270")


if __name__ == "__main__":
    main()
