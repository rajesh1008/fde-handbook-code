"""Listing 3.2: audit the hand-written day-5 deck, lint the repo, and generate the status instead.

Run:  python day5_status.py
"""
import pathlib

from caldwell_week import DAY5_DECK, build_week

OUT = pathlib.Path(__file__).resolve().parent / "output" / "caldwell-repo"


def main():
    repo = build_week()
    print("== audit of the deck as sent (day 5) ==")
    for v in repo.audit(DAY5_DECK):
        print(" ", v)
    print("\n== lint (day 5) ==")
    for p in repo.lint(today=5):
        print(" ", p)
    repo.save(OUT)
    path = repo.write_status(OUT, 5)
    print(f"\n== generated status: {path.relative_to(OUT.parent.parent)} ==")
    print(path.read_text(), end="")


if __name__ == "__main__":
    main()
