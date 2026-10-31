"""Listing 19.2: thirty nights of Pennant's TMS export, loaded naively and through a FileDrop connector.
Injected: night 9 the MFT re-sends the same file; night 17 a TMS patch renames 'status' to 'leg_status';
night 23 the transfer is cut off at 18,200 rows; night 26 no file arrives. Deterministic stand-in data."""
import datetime as dt
import _paths  # noqa: F401
from fieldkit.connectors import FileDrop
from sim import nightly_csv, HEADER

fd = FileDrop("pennant-tms-status", HEADER, deadline_min=3 * 60 + 30,
              key=lambda d: "weekday" if d.weekday() < 5 else "weekend")
naive = {"loaded": 0, "null_status_rows": 0, "double_loaded_rows": 0, "partial_nights": 0, "silent_misses": 0}
log, prev = [], None
for night in range(1, 31):
    hdr = [("leg_status" if h == "status" else h) for h in HEADER] if night == 17 else None
    if night == 26:
        miss = fd.missing(False, 3 * 60 + 31)
        naive["silent_misses"] += 1
        log.append((night, "-", 0, "ALARM 03:30 no file" if miss else "?"))
        continue
    content, day = (prev if night == 9 else nightly_csv(night, rows=18200 if night == 23 else None, header=hdr))
    arrived = 2 * 60 + 14 + night % 9
    b = fd.check(f"tms_status_{day:%Y%m%d}.csv", content, arrived, label=day)
    rows = b.rows if b.rows else content.count(b"\n")
    naive["loaded"] += content.count(b"\n")
    if night == 17: naive["null_status_rows"] += content.count(b"\n")
    if night == 9: naive["double_loaded_rows"] += content.count(b"\n")
    if night == 23: naive["partial_nights"] += 1
    if b.status != "accepted" or night in (1, 2, 30):
        log.append((night, day.strftime("%a"), rows, f"{b.status.upper()} " + "; ".join(b.reasons)))
    prev = (content, day)
for n, d, r, msg in log:
    print(f"night {n:2} {d:3} rows {r:6,}  {msg}")
acc = sum(len(v) for v in fd.history.values())
print(f"\nconnector: accepted {acc} nights, refused or flagged {len(log) - 3} events, 0 rows loaded from a bad night")
print("naive loader: " + ", ".join(f"{k} {v:,}" for k, v in naive.items()))
