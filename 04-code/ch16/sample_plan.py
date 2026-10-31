"""Listing 16.5: the gold-set draw plan (300 files, stratified) and its signed manifest.

Population shares are estimated from the 200-file sample (stand-in for Caldwell's intake counts, which Kessler's
team pulls from the claims system). Exceptions the adjusters flagged are oversampled; every stratum gets a floor."""
from collections import Counter
import _paths  # noqa: F401
from standin_sample import sample
from fieldkit.sampling import allocate, weighted_accuracy, Manifest
from extract_standin import extract
from score import score

real = sample()


def stratum(d):
    if d["doc_type"] != "first notice of loss":
        return d["doc_type"]
    return f"first notice, {d['channel']}"


pop = Counter(stratum(d) for d in real)
scale = 14_200 / len(real)              # stand-in: about 14,200 documents in a quarter's intake
population = {s: round(c * scale) for s, c in pop.items()}
plan = allocate(population, 300, floor=20, oversample={"first notice, fax": 1.5, "first notice, mail": 1.5})
print("stratum                    population   drawn  weight")
for s in sorted(plan, key=lambda s: -population[s]):
    print(f"  {s:<24} {population[s]:9,}   {plan[s][0]:5d}  {plan[s][1]:5.2f}")
print(f"  {'total':<24} {sum(population.values()):9,}   {sum(a for a, _ in plan.values()):5d}")

# what the weights do: the same stratum accuracies, unweighted vs weighted (extractor v2 on the 200, development)
acc = {}
for s in plan:
    docs = [d for d in real if stratum(d) == s]
    acc[s] = score(docs, [extract(d, "v2") for d in docs])["accuracy"]
unweighted = sum(acc[s] * plan[s][0] for s in plan) / 300
print(f"stratum accuracies applied to the plan: unweighted {unweighted:.1%}, weighted {weighted_accuracy(acc, plan):.1%}")

m = Manifest("gold-set-300 (draw plan)", drawn_by="Natarajan (claims system query)", signed_by="Kessler",
             location="Caldwell AWS account, bucket claims-eval, prefix gold/", delete_on="engagement end + 90 days")
for d in real[:5]:
    m.add(d["id"], stratum(d), d["text"])
print(m.header())
for r in m.rows[:3]:
    print(f"  {r['file']}  {r['stratum']:<22} sha256 {r['sha256'][:16]}...")
changed = {d["id"]: d["text"] for d in real[:5]}
changed[real[2]["id"]] += " "
print(f"verify after a one-space edit to {real[2]['id']}: changed {m.verify(changed)}")
