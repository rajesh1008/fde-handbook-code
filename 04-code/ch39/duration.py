"""How long is long enough: four stopping rules on 2,000 simulated shadow windows. Deterministic stand-in.
Each window: a release whose true reference-mix agreement is drawn around rc-1's measured rates; with
probability 0.3 it carries a paper-channel regression; each five-day week is a holiday week with probability 0.2."""
import json, numpy as np
import _paths  # noqa: F401
import world as W, suite as U

rng = np.random.default_rng(3912)
_, _, since = U.gate(W.caldwell_window())
BASE = np.array([since[s][0] / since[s][1] for s in W.STRATA])
REF = np.array([W.REFERENCE[s] for s in W.STRATA]); HOL = np.array([W.HOLIDAY[s] for s in W.STRATA])
PAPER = np.array([s in W.REGRESSION for s in W.STRATA])
BAR, CAP, TRIALS = 0.85, 30, 2000


def wilson(k, n, z=1.96):
    p = k / n; den = 1 + z * z / n; c = (p + z * z / (2 * n)) / den
    h = z * np.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / den
    return c - h, c + h


def trial():
    rates = np.clip(BASE + rng.uniform(-0.09, 0.01) - (0.20 * PAPER if rng.random() < 0.3 else 0), 0.3, 0.99)
    truth = float(REF @ rates)
    hol = rng.random(CAP // 5 + 1) < 0.2
    n = np.zeros((CAP, 8), int); k = np.zeros((CAP, 8), int)
    for t in range(CAP):
        mix = HOL if hol[t // 5] else rng.dirichlet(REF * 400)
        n[t] = rng.multinomial(W.PER_DAY, mix); k[t] = rng.binomial(n[t], rates)
    return truth, n, k


def raw(n, k, a, b):
    return k[a:b].sum() / n[a:b].sum()


def decide(n, k):
    out = {}
    out["fixed 5 days"] = (raw(n, k, 0, 5) >= BAR, 5)
    out["fixed 10 days"] = (raw(n, k, 0, 10) >= BAR, 10)
    d = None
    for t in range(5, CAP + 1):
        daily = k[t - 5:t].sum(1) / n[t - 5:t].sum(1)
        if daily.max() - daily.min() <= 0.03:
            d = t; break
    d = d or CAP
    out["until stable"] = (raw(n, k, 0, d) >= BAR, d)
    d, go = CAP, False
    for t in range(10, CAP + 1):
        cov = n[:t].sum(0); mixd = 0.5 * np.abs(cov / cov.sum() - REF).sum()
        lo, hi = wilson(k[:t].sum(), n[:t].sum()); l5 = raw(n, k, t - 5, t)
        if cov.min() >= 60 and mixd <= 0.10 and lo <= l5 <= hi:
            rw = float(REF @ (k[:t].sum(0) / cov)); d, go = t, rw >= BAR; break
    out["Shadow Exit rule"] = (go, d)
    return out


res = {r: [] for r in ("fixed 5 days", "fixed 10 days", "until stable", "Shadow Exit rule")}
truths = []
for _ in range(TRIALS):
    truth, n, k = trial(); truths.append(truth)
    for r, (go, d) in decide(n, k).items():
        res[r].append((go, d, truth >= BAR))
bad = sum(1 for t in truths if t < BAR)
print(f"{TRIALS} simulated windows; {bad} releases truly below the 85% bar at the reference mix ({bad / TRIALS:.0%})")
print(f"{'rule':18} {'false go':>9} {'false hold':>11} {'median days':>12} {'p90 days':>9}")
table = {}
for r, v in res.items():
    fg = sum(1 for go, d, ok in v if go and not ok) / max(1, sum(1 for *_, ok in v if not ok))
    fh = sum(1 for go, d, ok in v if not go and ok) / max(1, sum(1 for *_, ok in v if ok))
    ds = sorted(d for _, d, _ in v)
    table[r] = (fg, fh, ds[len(ds) // 2], ds[int(len(ds) * 0.9)])
    print(f"{r:18} {fg:9.1%} {fh:11.1%} {ds[len(ds) // 2]:12} {ds[int(len(ds) * 0.9)]:9}")
json.dump(table, open("output/duration.json", "w"))
