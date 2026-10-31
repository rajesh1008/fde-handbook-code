"""Failure injection: a product vendor's playbook run by an integrator with no product to defend."""
from homes import HOMES
from playbook import INTEGRATOR_PLAYBOOK, VENDOR_PLAYBOOK, report, tally, run

integ = HOMES["integrator"]
print("FAILURE INJECTION")
fits = report("NORTHLIGHT PLAYBOOK v1", VENDOR_PLAYBOOK, integ)
bad = [f for f in fits if f.verdict in ("BREAKS", "INVERTS")]
print(f"  {len(bad)} of {len(fits)} plays fail outright; first to fail in the field: "
      f"{bad[0].play.key} ({bad[0].reason})")
print("REPAIR: same intents, rewritten for the home that runs them")
fixed = report("INTEGRATOR PLAYBOOK", INTEGRATOR_PLAYBOOK, integ)
print("  vendor running the integrator's playbook: "
      + "  ".join(f"{k} {v}" for k, v in tally(run(INTEGRATOR_PLAYBOOK, HOMES['vendor'])).items()))
