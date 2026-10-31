"""Listing 26.4: validating a judge against Anne's adjusters, with the injected failure (judge_v1)."""
import json
from world import gold_items, judge_v1, judge_v2, acc
from fieldkit.evals import JudgeValidation, cohen_kappa, corrected_interval, flip_rate

items = gold_items()
dev = [it for it in items if it.split == "dev"]
test = [it for it in items if it.split == "test"]
expert_t = [it.anne_ok for it in test]
print(f"held-out test split: {len(test) // 10} documents, {len(test)} fields; Anne's adjusters pass "
      f"{sum(expert_t)} ({sum(expert_t) / len(test):.1%})")
out = {}
for name, j in (("judge_v1 (Northlight rubric)", judge_v1), ("judge_v2 (Caldwell rubric)", judge_v2)):
    jt = [j(it) for it in test]
    v = JudgeValidation(jt, expert_t)
    runs = [[j(it, run=r) for it in test] for r in range(3)]
    ok, why = v.verdict_with_repeats(runs, max_flip=0.05, min_tpr=0.90, min_tnr=0.80, min_fail=30)
    p, lo, hi = corrected_interval(jt, [j(it) for it in dev], [it.anne_ok for it in dev], reps=2000)
    print(f"\n{name}")
    print(f"  passes {sum(jt)} of {len(jt)} ({sum(jt) / len(jt):.1%})   agrees with Anne on "
          f"{sum(a == b for a, b in zip(jt, expert_t)) / len(jt):.1%}   kappa {cohen_kappa(jt, expert_t):.2f}")
    print(f"  TP {v.tp}  FN {v.fn}  FP {v.fp}  TN {v.tn}   TPR {v.tpr:.2f}  TNR {v.tnr:.2f}")
    print(f"  not unanimous across three runs: {flip_rate(runs):.1%} of fields")
    print(f"  corrected with dev-split TPR/TNR: {p:.1%} (95% interval {lo:.1%} to {hi:.1%})")
    print(f"  verdict: {'VALID for Caldwell' if ok else 'NOT VALID: ' + '; '.join(why)}")
    out[name.split()[0]] = dict(raw=sum(jt) / len(jt), tpr=v.tpr, tnr=v.tnr, tp=v.tp, fn=v.fn, fp=v.fp, tn=v.tn,
                                corr=p, lo=lo, hi=hi, flips=flip_rate(runs), ok=ok)
print(f"\nAnne's adjusters on the test split, unweighted: {acc(test):.1%}")
out["anne"] = acc(test)
json.dump(out, open("output/judge_validation.json", "w"), indent=1)
