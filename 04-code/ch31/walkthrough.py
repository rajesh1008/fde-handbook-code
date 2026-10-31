"""Listing 31.2: one first notice through the whole agent, with where every step ran (deterministic stand-in)."""
from agent import Doc, Release, Gateway, run, SUITE
from state import ClaimStateStore
from world import RELEASE

EMILY = Doc("E-142-017", 142, "email", "T3", "IK-142-0017",
            truth=dict(policy_number="HO-4471902-6", claimant_name="Emily Carter", loss_date="day 139",
                       date_received="day 142", loss_type="water", loss_location="kitchen, ground floor",
                       injury_reported="no", police_report_ref="", other_party="", intake_channel="email",
                       cause_code="WL-03 appliance supply line"),
            text="The supply line behind my dishwasher split overnight and the kitchen floor is soaked.")

if __name__ == "__main__":
    print("release", RELEASE["name"] + ":", "; ".join(f"{k} {v}" for k, v in RELEASE.items() if k != "name"))
    print(f"document {EMILY.id}  channel {EMILY.channel}  claimant Emily Carter (synthetic)  intake key {EMILY.key}  mode shadow\n")
    store, gw = ClaimStateStore(), Gateway()
    tr, out = run(EMILY, Release(), gw, store)
    print(f"{'step':<7}{'class':<9}{'ran where':<36}result")
    for s, c, w, r in tr:
        print(f"{s:<7}{c:<9}{w:<36}{r}")
    print(f"\ngateway: {len(gw.calls)} calls as {gw.identity} (pin {gw.pin}): "
          + ", ".join(f"{m} ${d:.5f}" for m, _, _, _, d in gw.calls) + f"; total ${out['dollars']:.4f} (stand-in rates)")
    rec = store.claims[EMILY.key]
    print(f"state: {len(rec.items)} items under {EMILY.key}, each a pointer ({rec.items['loss_type'].source_ref}); "
          f"kept 90 days (shadow), owner {store.owner}")
    print(f"read by nl-shadow-readers: {len(store.read(EMILY.key, 'nl-shadow-readers', 142))} items; ", end="")
    try:
        store.read(EMILY.key, "nl-eval", 142)
    except PermissionError as e:
        print("read by nl-eval refused:", e)
    print(f"guardrail cards live: {', '.join(c.rid for c in SUITE.live())}")
