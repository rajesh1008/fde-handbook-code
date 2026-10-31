"""Listing 14.2 driver: every step of the electronic referral path through the decision tree (day 17)."""
import pipeline as pl
from decision_tree import CLASSES, SHORT, classify, split, share


def main(steps=pl.ELECTRONIC, title="Electronic referral path"):
    print(f"{title}: {len(steps)} steps")
    for s in steps:
        print(f"  {s.n} {s.name:<58} {SHORT[classify(s)]:<9} {s.michael}")
    sp = split(steps)
    print("  " + ", ".join(f"{c}: {sp[c]}" for c in CLASSES))
    print(f"  deterministic share {share(steps):.0%}; model steps {sp[CLASSES[2]] + sp[CLASSES[3]]}, "
          f"all draft only: {all(s.michael == 'draft only' for s in steps if classify(s) in CLASSES[2:])}")
    print("  Refused by Michael Hart (not built):")
    for what, why in pl.REFUSED:
        print(f"    - {what}: {why}")


if __name__ == "__main__":
    main()
