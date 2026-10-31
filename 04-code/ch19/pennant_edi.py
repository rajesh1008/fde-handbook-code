"""Listing 19.8: one day of Pennant's carrier status messages (X12 214), parsed with envelope checks,
folded into an intraday status per shipment leg, and reconciled with the next 02:00 TMS export.
Deterministic stand-in: 312 sets, 4 with a wrong segment count, 3 with an unknown status code; in the export,
9 legs carry a status a clerk keyed by hand and 2 legs are unknown to the TMS."""
import random
import _paths  # noqa: F401
from fieldkit.connectors import EDIError, edi_status, parse_x12, reconcile
from sim import edi_day

text, _ = edi_day()
sets, env_err = parse_x12(text)
status, sem_err = {}, []
for s in sets:
    try:
        ship, leg, st, stamp = edi_status(s)
    except EDIError as e:
        sem_err.append(str(e)); continue
    k = f"{ship}/{leg}"
    if k not in status or stamp >= status[k]["stamp"]:
        status[k] = {"status": st, "stamp": stamp}
print(f"transaction sets 312: envelope errors {len(env_err)}, unknown codes {len(sem_err)}, parsed {len(sets) - len(sem_err)}")
print(f"  e.g. {env_err[0][0]}: {env_err[0][1]}; {sem_err[0]}")
print(f"legs with an intraday status: {len(status)}")
rng = random.Random(30)
keys = sorted(status)
override = set(rng.sample(keys, 9))
unknown = set(rng.sample([k for k in keys if k not in override], 2))
csv = {k: {"status": ("delivered" if v["status"] != "delivered" else "arrived") if k in override else v["status"]}
       for k, v in status.items() if k not in unknown}
r = reconcile({k: {"status": v["status"]} for k, v in status.items()}, csv, ["status"])
print(f"reconciled with the 02:00 export: {r.counts()}")
print(f"  mismatched example: {r.mismatched[0][0]} EDI '{status[r.mismatched[0][0]]['status']}' vs TMS "
      f"'{csv[r.mismatched[0][0]]['status']}'")
print(f"agreement on legs both sides know: {len(r.matched) / (len(r.matched) + len(r.mismatched)):.1%}")
