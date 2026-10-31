"""Section 27.4: no recommendation below the floor. The day 133 rehearsal on cal-600's checked half: each field
reworked once with the suggestion shown and once keyed from the source (stand-in reviewer rates)."""
import common as C
import world as W

_, _, chk = C.cal()
m, th = C.model(), C.thresholds()
edges = [0.0, 0.2, th.floor, 0.7, th.proceed, 1.01]
print(f"floor {th.floor:.2f}, proceed {th.proceed:.2f}; {len(chk):,} fields")
print(f"{'calibrated score':>17s} {'fields':>6s} {'model right':>11s} {'error, shown':>12s} {'error, keyed':>12s}")
rows = []
for a, b in zip(edges, edges[1:]):
    its = [i for i in chk if a <= m.score(i) < b]
    if not its:
        continue
    sh = sum(not W.review_outcome(i, "review", True) for i in its) / len(its)
    ke = sum(not W.review_outcome(i, "review", False) for i in its) / len(its)
    rows.append(dict(lo=a, hi=min(b, 1.0), n=len(its), right=C.acc(its), shown=sh, keyed=ke))
    print(f"{a:7.2f} to {min(b, 1.0):4.2f} {len(its):6,d} {C.acc(its):11.1%} {sh:12.1%} {ke:12.1%}")
print()
print("below the floor a shown value is wrong more often than right, and reviewers on poor pages accept it;")
print("above the floor the suggestion is about as safe as keying and needs only a check")
C.dump("floor", dict(rows=rows, floor=th.floor, proceed=th.proceed))
