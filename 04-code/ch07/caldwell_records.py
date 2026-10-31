"""SYNTHETIC RECORDS (deterministic stand-in; no Caldwell data). Generated to the shape Ruth Calloway described
on day 24 and Chapter 6's path volumes, so the checks in this chapter can run before any real record arrives.
Seeded; every run prints the same numbers."""
import random, datetime as dt
from discovery_snapshot import PATHS

# days between the date Caldwell received a notice (stamp, fax header or call date) and the scan/ingest time
LAG = {"P01": (0, 1, 1, 1, 2, 3), "P02": (0, 0, 0, 1), "P03": (0, 0, 0, 0, 0, 1), "P04": (0,), "P05": (1, 2, 2, 3),
       "P06": (0, 1, 2, 3, 5), "P07": (2, 4, 6, 8, 10), "P08": (1,), "P09": (2, 4, 7), "P10": (1, 3, 6), "P11": (0, 1)}
START = dt.date(2026, 3, 2)  # a Monday

def first_notices(n=400, seed=7):
    rng = random.Random(seed)
    ids = list(PATHS); w = [PATHS[p][2] for p in ids]
    out = []
    for i in range(n):
        p = rng.choices(ids, w)[0]
        received = START + dt.timedelta(days=rng.randrange(0, 56))
        lag = rng.choice(LAG[p])
        ingest = received + dt.timedelta(days=lag)
        while ingest.weekday() >= 5 and p in ("P01", "P05", "P07", "P09", "P10"):  # scanned on business days
            ingest += dt.timedelta(days=1)
        out.append(dict(doc=f"D{i+1:04d}", path=p, notice_received_dt=received, received_at=ingest))
    return out

def duplicates(n=1000, seed=11):
    """Second-door duplicates: days between the first notice being keyed and the duplicate arriving."""
    rng = random.Random(seed)
    return [0 if rng.random() < 0.11 else rng.choice((1, 1, 2, 2, 3, 5, 8)) for _ in range(n)]

def loss_date_corrections(n=1000, seed=13):
    """Days after first notice when the loss date was corrected, or None (about 9% corrected within 14 days)."""
    rng = random.Random(seed)
    out = []
    for _ in range(n):
        r = rng.random()
        out.append(rng.randint(1, 14) if r < 0.09 else (rng.randint(15, 60) if r < 0.094 else None))
    return out
