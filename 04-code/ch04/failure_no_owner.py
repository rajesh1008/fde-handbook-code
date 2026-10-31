"""Listing 4.4: failure injection. Caldwell as it could look at shadow exit, then the same system with every
owner removed. The naive score cannot tell them apart; the gated assessment can."""
from checklists import caldwell_projected


def main():
    print("FAILURE INJECTION  owners removed from a system that is otherwise ready")
    for no_owner in (False, True):
        v = caldwell_projected(no_owner=no_owner).assess(day=140)
        print(v.summary())
        print()
    a = caldwell_projected().assess(140)
    b = caldwell_projected(no_owner=True).assess(140)
    print(f"naive score moved {a.naive - b.naive:+.2f}; gated score moved {b.gated - a.gated:+.2f}; "
          f"verdict {a.label} -> {b.label}")


if __name__ == "__main__":
    main()
