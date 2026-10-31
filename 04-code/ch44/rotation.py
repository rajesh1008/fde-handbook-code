"""Listing 44.7: monthly load index per person, red flags, and a replay under the rotation policy."""
import world as W
from practice import load_series, red_months
print("load index = travel days/10 + overnight pages/4 + 0.25 per month on one account beyond six")
print("person          " + " ".join(f"{m:>5}" for m in range(1, 13)))
for p in W.LOAD:
    s = load_series(p)
    print(f"{p:<16}" + " ".join(f"{'.' if v is None else f'{v:.2f}':>5}" for v in s))
print()
for p in W.LOAD:
    s = load_series(p)
    reds = red_months(s)
    if reds:
        print(f"RED {p}: two consecutive months >= {W.LOAD_RED} first in month {reds[0]}; red months {reds}")
    tenure_flag = [m for m in range(12) if W.LOAD[p]["account"][m] and
                   sum(1 for k in range(m + 1) if W.LOAD[p]["account"][k] == W.LOAD[p]["account"][m]) > W.MAX_MONTHS_ON_ACCOUNT]
    if tenure_flag and not reds:
        print(f"rotate {p}: beyond {W.MAX_MONTHS_ON_ACCOUNT} months on {W.LOAD[p]['account'][tenure_flag[0]]} from month {tenure_flag[0] + 1}")
print(f"\nreplay under policy (travel cap {W.TRAVEL_CAP} days, Pennant nights on a rota of {W.ROTA_DEPTH}, "
      f"rotate after {W.MAX_MONTHS_ON_ACCOUNT} months):")
for p in ("Maya Brooks", "lead FDE", "Callum Reid"):
    a, b = load_series(p), load_series(p, policy=True)
    print(f"  {p:<14} peak {max(v for v in a if v is not None):.2f} -> {max(v for v in b if v is not None):.2f}; "
          f"red months {len(red_months(a))} -> {len(red_months(b))}")
