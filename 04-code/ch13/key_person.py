"""Key-person risk on both sides: single holders and concentration, at Pennant and Caldwell."""
from cadence_data import HOLDINGS
from fieldkit.cadence import bus_factor

if __name__ == "__main__":
    for customer, h in HOLDINGS.items():
        flags = bus_factor(h)
        print(f"KEY-PERSON RISK  {customer}  ({len(h)} capabilities)")
        for f in flags:
            print(f"  {f}")
