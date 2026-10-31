"""Sprint zero exit check for Caldwell (days 15-28): counterparts named, access owned, golden paths, registers open."""
from cadence_data import CALDWELL_COUNTERPARTS, CALDWELL_GOLDEN_PATHS, caldwell_register
from fieldkit.deployment import is_person

def main(day=28):
    print(f"SPRINT ZERO EXIT  Caldwell Mutual  day {day}")
    gaps = 0
    for decision, who in CALDWELL_COUNTERPARTS.items():
        ok = is_person(who)
        gaps += not ok
        print(f"  {'ok ' if ok else 'GAP'} {decision:<38}{who or '(nobody named)'}")
    print("golden paths:")
    for k, path, rung, n in CALDWELL_GOLDEN_PATHS:
        print(f"  {k}  {path:<52}{rung} ({n} documents)")
    reg = caldwell_register()
    opened = [r for r in reg.records.values() if r.raised_day <= day]
    print(f"decision register: {len(opened)} records opened by day {day}, "
          f"{sum(r.status == 'decided' and r.decided_day <= day for r in opened)} decided")
    print(f"counterpart gaps: {gaps}  ->  {'EXIT' if gaps == 0 else 'EXIT WITH RECORDED GAP (D-06)'}")

if __name__ == "__main__":
    main()
