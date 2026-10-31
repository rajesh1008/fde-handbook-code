"""Listings 50.9 and 50.10: shadow mode against credit officers' own memos, days 120 to 149. 600 drafts scored by
Harbourline's credit review team against the memo the officer wrote; 38 packages quarantined before drafting.
Deterministic stand-in: the records are constructed, not sampled, so the counts are exact every run."""
import json, sys
import _paths  # noqa: F401
from fieldkit.gates import wilson
import world as W

# per standard: (drafts scored, agree, equivalent, human wrong, agent loud, agent silent, drafted with review flags)
MIX = {"IFRS": (312, 286, 6, 5, 10, 5, 20), "ASPE": (226, 205, 5, 3, 10, 3, 14), "US GAAP": (62, 55, 1, 1, 1, 4, 4)}
OUTCOMES = ("agree", "equivalent", "human wrong", "agent loud", "agent silent")


def records(mix=MIX, scale=1.0):
    out, i = [], 0
    for std, (n, *parts) in mix.items():
        counts = [round(x * scale) for x in parts[:5]]
        counts[0] = round(n * scale) - sum(counts[1:])
        flags = round(parts[5] * scale)
        seq = [o for o, k in zip(OUTCOMES, counts) for _ in range(k)]
        for j, o in enumerate(seq):
            i += 1
            out.append(dict(memo=f"HL-M-{i:04d}", standard=std, outcome=o, decision="review" if j % max(1, len(seq) // max(1, flags)) == 0 and sum(r["decision"] == "review" for r in out if r["standard"] == std) < flags else "proceed",
                            day=W.DAYS["shadow"][0] + (i * 7) % 30))
    return out


def funnel(recs):
    q = sum(W.QUARANTINED.values())
    f = dict(seen=len(recs) + q, proceed=sum(r["decision"] == "proceed" for r in recs),
             review=sum(r["decision"] == "review" for r in recs), escalate=q, none=0, human=len(recs),
             agree=sum(r["outcome"] == "agree" for r in recs))
    for o, k in (("equivalent", "equivalent"), ("human wrong", "human_wrong"), ("agent loud", "loud"), ("agent silent", "silent")):
        f[k] = sum(r["outcome"] == o for r in recs)
    f["escalations"] = q
    return f


def by_standard(recs):
    rows = []
    for s in W.STANDARDS:
        rs = [r for r in recs if r["standard"] == s]
        k = sum(r["outcome"] == "agree" for r in rs); lo, hi = wilson(k, len(rs))
        rows.append((s, k, len(rs), lo, hi, sum(r["outcome"] == "agent silent" for r in rs)))
    return rows


if __name__ == "__main__":
    recs = records(); f = funnel(recs)
    if len(sys.argv) > 1 and sys.argv[1] == "json":
        print(json.dumps(f)); raise SystemExit
    k, n = f["agree"], f["human"]; lo, hi = wilson(k, n)
    print(f"shadow days {W.DAYS['shadow'][0]} to {W.DAYS['shadow'][1]}; scored by Harbourline credit review against each officer's own memo")
    print(f"packages seen {f['seen']}; quarantined before drafting {f['escalate']}; drafts scored {n}")
    print(f"agreement {k}/{n} = {k / n:.1%} (95% interval {lo:.1%} to {hi:.1%}); bid sentence bar 90%")
    print("disagreements: " + ", ".join(f"{o} {f[x]}" for o, x in (("equivalent", "equivalent"), ("human wrong", "human_wrong"),
                                                                     ("agent loud", "loud"), ("agent silent", "silent"))))
    print(f"{'standard':<9}{'agree':>8}{'scored':>8}{'rate':>8}   95% interval     silent")
    for s, k, n, lo, hi, sil in by_standard(recs):
        print(f"{s:<9}{k:>8}{n:>8}{k / n:>8.1%}   {lo:.1%} to {hi:.1%}   {sil}")
    print("sample size (BC-16, day 45): interval for each standard at the same rates")
    for total in (400, 600):
        rs = records(scale=total / 600)
        print(f"  {total} memos: " + "; ".join(f"{s} {k}/{n} {lo:.1%} to {hi:.1%} (width {(hi - lo) * 100:.1f} pts)"
                                           for s, k, n, lo, hi, _ in by_standard(rs)))
