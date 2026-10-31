"""Listing 21.7: what it costs to add lineage on day D instead of day 0."""
import _paths  # noqa: F401
from pennant import u

PER_DAY = 70          # released claims per day (stand-in)
MAIL_RETENTION = 30   # days the mailbox keeps a scan
BUILD_IN = 34         # hours to build the chain on day 0
RETROFIT_FIXED = 120  # hours to bolt it on later (schema, backfill tooling, re-plumbing)
PER_RECOVER = 0.05    # hours to reconstruct one recoverable output
FX_SHARE = 0.42       # claims that depend on a currency conversion


def retrofit(day):
    if day == 0:
        return BUILD_IN, 0, 0
    n = recoverable = 0
    for d in range(day):
        for i in range(PER_DAY):
            n += 1
            mail_ok = day - d <= MAIL_RETENTION or u(d, i, "edi") < 0.35
            fx_ok = u(d, i, "fx") >= FX_SHARE or d % 30 == 29     # month-end snapshot only
            recoverable += mail_ok and fx_ok
    hours = RETROFIT_FIXED + PER_RECOVER * recoverable
    return hours, n, n - recoverable


if __name__ == "__main__":
    print("day lineage starts | hours | outputs already released | unrecoverable")
    for day in (0, 15, 30, 45, 60, 75, 90):
        h, n, lost = retrofit(day)
        print(f"  day {day:>3}          | {h:>5.0f} | {n:>6} | {lost:>5} ({(lost / n if n else 0):.0%})")
