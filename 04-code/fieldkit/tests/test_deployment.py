from fieldkit import Checklist, Proof, DIMENSIONS, is_person


def _full(owner="Anne Kessler", accepted=3, authority="defines correct"):
    c = Checklist("t", customer_people=("Anne Kessler",))
    for d in DIMENSIONS:
        for i in range(2):
            c.add(Proof(f"{d}-{i}", d, "r", status="held", must_pass=True, measured_by="Anne Kessler",
                        on_what="gold set, 300 documents"))
    for p in c.proofs.values():
        if p.dimension == "ownership":
            p.owner, p.accepted_day, p.authority = owner, accepted, authority
    return c


def test_ready_when_all_held():
    assert _full().assess(1).label == "READY"


def test_owner_not_person_blocks_but_naive_unchanged():
    good, bad = _full().assess(1), _full(owner="Operations").assess(1)
    assert bad.naive == good.naive == 1.0
    assert bad.label == "NOT READY"


def test_owner_needs_acceptance_and_authority():
    assert _full(accepted=None).assess(1).label == "NOT READY"
    assert _full(authority="").assess(1).label == "NOT READY"


def test_synthetic_capability_does_not_count():
    c = _full()
    c.update("capability-0", on_what="synthetic packets")
    assert c.assess(1).label == "NOT READY"


def test_is_person():
    assert is_person("Michael Hart") and not is_person("TBD")
