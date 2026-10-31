"""Chapter 15: the same seven pipeline stages run on the synthetic set and on the first real sample.

STAND-IN: every stage is deterministic code; no model is called, so the numbers are about the
plumbing and the data, never about extraction accuracy (Chapter 16 measures that, with Anne Kessler
scoring). Synthetic data proves the plumbing, not the accuracy.
"""
import random, re, sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "fieldkit"))
from fieldkit.fixtures import caldwell_sample, DOC_TYPES

SCHEMA = ["claim_id", "policy_number", "loss_date", "doc_type", "pages", "ocr_confidence"]


def synthetic_claims(n=200, seed=6):
    """Built from the schema and from Anne Kessler's description of a claim file; no customer record used."""
    rng = random.Random(seed)
    return [dict(claim_id=f"CM-{2026_00000 + 3 * i:010d}", policy_number=f"HP{rng.randint(100000, 999999)}",
                 loss_date=f"2026-{rng.randint(1, 8):02d}-{rng.randint(1, 28):02d}", doc_type=rng.choice(DOC_TYPES),
                 pages=rng.choice([1, 2, 3, 4, 6]), ocr_confidence=round(rng.uniform(0.97, 0.995), 3))
            for i in range(n)]


STAGES = [
    ("1 manifest parses", lambda r: all(c in r for c in SCHEMA)),
    ("2 key valid", lambda r: bool(re.fullmatch(r"CM-\d{10}", str(r.get("claim_id", ""))))),
    ("3 policy number parses", lambda r: bool(re.fullmatch(r"HP\d{6}", r.get("policy_number", "")))),
    ("4 loss date normalizes", lambda r: bool(re.fullmatch(r"2026-(0[1-9]|1[0-2])-\d\d", r.get("loss_date", "")))),
    ("5 document type routes", lambda r: r.get("doc_type") in DOC_TYPES),
    ("6 recognition gate: auto", lambda r: r.get("ocr_confidence", 0) >= 0.80),
    ("7 page split: one job", lambda r: r.get("pages", 99) <= 25),
]


def run(rows):
    return {name: sum(1 for r in rows if fn(r)) for name, fn in STAGES}


syn, real = synthetic_claims(), caldwell_sample()
a, b = run(syn), run(real)
print(f"{'stage':<28}{'synthetic':>10}{'real':>8}  verdict")
same = 0
for name, _ in STAGES:
    pa, pb = 100 * a[name] / len(syn), 100 * b[name] / len(real)
    ok = abs(pa - pb) < 1
    same += ok
    print(f"{name:<28}{pa:>9.1f}%{pb:>7.1f}%  " + ("unchanged" if ok else f"differs by {pa - pb:.1f} points: the data, not the code"))
print(f"stages unchanged from synthetic to real: {same} of {len(STAGES)}")
print(f"files sent to review by the recognition gate: synthetic {len(syn) - a[STAGES[5][0]]} of {len(syn)}, "
      f"real {len(real) - b[STAGES[5][0]]} of {len(real)}")
