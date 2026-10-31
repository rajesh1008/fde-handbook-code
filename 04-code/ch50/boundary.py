"""Listing 50.7: the release boundary in the contract (Schedule D, stand-in), release one in force and release two
proposed. Uses fieldkit.actions unchanged."""
import _paths  # noqa: F401
from fieldkit.actions import Grant, ReleaseBoundary
import world as W

REFUSED = {"write_origination": "David Okafor and Helen Marsh, Schedule D: release one reads and drafts only",
           "submit_to_committee": "David Okafor: the credit officer submits, never the system",
           "draft_recommendation": "Helen Marsh: the recommendation is outside the validated use"}


def release_one():
    return ReleaseBoundary(W.CUSTOMER, [
        Grant("read", ("shadow", "production"), ("read_package", "read_policy", "read_prior_memos"), "David Okafor", 61,
              "read-only service identity; CL-09"),
        Grant("draft", ("shadow",), ("draft_memo",), "David Okafor", 112, "drafts scored, never shown"),
        Grant("draft", ("production",), ("draft_memo",), "David Okafor", 158, "after Model-Risk Approval"),
    ], refused=REFUSED)


PROPOSED = [  # release two: each signature is a separate decision; none is given as of day 171
    ("re-run the classification with writes in scope (H11 medium to high)", "Helen Marsh"),
    ("architecture review of the write path and its service identity", "Martin Shaw"),
    ("operational risk register entry and Schedule D amendment", "David Okafor"),
    ("contract amendment reviewed by legal", "Claire Dubois"),
]


def release_two_proposed():
    """The grant release two asks for. It carries no approver, so the lab keeps it out of force."""
    return Grant("write", ("uat", "production"), ("write_origination",), "", 0,
                 "per-write officer approval in the suite; separate submission")


def in_force(b):
    from fieldkit.security import is_person
    return ReleaseBoundary(b.customer, [g for g in b.grants if is_person(g.approved_by) and g.day], refused=b.refused)


OPS = ("read_package", "draft_memo", "draft_recommendation", "submit_to_committee", "write_origination")
if __name__ == "__main__":
    b = release_one()
    print("release one, in force from day 171"); print(b.table())
    for op in OPS:
        ok, why = b.check(op, "production")
        print(f"  production {op:<21} {'allowed' if ok else 'REFUSED'}: {why.replace('refused: ', '')}")
    g = release_two_proposed()
    r = dict(REFUSED); r.pop("write_origination")
    b2 = in_force(ReleaseBoundary(W.CUSTOMER, b.grants + [g], refused=r))
    print("release two, proposed: write_origination in uat and production, " + g.condition)
    for env in ("uat", "production"):
        ok, why = b2.check("write_origination", env)
        print(f"  {env:<10} write_origination     {'allowed' if ok else 'REFUSED'}: {why} (grant has no approver)")
    print("signatures release two needs (none given as of day 171):")
    for what, who in PROPOSED:
        print(f"  {who:<14} {what}")
