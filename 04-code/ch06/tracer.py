"""Listing 6.2: one tracer document followed end to end through the closed Springfield fax number.

The tracer is a synthetic first-notice form in the name of the fixture claimant Emily Carter, marked TEST on
every page, faxed with Anne Kessler's consent on day 13 at 07:52. Timings are the stand-in for the FDE's
notes; the arithmetic below is the point.
"""
from datetime import datetime, timedelta

D0 = datetime(2026, 1, 1)   # day 1 of the engagement, used only for arithmetic


def at(day, hhmm):
    h, m = map(int, hhmm.split(":"))
    return D0 + timedelta(days=day - 1, hours=h, minutes=m)


# (when, who, system, what happened, hands-on minutes)
EVENTS = [
    (at(13, "07:52"), "sender", "fax gateway, legacy line", "fax received on the closed office's number", 0),
    (at(13, "08:10"), "gateway rule", "regional mailbox", "forwarded as an image attachment", 0),
    (at(14, "13:25"), "regional assistant", "regional mailbox", "opened on the twice-weekly check, forwarded", 3),
    (at(14, "13:31"), "mail system", "claims shared mailbox", "arrives as a forward, original date lost", 0),
    (at(15, "09:02"), "intake clerk", "intake queue", "indexed; policy number unreadable, sent to exceptions", 4),
    (at(15, "14:40"), "Tom Whitfield", "claims system", "rang the agent on the cover sheet for the number, keyed", 9),
]

print("when        who                  system                      minutes  what")
for t, who, sys_, what, m in EVENTS:
    d = (t - D0).days + 1
    print(f"day {d} {t:%H:%M}  {who:<20} {sys_:<27} {m:>7}  {what}")
work = sum(e[4] for e in EVENTS)
elapsed = EVENTS[-1][0] - EVENTS[0][0]
hours = elapsed.total_seconds() / 3600
people = {e[1] for e in EVENTS if e[4] > 0}
systems = {e[2] for e in EVENTS}
print(f"hands-on: {work} minutes; elapsed: {elapsed.days} days {elapsed.seconds // 3600} h {elapsed.seconds % 3600 // 60} min")
print(f"work share of elapsed time: {100 * work / 60 / hours:.2f}%")
print(f"people who worked it: {len(people)}; systems it passed through: {len(systems)}")
print(f"received date recorded: day {(EVENTS[-1][0] - D0).days + 1} (faxed day 13)")
