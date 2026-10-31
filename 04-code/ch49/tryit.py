"""Try It Yourself 49.A to 49.C. Deterministic stand-in."""
import sys
import _paths  # noqa: F401
import world
from world import year_one

p = sys.argv[1]
if p == "a":
    print("49.A: Greystone, when must it go live for two years to break even?")
    import retro
    retro.greystone()
elif p == "b":
    print("49.B: Pennant if the night duty had been booked and the managed service never sold")
    base = year_one("pennant")
    world.CUST["pennant"]["managed_from"] = None
    y = year_one("pennant")
    print(f"  with managed service   margin {base['margin']:.1%}  gross profit ${base['gp']:,.0f}")
    print(f"  without                margin {y['margin']:.1%}  gross profit ${y['gp']:,.0f}")
    world.AFTER["pennant"]["night duty never booked"] = 0
    y2 = year_one("pennant")
    print(f"  without, night duty left unbooked: margin {y2['margin']:.1%} (the ledger flatters by "
          f"{(y2['margin'] - y['margin']) * 100:.1f} points)")
else:
    print("49.C: give the fourth customer a model-risk function and rerun the check")
    import fourth
    fourth.INDUSTRY_GATES.clear()
    fourth.REGISTER["model-risk officer"] = ("Nadia Fern", "model validation")
    rows, probs = fourth.check(fourth.SIGNED, {})
    for pr in probs:
        print("  REFUSED " + pr)
    print(f"problems: {len(probs)}")
