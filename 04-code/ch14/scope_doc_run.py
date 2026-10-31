"""Listing 14.3 driver: the scoping document Greystone signed on day 19, rendered from data, and its lint."""
import pipeline as pl
import projection as pj
import scoping_doc as sd
from decision_tree import CLASSES, split


def main():
    p = pj.project(pl.ELECTRONIC)
    sp = split(pl.ELECTRONIC)
    inv = dict(electronic=pl.VOLUME["electronic"], fax=pl.VOLUME["fax"], steps_e=len(pl.ELECTRONIC),
               steps_f=len(pl.FAX), det_e=sp[CLASSES[0]], model_e=sp[CLASSES[2]] + sp[CLASSES[3]])
    doc = sd.signed_v10(p, inv)
    print(sd.render(doc, "Greystone Health: referral intake, release 1 scope (v1.0, day 19)", sd.SIGNATURES))
    print("lint:", sd.lint(doc) or "0 refusals")
    print("status mix:", ", ".join(f"{k} {v}" for k, v in sd.status_mix(doc).items()))
    print("strips:", ", ".join(f"{s} {sum(1 for c in doc if c.strip == s)}" for s in sd.STRIPS))
    print("projection inputs:")
    i = pj.Inputs()
    for k, v in i.__dict__.items():
        print(f"  {k:<22}{v!s:>6}  {pj.STRIP[k]}")


if __name__ == "__main__":
    main()
