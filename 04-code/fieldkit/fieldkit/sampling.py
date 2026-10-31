"""The sample: stratified, de-identified where it must be, and signed for (Chapter 16, fieldkit v2.1).

`allocate` splits a sample size across strata in proportion to the population, with a floor per stratum so small
strata can be measured at all, and an oversample for strata the customer's experts flag as exceptions. Each stratum
carries a design weight (population share over sample share) so a weighted accuracy estimates the population and an
unweighted one does not pretend to. `Manifest` records every drawn file with a content hash, who drew it, who signed
for it, where it lives and when it is deleted.
"""
from __future__ import annotations

import hashlib
import math
from dataclasses import dataclass, field


def allocate(population, n, floor=10, oversample=None):
    """population: {stratum: count}. oversample: {stratum: factor}. Returns {stratum: (allocated, weight)}."""
    oversample = oversample or {}
    total = sum(population.values())
    raw = {s: population[s] / total * n * oversample.get(s, 1.0) for s in population}
    alloc = {s: min(population[s], max(floor, math.floor(v))) for s, v in raw.items()}
    # bring the total back to n, trimming the largest strata first (never below the floor)
    while sum(alloc.values()) > n:
        s = max((s for s in alloc if alloc[s] > floor), key=lambda s: alloc[s])
        alloc[s] -= 1
    while sum(alloc.values()) < n:
        s = max(alloc, key=lambda s: raw[s] - alloc[s])
        alloc[s] += 1
    out = {}
    for s, a in alloc.items():
        w = (population[s] / total) / (a / n) if a else 0.0
        out[s] = (a, round(w, 2))
    return out


def weighted_accuracy(per_stratum, plan):
    """per_stratum: {stratum: accuracy}; plan from allocate. Population estimate of accuracy."""
    num = sum(per_stratum[s] * plan[s][0] * plan[s][1] for s in per_stratum)
    den = sum(plan[s][0] * plan[s][1] for s in per_stratum)
    return num / den if den else float("nan")


def sha256(text):
    return hashlib.sha256(text.encode()).hexdigest()


@dataclass
class Manifest:
    name: str
    drawn_by: str
    signed_by: str
    location: str
    delete_on: str
    rows: list = field(default_factory=list)

    def add(self, file_id, stratum, content):
        self.rows.append({"file": file_id, "stratum": stratum, "sha256": sha256(content)})

    def verify(self, contents):
        """contents: {file_id: text}. Returns the files whose hash no longer matches (changed or missing)."""
        return [r["file"] for r in self.rows if r["file"] not in contents or sha256(contents[r["file"]]) != r["sha256"]]

    def header(self):
        return (f"manifest {self.name}: {len(self.rows)} files  drawn by {self.drawn_by}  signed for by {self.signed_by}\n"
                f"  location {self.location}  delete on {self.delete_on}")
