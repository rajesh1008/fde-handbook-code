"""Staff turnover on both sides: fieldkit.liveops.OwnershipMap for each customer and for Northlight's side of each
account, read before and after the departures of production months 6 to 12. Deterministic stand-in."""
import _paths  # noqa: F401
from fieldkit.liveops import OwnershipMap


def caldwell(v1=False):
    o = OwnershipMap()
    o.add("own-exec", "Daniel Reyes", "Anne Kessler" if v1 else None, True)
    o.add("own-gold-set", "Lena Ortiz", "Tom Whitfield", True)
    o.add("own-operations", "Priya Natarajan", "Owen Pryce", True)
    o.add("own-model-risk", "Catherine Doyle", "Owen Pritchard", True)
    o.add("own-override", "Anne Kessler", "Joan Mercer", True)
    o.add("T3 run the evaluation suite", "Owen Pryce", "Ruth Calloway" if v1 else None, True)
    o.add("D2 rollback alone", "Priya Natarajan", "Owen Pryce", True)
    o.add("T4 upgrade dry run", "Owen Pryce", "Priya Natarajan", True)
    return o, ["Owen Pryce"]


def pennant(v1=False):
    o = OwnershipMap()
    o.add("own-exec", "Grant Holloway", "Rosa Delgado", True)
    o.add("own-gold-set", "Dana Whitaker", "Tasha Greene" if v1 else None, True)
    o.add("own-operations", "Rosa Delgado", "Tasha Greene", True)
    o.add("own-model-risk", "Joanne Pruitt", "Kofi Mensah", True)
    o.add("own-override", "Rosa Delgado", "Andre Willis", True)
    o.add("weekly matched sample", "Dana Whitaker", "Tasha Greene" if v1 else None, True)
    o.add("EU lane certificates", "Nadia Brooks", "Andre Willis" if v1 else None, v1)
    return o, ["Dana Whitaker"]


def greystone(v1=False):
    o = OwnershipMap()
    o.add("own-exec", "Denise Alvarez", "Michael Hart", True)
    o.add("own-gold-set", "Tess Moreno", "Keisha Monroe", True)
    o.add("own-operations", "Erin Walsh", "provider change manager", False)
    o.add("own-model-risk", "Sam Oakley", "Hannah Price", True)
    o.add("own-override", "Michael Hart", "Tess Moreno", True)
    o.add("emergency change path", "provider account lead (old team)", "provider change manager" if v1 else None, v1)
    o.add("payer criteria table", "Michael Hart" if v1 else None, "Tess Moreno" if v1 else None, v1)
    return o, ["provider account lead (old team)"]


def northlight(v1=False):
    o = OwnershipMap()
    o.add("Caldwell retainer lead", "lead FDE", "Sofia Brennan", True)
    o.add("Pennant night on-call rota", "lead FDE", "Leo Martens", True)
    o.add("Pennant service review", "lead FDE", "Leo Martens" if v1 else None, v1)
    o.add("Greystone account lead", "lead FDE", "Callum Reid", True)
    o.add("Greystone upgrade evidence", "Maya Brooks", "Sofia Brennan" if v1 else None, v1)
    o.add("evaluation lead, all accounts", "Sofia Brennan", "Callum Reid" if v1 else None, v1)
    return o, ["Maya Brooks", "lead FDE"]


def report(name, fn):
    lines = []
    for ver in (False, True):
        o, leavers = fn(ver)
        before = o.coverage(); sp = o.single_points()
        for p in leavers:
            o.leave(p)
        lines.append((ver, before, o.coverage(), sp, o.orphans()))
    print(f"\n{name}  leavers: {', '.join(fn()[1])}")
    for ver, b, a, sp, orph in lines:
        print(f"  {'v1' if ver else 'v0'} coverage {b:.2f} -> {a:.2f}; single points before: {len(sp)}; "
              f"orphans after: {orph or 'none'}")
    return lines


def main():
    print("TURNOVER ON BOTH SIDES  ownership coverage before and after the departures  (deterministic stand-in)")
    res = {}
    for n, f in [("Caldwell", caldwell), ("Pennant", pennant), ("Greystone", greystone),
                 ("Northlight (all three accounts)", northlight)]:
        res[n] = report(n, f)
    return res


if __name__ == "__main__":
    main()
