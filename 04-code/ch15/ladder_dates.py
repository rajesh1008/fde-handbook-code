"""Chapter 15: the day each access-ladder rung was reached, per customer (the data for Signature 6)."""
import json, sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "fieldkit"))
from fieldkit.access import LADDER
from fieldkit.fixtures import pennant_tracker, harbourline_tracker
from fieldkit.histories import caldwell_history, greystone_history, rung_reached_days

rows = {"Caldwell Mutual (day 54)": rung_reached_days(caldwell_history().replay(54)),
        "Greystone Health (day 112)": rung_reached_days(greystone_history().replay(112)),
        "Pennant Logistics (fixture)": rung_reached_days(pennant_tracker()),
        "Harbourline Bank (fixture)": rung_reached_days(harbourline_tracker())}
print(f"{'customer':<30}" + "".join(f"{r:>11}" for r in LADDER))
for name, d in rows.items():
    print(f"{name:<30}" + "".join(f"{('day ' + str(d[r])) if r in d else '-':>11}" for r in LADDER))
out = pathlib.Path(__file__).with_name("output") / "ladder_dates.json"
out.write_text(json.dumps(rows, indent=1))
