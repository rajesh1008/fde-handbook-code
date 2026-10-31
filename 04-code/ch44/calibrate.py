"""Listing 44.4: inter-rater agreement on the discovery role-play, before and after behavioral anchors."""
import world as W
from practice import calibration, ANCHORS
for label, r in (("before anchors (month 8)", W.RATINGS_BEFORE), ("after anchors (month 10)", W.RATINGS_AFTER)):
    c = calibration(r)
    print(label)
    for k, v in c["pairs"].items():
        print(f"  kappa {k:<14} {v:.2f}")
    print(f"  mean kappa {c['mean_kappa']:.2f}; unanimous {c['unanimous']} of {c['n']}; "
          f"recordings with a two-point spread: {c['spread2']}")
print("\nanchors used after month 9:")
for k, v in ANCHORS.items():
    print(f"  {k}: {v}")
