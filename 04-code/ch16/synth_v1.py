"""Listing 16.1: synthetic v1 and the extractor stand-in's self-scored accuracy on it (the day-44 number)."""
import _paths  # noqa: F401
from collections import Counter
from claimsgen import generate, V1
from extract_standin import extract
from score import score
from runs import SYN_SEED, SYN_N

docs = generate(V1, SYN_N, SYN_SEED)
sc = score(docs, [extract(d, "v1") for d in docs])
print(f"profile: {V1.name}")
print(f"documents {len(docs)}  channels {dict(Counter(d['channel'] for d in docs))}")
print(f"document types {dict(Counter(d['doc_type'] for d in docs))}")
print(f"documents with any exception tag: {sum(1 for d in docs if d['tags'])}")
print("--- one synthetic document (D0001) ---")
print(docs[1]["text"].rstrip())
print("--- extractor stand-in v1, scored against the generator's own gold values ---")
print(f"field accuracy {sc['accuracy']:.0%}  ({sc['correct']:,} of {sc['fields']:,} fields)")
print("  " + "  ".join(f"{f} {a / b:.0%}" for f, (a, b) in list(sc["per_field"].items())[:5]))
print("  " + "  ".join(f"{f} {a / b:.0%}" for f, (a, b) in list(sc["per_field"].items())[5:]))
