"""Listing 4.6: the oversight profile. Fix the reliability of what goes out without review, and report the
share of work that must be reviewed to hold it. Qualified on held-out cases, not on the cases used to set
the threshold.

The data here is a seeded STAND-IN: 400 documents x 10 fields with synthetic confidences, shaped like the
day-2 failure mix. It proves the procedure, not Caldwell's numbers; the real profile is computed on Anne
Kessler's gold set (Chapter 26)."""
import math
import random


def wilson_lower(k, n, z=1.96):
    if n == 0:
        return 0.0
    p = k / n
    d = 1 + z * z / n
    c = p + z * z / (2 * n)
    r = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n))
    return (c - r) / d


def simulate(seed, n_docs=400, fields=10, accuracy=0.72, sharpness=3.0):
    """(confidence, correct) per field. sharpness: how well confidence separates right from wrong."""
    rng = random.Random(seed)
    out = []
    for _ in range(n_docs * fields):
        correct = rng.random() < accuracy
        mu = 0.5 + (0.5 if correct else -0.5) * sharpness / 4
        conf = min(1.0, max(0.0, rng.gauss(mu, 0.18)))
        out.append((conf, correct))
    return out


def profile(rows, target, seed=7):
    rng = random.Random(seed)
    rows = rows[:]
    rng.shuffle(rows)
    cal, held = rows[: len(rows) // 2], rows[len(rows) // 2:]
    best = None
    for t in sorted({round(c, 3) for c, _ in cal}):
        auto = [ok for c, ok in cal if c >= t]
        if len(auto) >= 30 and wilson_lower(sum(auto), len(auto)) >= target:
            best = t
            break
    if best is None:
        return dict(threshold=None, review_share=1.0, held_precision=None, lower=None, qualifies=False)
    auto = [ok for c, ok in held if c >= best]
    k, n = sum(auto), len(auto)
    lower = wilson_lower(k, n)
    return dict(threshold=best, review_share=1 - n / len(held), held_precision=k / n if n else None,
                lower=lower, qualifies=lower >= target)


SYSTEMS = {"pipeline A": dict(seed=11, accuracy=0.72, sharpness=2.0),
           "pipeline B": dict(seed=12, accuracy=0.71, sharpness=1.3)}


def main(targets=(0.90, 0.95, 0.98, 0.99)):
    print("OVERSIGHT PROFILE  stand-in, 400 documents x 10 fields, threshold set on one half, checked on the other")
    for name, kw in SYSTEMS.items():
        rows = simulate(**kw)
        acc = sum(ok for _, ok in rows) / len(rows)
        print(f"{name}  field accuracy with no review {acc:.1%}")
        for tg in targets:
            p = profile(rows, tg)
            if p["threshold"] is None:
                print(f"  target {tg:.0%}  no threshold reaches it; everything is reviewed")
                continue
            print(f"  target {tg:.0%}  review {p['review_share']:5.1%}  held-out correct {p['held_precision']:.1%}"
                  f"  lower bound {p['lower']:.1%}  {'QUALIFIES' if p['qualifies'] else 'DOES NOT QUALIFY'}")


if __name__ == "__main__":
    main()
