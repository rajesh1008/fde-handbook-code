"""Try It Yourself, Chapter 6. Usage: python tryit.py a|b|c (deterministic stand-in)."""
import sys
import caldwell_discovery as cd
from discovery import DiscoveryLog, Note, NoteRejected

ex = sys.argv[1] if len(sys.argv) > 1 else "a"
print(f"--- exercise {ex}")
if ex == "a":
    # How much disagreement counts as a contradiction is a judgment; see what changes with it.
    log = cd.build_log(resolve=False)
    for tol in (0.1, 0.25, 0.5, 1.0):
        cs = log.contradictions(26, tolerance=tol)
        print(f"tolerance {tol:>4}: {len(cs)} contradictions ({', '.join(c.path for c in cs) or 'none'})")
elif ex == "b":
    # Remove Tom Whitfield: his two desk sessions, his interviews, and every path he gave the lead on.
    log = cd.build_log()
    gone = {p for p, who in cd.LEAD.items() if who == "Tom Whitfield"}
    log.notes = [n for n in log.notes if n.who != "Tom Whitfield" and n.path not in gone]
    r = log.coverage(26)
    print(f"paths known: {len(r.rows)} of 11; covered: {sum(x.covered for x in r.rows)}")
    print(f"known volume {r.total_volume:,.0f} of 14,800 a month; covered {r.covered_volume:,.0f}")
    print(f"never found: {', '.join(sorted(gone))} ({sum(cd.SPEC[p].volume for p in gone):,} documents a month)")
elif ex == "c":
    # Greystone referral intake: a note that would carry patient data is refused before it is stored.
    import discovery
    text = "fax for 00482913, cardiology"  # a bare medical record number, as a coordinator reads it aloud
    Note(3, "shadow", "referral coordinator", "R02", "arrive", text, n=1)
    print("Caldwell patterns: accepted (the bare number gets through)")
    discovery.IDENTIFIER_PATTERNS += (r"\b\d{8}\b", r"\b\d{1,2}/\d{1,2}/\d{2,4}\b")
    try:
        Note(3, "shadow", "referral coordinator", "R02", "arrive", text, n=1)
    except NoteRejected as e:
        print(f"Greystone patterns: rejected: {e}")
    g = DiscoveryLog("Greystone Health", {"R01": "referral fax", "R02": "electronic referral",
                                          "R03": "phone referral, fax follows", "R04": "payer portal status",
                                          "R05": "paper carried by the patient"}, documented=("R01", "R02"))
    for pid in ("R01", "R02"):
        for q in ("arrive", "touch", "decide", "except", "land"):
            g.add(Note(2, "interview", "Michael Hart", pid, q, "described in the referral policy"))
    for pid, n in (("R01", 19), ("R03", 6), ("R05", 2)):
        for q in ("arrive", "touch", "decide", "except", "land"):
            g.add(Note(4, "shadow", "referral coordinator", pid, q, f"{n} referrals watched", n=n))
    print(g.coverage(4).render())
