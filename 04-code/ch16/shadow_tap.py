"""Listing 16.6: a shadow tap that keeps agreement and profile only, proved by canaries.

Run 1 is the tap as first written, with a debug line left in. Run 2 removes it. Both pass the same 200 stand-in
documents plus three canary documents, then scan every file the tap wrote."""
import random
import shutil
import tempfile
import _paths  # noqa: F401
from claimsgen import make_doc
from standin_sample import sample, REAL_STRUCTURE
from extract_standin import extract
from features import features
from fieldkit.shadow import ShadowTap, make_canary, scan_stores

real = sample()
rng = random.Random(56)
canaries = []
for j in range(3):
    c = make_canary(rng)
    d = make_doc(900 + j, rng, REAL_STRUCTURE, dict(doc_type="first notice of loss", claimant=c["claimant_name"]))
    d["text"] = d["text"].replace(d["gold"]["policy_number"] or "HPX", c["policy_number"]) + f"\nref {c['token']}\n"
    d["gold"]["policy_number"] = c["policy_number"]
    canaries.append((d, c))

for run, debug in (("run 1 (as first written)", True), ("run 2 (debug line removed)", False)):
    store = tempfile.mkdtemp(prefix="shadow16-")
    tap = ShadowTap(secret="caldwell-held-key", store_dir=store, debug_log=debug)
    for d in real + [d for d, _ in canaries]:
        tap.observe(d["id"], d["text"], extract(d, "v2"), d["gold"], features(d))
    tokens = [v for _, c in canaries for k, v in c.items()]
    hits = scan_stores(store, tokens)
    files = sorted({h[0] for h in hits})
    print(f"{run}: observed {len(tap.rows)} documents, canary tokens {len(tokens)}, hits {len(hits)} in {files or 'no file'}"
          f"  -> {'FAIL' if hits else 'PASS'}")
    if not debug:
        ag = tap.agreement()
        print("  kept per document: keyed hash, field agreement, 9 profile features; no text, no values")
        print("  agreement with adjusters (development, stand-in): " +
              ", ".join(f"{f} {v:.0%}" for f, v in list(ag.items())[:5]))
    shutil.rmtree(store)
