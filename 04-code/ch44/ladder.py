"""Listing 44.8: promotion packets checked against the ladder's evidence criteria."""
import world as W
from practice import ladder_check
for name, packet in W.PACKETS.items():
    r = ladder_check(packet, "Senior FDE")
    print(f"{name}: {'READY' if r['ready'] else 'NOT YET'}")
    for k, need, have, ok in r["rows"]:
        print(f"  {'ok ' if ok else 'gap'} {k:<36} need {need}, have {have}")
    if r["ignored"]:
        print("  not evidence (ignored): " + ", ".join(f"{k} {v}" for k, v in r["ignored"].items()))
