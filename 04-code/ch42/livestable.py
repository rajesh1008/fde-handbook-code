"""The ninety-day review as the Live Stable gate (Chapter 42). Usage: python livestable.py v0|v1
v0: the review run on day 60 with the engagement as handed over (monthly sample read by Northlight, the
    day-38 incident open in the runbook, no customer drill, the EU pin about to retire).
v1: the review run on day 90 after the chapter's methods. Each criterion carries its evidence and who measured
    it; a criterion measured by Northlight alone does not count (fieldkit.liveops.live_stable).
Criteria agreed at Kofi Mensah's change board on day 30."""
import sys, subprocess
from pathlib import Path
import _paths  # noqa: F401
from world import day_docs, outcome
from fieldkit.liveops import live_stable
from ownership import timeline

mode = sys.argv[1] if len(sys.argv) > 1 else "v1"
here = Path(__file__).parent
run = lambda *a: subprocess.run([sys.executable, *a], cwd=here, capture_output=True, text=True).stdout
if mode == "v1":
    oc = [outcome(x, 0.78) for d in range(63, 91) for x in day_docs(d, fixed=True)]
    m, s, n = oc.count("matched"), oc.count("silent"), len(oc)
    ttm = [l for l in run("drill.py", "v2").splitlines() if l.startswith("time to detect")][0]
    _, tl = timeline()
    rd = tl[-1][2].gated
    crit = [
        ("1 no open Sev-1 or Sev-2", True, "INC-P-038 closed day 43 by runbook change RC-17", "Kofi Mensah"),
        ("2 matched >= 80%, silent <= 0.5%, last 4 weeks", m / n >= 0.80 and s / n <= 0.005,
         f"days 63-90: {m}/{n} matched {m/n:.1%}, silent {s} ({s/n:.2%})", "Dana Whitaker's team"),
        ("3 drift monitor read by the customer weekly", True, "13 weekly reads, last day 90", "Dana Whitaker"),
        ("4 incident drill passed alone, TTM <= 30 min", True, ttm.replace("time to ", "").replace("   ", "; "),
         "Nadia Brooks"),
        ("5 every model change recorded and approved", True, "MC-EU-02 approved day 54, migrated day 55",
         "Joanne Pruitt"),
        ("6 two-of-five rule and named deputies", True, "rule passes; 6 of 10 holdings deputized", "Grant Holloway"),
        ("7 hand-over readiness >= 0.80", rd >= 0.80, f"{rd:.2f} (Chapter 41 score, day 70 drill)", "Kofi Mensah"),
        ("8 gold set refreshed on production documents", True, "60 BRF-INV v2 documents added day 33",
         "Dana Whitaker"),
    ]
    day = 90
else:
    oc = [outcome(x, 0.80) for d in range(33, 61) for x in day_docs(d, fixed=d >= 36)]
    m, s, n = oc.count("matched"), oc.count("silent"), len(oc)
    crit = [
        ("1 no open Sev-1 or Sev-2", False, "INC-P-038 open: no runbook change owner", "Northlight"),
        ("2 matched >= 80%, silent <= 0.5%, last 4 weeks", m / n >= 0.80 and s / n <= 0.005,
         f"days 33-60: {m}/{n} matched {m/n:.1%}, silent {s} ({s/n:.2%})", "Northlight"),
        ("3 drift monitor read by the customer weekly", False, "monthly sample, read by Northlight", "Northlight"),
        ("4 incident drill passed alone, TTM <= 30 min", False, "no drill; day-38 TTM 60 min", ""),
        ("5 every model change recorded and approved", False, "EU pin retires day 62; no plan", ""),
        ("6 two-of-five rule and named deputies", False, "own-exec and provider account orphaned", ""),
        ("7 hand-over readiness >= 0.80", False, "0.30 (Chapter 41 score after day 14)", "Kofi Mensah"),
        ("8 gold set refreshed on production documents", False, "not since go-live", ""),
    ]
    day = 60
verdict, lines = live_stable(crit)
print(f"NINETY-DAY REVIEW  Pennant  mode {mode}  run on production day {day}  (deterministic stand-in)")
for l in lines:
    print(l)
print(f"verdict: {verdict}")
if verdict == "LIVE STABLE":
    print(f"time to production (signature to Live Stable): engagement day 168 + {day} = day {168 + day}")
