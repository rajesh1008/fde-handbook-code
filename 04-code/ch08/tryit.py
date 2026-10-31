"""Try It Yourself, Chapter 8. Run: python tryit.py a | b | c  (deterministic stand-in)."""
import sys
import caldwell_scope as cs
from scoping import Claim, Criterion, ScopeDoc, Source

which = (sys.argv[1:] or ["a"])[0]
if which == "a":                      # take the scorer off one criterion
    doc = cs.signed()
    doc.criteria[3].scorer = "claims operations"
    for f in doc.lint():
        print("  ", *f)
    print(f"evaluation suite accepts {len(doc.suite_config())} of {len(doc.criteria)} criteria")
elif which == "b":                    # shrink the calibration set
    import calibration as cal
    for n in (60, 20):
        cal.N_DOCS = n
        r2 = cal.per_field(2)
        exact = [f for f, k, _ in r2 if k >= 0.8]
        low = ", ".join(f"{f} {k:.2f}" for f, k, _ in r2 if k < 0.8)
        print(f"{n} documents: {len(exact)} of 14 exact; below 0.80: {low}")
elif which == "c":                    # Greystone: a referral scope with two of this chapter's mistakes in it
    g = ScopeDoc("Greystone Health", 18, "Thursday draft", [], {}, ["medical necessity", "approval or denial"],
                 [Criterion("G-01", "Drafted prior-authorization requests are complete",
                            "required payer fields present and supported by the packet", "clinical reviewers",
                            "Greystone referral packets, three specialties", 300, "drafts produced", ">= 95%",
                            "suite: payer_fields")], [], [],
                 [Claim("G-a", "The fax receipt time is the referral's received date", "F",
                        Source("Greystone Health", "customer", "Thursday draft", 18), "criteria",
                        derived_from="G-0")],
                 lineage={"G-0": Claim("G-0", "Fax receipt time starts the referral clock", "V",
                                       Source("Northlight FDE", "vendor", "question bank G03", 12))})
    for f in g.lint():
        print("  ", *f)
