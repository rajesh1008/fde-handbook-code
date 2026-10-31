"""Listing 50.8b: David Okafor's pack, the eight artifacts the accountable executive shows the regulator, at
submission one (day 118) and at go-live (day 171). Uses fieldkit.gates.pack unchanged."""
import sys
import _paths  # noqa: F401
from fieldkit.gates import Artifact as A, pack

STATES = {
    118: [A("decision record", "HL gate register, AR and BC", "David Okafor", 112, "present"),
          A("lineage", "lineage store, build environment", "Martin Shaw", 112, "present"),
          A("model and prompt versions", "Northlight release notes", "", None, "partial", "vendor list, not the bank inventory"),
          A("evaluation at the time", "Northlight scoring, 200 memos", "", None, "partial", "scored by the vendor"),
          A("human review", gap="no shadow scoring yet"),
          A("authority boundary", "Schedule D, release one", "David Okafor", 61, "present"),
          A("incident history", gap="no incident process mapped to the bank register"),
          A("monitoring", gap="no metric the bank can compute")],
    171: [A("decision record", "HL gate register, AR to MRA", "David Okafor", 158, "present"),
          A("lineage", "lineage store, Canada region", "Martin Shaw", 171, "present"),
          A("model and prompt versions", "model inventory, 7 entries", "Helen Marsh", 158, "present"),
          A("evaluation at the time", "validation report, submission two", "Helen Marsh", 158, "present"),
          A("human review", "credit review scores, 600 memos", "David Okafor", 149, "present"),
          A("authority boundary", "Schedule D, release one", "David Okafor", 158, "present"),
          A("incident history", "operational risk register, shadow entries", "David Okafor", 150, "present"),
          A("monitoring", "M1 to M4 defined", "Helen Marsh", 158, "partial", "first monthly report due day 201")],
}

if __name__ == "__main__":
    day = int(sys.argv[1])
    p = pack(STATES[day])
    print(f"Harbourline Bank, day {day}: present {p['counts']['present']}, partial {p['counts']['partial']}, "
          f"missing {p['counts']['missing']}; digest {p['digest']}; complete {p['complete']}")
    for a in p["rows"]:
        who = f"{a.owner}, day {a.day}" if a.owner and a.day is not None else "-"
        print(f"  {a.name:<26} {a.status:<8} {a.ref or '-':<42} {who:<20} {a.gap}")
