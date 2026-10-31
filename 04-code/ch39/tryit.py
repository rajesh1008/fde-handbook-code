"""Try It Yourself, Chapter 39. Usage: tryit.py a|b|c"""
import sys
import _paths  # noqa: F401
import world as W, suite as U

D = W.caldwell_window(); p = sys.argv[1]
if p == "a":
    print("Exercise A: raise the coverage minimum and watch which stratum stops the gate")
    for m in (60, 100, 116, 150):
        rows, dec, since = U.gate(D, coverage=m, only=("G-2",), scorecard=False)
        print(f"coverage >= {m:3}: {rows[0][2]:40} {rows[0][4]}")
elif p == "b":
    print("Exercise B: after the holiday injection, how many normal intake days until G-2 and G-3 pass?")
    _, _, since = U.gate(D); rates = {s: k / n for s, (k, n, _) in since.items()}
    H = W.holiday_week(rates); ch = [(149, "rc-1h", tuple(W.STRATA))]
    extra, day = [], 154
    for i in range(1, 16):
        day += 1 if (day + 1) % 7 not in (0, 1) else 3
        import random
        r = random.Random(4000 + i); c = W._counts(W.REFERENCE, W.PER_DAY, r, 6)
        for s in W.STRATA:
            p_ = W.REGRESSION.get(s, rates[s])
            extra += [dict(day=day, id=f"N{day}{s}{j}", stratum=s, cause=None if r.random() < p_ else "x",
                           band="review", wrong=False, silent=False, streams=()) for j in range(c[s])]
        rows, dec, _ = U.gate(H + extra, changes=ch, only=("G-2", "G-3"), scorecard=False)
        print(f"+{i:2} normal days (to day {day}): G-2 {rows[0][4]:5} {rows[0][2]:34} G-3 {rows[1][4]:5} {rows[1][2]}")
        if all(r_[4] == "pass" for r_ in rows):
            break
    print("note: G-3 stays FAIL while the paper regression is real; more days only make the evidence firmer")
elif p == "c":
    print("Exercise C: change the clean-day rule for fixed silent causes")
    for c in (3, 4, 5):
        rows, dec, _ = U.gate(D, clean=c, only=("G-5",), scorecard=False)
        print(f"clean days >= {c}: G-5 {rows[0][4]:10} decision for G-5 alone: {dec}")
