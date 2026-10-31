"""Listing 16.4: the representativeness report, run on day 53 for v1 and on day 58 for v2. Label-free."""
import _paths  # noqa: F401
from claimsgen import generate, V1
from standin_sample import sample
from features import features
from profile_v2 import profile_from_sample
from fieldkit.synthetic import RepresentativenessReport
from runs import SYN_SEED, SYN_N, V2_SEED

real = sample()


def report(docs, name):
    return RepresentativenessReport([features(d) for d in docs], [features(d) for d in real],
                                    [d["tags"] for d in docs], [d["tags"] for d in real], name=name).run()


r1 = report(generate(V1, SYN_N, SYN_SEED), "synthetic v1 vs the 200 (day 53)")
print(r1.render())
print()
v2 = profile_from_sample(real)
r2 = report(generate(v2, SYN_N, V2_SEED), "synthetic v2 vs the 200 (day 58)")
print(r2.render())
