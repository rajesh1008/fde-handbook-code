"""Try It Yourself, Chapter 11.  python tryit.py 1|2|3"""
import sys
import _path  # noqa: F401
import stakeholders as S, champions as C, status
from stakeholders import Person, StakeholderMap


def try1():
    """Draw the map of an engagement of your own from the kickoff invite only, then check it."""
    mine = StakeholderMap("Your customer", 3, [
        Person("vp", "VP who signed", "VP Finance", ("sponsor",), 1, source="kickoff"),
        Person("it", "IT director", "IT", ("approver", "owner"), 1, source="org chart"),
    ])
    print("TRY 1: a kickoff-only map"); print(S.report(mine))


def try2():
    """Add operators and a blocker with reasons, then age the map by three weeks."""
    m = StakeholderMap("Your customer", 12, [
        Person("vp", "VP who signed", "VP Finance", ("sponsor",), 10, source="own words"),
        Person("it", "IT director", "IT", ("approver", "owner"), 11, source="own words"),
        Person("ap", "AP clerk lead", "Accounts payable", ("operator",), 9, champion=True, source="observed"),
        Person("aud", "Internal audit", "Audit", ("blocker",), 8, reasons=("no automated approval of payments",), source="own words"),
    ])
    print("TRY 2: the same map on day 12 and day 33"); print(S.report(m)); print(); print(S.report(m, today=33))


def try3():
    """Write a status that hides a slip and let the lint find it. Then fix the headline."""
    s = status.Status(4, 28, "green", 90, 101, headline="Good progress this week; gates passed 0 of 5",
                      done=["Read access granted"], in_progress=["Extraction on the sample"],
                      blockers=[status.Blocker("Write access", "IT director", 10, 35)], risks=["Clerk turnover"],
                      decisions=[("Exception queue owner", "VP who signed", 31)], next_week=["Shadow two clerks"])
    print("TRY 3: lint a status"); [print("  -", p) for p in status.lint(s)]
    s.headline = "Go-live slips from day 90 to day 101 because write access is 18 days old; gates passed 0 of 5"
    s.reported = "amber"
    print("  after rewrite:", status.lint(s) or "clean")


if __name__ == "__main__":
    {"1": try1, "2": try2, "3": try3}[sys.argv[1] if len(sys.argv) > 1 else "1"]()
