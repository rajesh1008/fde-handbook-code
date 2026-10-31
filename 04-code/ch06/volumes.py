"""Listing 6.8: volumes, times and costs per path, from system counts and watched timings (stand-in).

Volumes are Caldwell's own monthly counts (artifacts); minutes and lags are means over the documents watched;
the intake cost of 46 dollars an hour is Caldwell's loaded figure (stand-in). Nothing here was measured on
production data; the numbers are as good as the sample under them, and the sample size is printed.
"""
from caldwell_discovery import watched_documents, PATHS, INTAKE_COST_PER_HOUR

docs = watched_documents()
rows = []
print("path  doc  vol/mo  seen  min/doc  hours/mo  cost/mo  lag days  late date")
for p in PATHS:
    ds = [d for d in docs if d.path == p.pid]
    if ds:
        mpd = sum(d.work_min for d in ds) / len(ds)
        lag = sum(d.lag_days for d in ds) / len(ds)
        late = sum(d.lag_days >= 0.5 for d in ds) / len(ds)
    else:
        mpd = p.work_min * (1 - p.exc_rate) + p.exc_min * p.exc_rate
        lag, late = p.lag_days, None
    hours = p.volume * mpd / 60
    rows.append((p, hours))
    late_s = f"{100 * late:.0f}%" if late is not None else "n/a"
    print(f"{p.pid}   {'yes' if p.documented else 'no':<4} {p.volume:>6,}  {len(ds):>4}  {mpd:>7.1f}  {hours:>8,.0f}  "
          f"${hours * INTAKE_COST_PER_HOUR:>6,.0f}  {lag:>8.1f}  {late_s:>9}")
th = sum(h for _, h in rows)
dh = sum(h for p, h in rows if p.documented)
tv = sum(p.volume for p in PATHS)
dv = sum(p.volume for p in PATHS if p.documented)
print(f"documented paths: {dv:,} documents ({100 * dv / tv:.1f}%), {dh:,.0f} hours ({100 * dh / th:.1f}%)")
print(f"found paths:      {tv - dv:,} documents ({100 * (tv - dv) / tv:.1f}%), {th - dh:,.0f} hours ({100 * (th - dh) / th:.1f}%)")
print(f"all intake: {th:,.0f} hands-on hours a month; ${th * INTAKE_COST_PER_HOUR / tv:.2f} a document at ${INTAKE_COST_PER_HOUR:.0f}/hour")
for p, h in rows:
    if p.pid in ("P02", "P10"):
        print(f"  {p.pid} {p.name}: ${h * INTAKE_COST_PER_HOUR / p.volume:.2f} a document")
allw = docs
print(f"watched documents whose recorded received date is later than arrival: "
      f"{sum(d.lag_days >= 0.5 for d in allw)} of {len(allw)} ({100 * sum(d.lag_days >= 0.5 for d in allw) / len(allw):.0f}%)")
