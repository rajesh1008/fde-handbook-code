"""Chapter 35: generate Greystone's data map from deployed configuration and compare it with the drawn map.
Usage: datamap.py v1 | v2"""
import sys

import _paths  # noqa: F401
from fieldkit.privacy import diff, digest, generate, lint, render
from world import GREYSTONE_DRAWN, greystone_config

mode = sys.argv[1] if len(sys.argv) > 1 else "v1"
if mode == "v1":
    gen = generate(greystone_config(122))
    found = lint(gen, {"HIPAA"}, owner="Greystone")
    print("Greystone data map, day 122: drawn (day 98) against generated from deployed configuration")
    print(f"  drawn hops {len(GREYSTONE_DRAWN)}   generated hops {len(gen)}   missing from drawing {len(diff(GREYSTONE_DRAWN, gen))}")
    print(f"  drawn map findings {len(lint(GREYSTONE_DRAWN, {'HIPAA'}, owner='Greystone'))}")
    print("\n  hop                          holder       data      retain  basis            lint")
    print(render(gen, found))
    print(f"\nfindings {len(found)} on {len({f.hop for f in found})} hops")
    for f in found:
        print(f)
else:
    gen = generate(greystone_config(125))
    found = lint(gen, {"HIPAA"}, owner="Greystone")
    again = generate(greystone_config(125))
    print("Greystone data map v2, day 125: regenerated after the fix")
    print("\n  hop                          holder       data      retain  basis            lint")
    print(render(gen, found))
    print(f"\nhops {len(gen)}   findings {len(found)}")
    print(f"digest (Northlight run)        {digest(gen)}")
    print(f"digest (Greystone security rerun, day 128) {digest(again)}   match {digest(gen) == digest(again)}")
    print("approval: data map v2 approved by Sam Oakley, Security Lead, day 129, against the digest above")
