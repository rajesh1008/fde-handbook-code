"""Try It Yourself exercises for Chapter 4.
  a  Greystone: an owner who is named but holds no authority over the thing he owns
  b  ask the oversight profile for 99% and watch it refuse
  c  Pennant: lint 'works on any document' against the layout inventory"""
import sys
from checklists import greystone_sales_demo
from oversight import simulate, profile, SYSTEMS
from promise_rewrite import Claim, lint


# Pennant's layout inventory after the first week (Chapter 3 [CHECK ch03]): 11 countries, 40+ layouts.
PENNANT_LAYOUTS = {"EDI 214 status message": 1, "carrier proof-of-delivery scan": 27, "customs form": 11,
                   "driver phone photo": 1, "free-text email exception": 1}
PENNANT_COVERED = {"EDI 214 status message"}   # the one layout the sales demo matched


def a():
    print(greystone_sales_demo().assess(day=0).summary())


def b():
    rows = simulate(**SYSTEMS["pipeline A"])
    for tg in (0.98, 0.99):
        p = profile(rows, tg)
        print(f"target {tg:.0%}: " + ("no threshold reaches it on the calibration half; everything is reviewed"
                                      if p["threshold"] is None else
                                      f"review {p['review_share']:.1%}, held-out lower bound {p['lower']:.1%}"))


def c():
    promise = Claim("works on any document you receive", "vendor position")
    print("as sold:", lint(promise) or "pass")
    inventory, covered = PENNANT_LAYOUTS, PENNANT_COVERED
    total = sum(inventory.values())
    print(f"layout inventory: {total} layouts across {len(inventory)} kinds; demo covered "
          f"{sum(inventory[k] for k in covered)} ({sum(inventory[k] for k in covered) / total:.0%})")
    rewrite = Claim("coverage reported per layout against the 41-layout inventory; uncovered layouts route to "
                    "the exceptions team unchanged", "proposed design",
                    inventory="Pennant layout inventory v1, 41 layouts, owner Jenna Ruiz")
    print("rewritten:", lint(rewrite) or "pass")


if __name__ == "__main__":
    for arg in sys.argv[1:] or ["a", "b", "c"]:
        print(f"--- exercise {arg}")
        {"a": a, "b": b, "c": c}[arg]()
