"""Listing 4.3 driver: the demo as sold, and Caldwell on day 10, through the same 25 proofs."""
from checklists import demo_as_sold, caldwell


def main():
    for c, day in ((demo_as_sold(), 2), (caldwell(10), 10)):
        print(c.assess(day).summary())
        print()


if __name__ == "__main__":
    main()
