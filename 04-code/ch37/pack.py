"""The accountable executive's pack. Usage: pack.py logs|day157"""
import sys
import _paths  # noqa: F401
from fieldkit.gates import pack
import world

which = sys.argv[1] if len(sys.argv) > 1 else "day157"
p = pack(world.pack_logs() if which == "logs" else world.pack_day157())
print(f"ACCOUNTABLE EXECUTIVE'S PACK  Caldwell Mutual  {'day 141, what we had: logs' if which == 'logs' else 'day 157'}")
for a in p["rows"]:
    who = f"{a.owner}, day {a.day}" if a.owner and a.day else "-"
    print(f"  {a.name:26} {a.status:8} {a.ref or '-':52} {who}")
    if a.gap:
        print(f"  {'':26} gap: {a.gap}")
c = p["counts"]
print(f"present {c['present']}, partial {c['partial']}, missing {c['missing']}; complete: {p['complete']}; digest {p['digest']}")
