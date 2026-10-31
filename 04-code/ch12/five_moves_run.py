"""Check two oral answers to the same hostile question for the five moves, and time them at 150 words a minute."""
import _path  # noqa: F401
from fieldkit.bid import five_moves

Q = "Your design adds a web console our standards prohibit. Why should we accept a deviation in year one?"
strong = dict(
    position="Because six operations staff need a queue view the add-in cannot show, and CL-23 allows a request for "
             "tools used by fewer than ten people.",
    evidence="Your standard PS-SUR-01 covers relationship managers and credit officers, 140 users; the console has "
             "six users, all in lending operations.",
    example="When a memo stalls, the console shows the 31 drafts waiting on a credit officer, oldest first; in the "
            "add-in that view would be 31 separate documents.",
    boundary="The console reads and reassigns; it does not edit or approve a memo, and it is not offered to "
             "relationship managers.",
    proof="The deviation request is line PS-SUR-01 in the crosswalk, with Martin Shaw as approver and day 40 as the "
          "decision day; you keep that page.")
weak = dict(
    position="Our console is a core part of the platform and customers love it.",
    evidence="It is used by most of our customers.",
    example="",
    boundary="",
    proof="We can show you a demo after the session.")
print(Q)
for name, a in (("strong", strong), ("weak", weak)):
    problems, secs = five_moves(a)
    print(f"{name}: {secs} seconds spoken; problems: {len(problems)}")
    for p in problems:
        print(f"  {p}")
