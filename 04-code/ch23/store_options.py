"""Section 23.1: whose embeddings, whose store. Three options Priya Natarajan compared on day 86 (stand-in rates)."""
import _paths  # noqa: F401
import caldwell_docs as C

TOK_PER_PASSAGE = 380          # Caldwell's real manual passages average about 380 tokens; the stand-in text is shorter
EMBED_USD_PER_M = 0.02         # gateway embedding deployment, stand-in rate
DIMS, BYTES = 1536, 4
PIN_DAYS = 90                  # Caldwell gateway rule: a dated deployment pin lasts at most 90 days
REVALIDATE_HOURS, LOADED_USD = 6, 46.0   # Anne's adjusters re-mark the question set after a re-embed

ix, recs, acl, versions = C.build()
n = len(ix.passages); toks = n * TOK_PER_PASSAGE
vec_mb = n * DIMS * BYTES / 1e6
embed_once = toks * EMBED_USD_PER_M / 1e6
reembed_event = embed_once + REVALIDATE_HOURS * LOADED_USD
options = [
    ("A vendor-hosted store", "Northlight cloud", "Northlight", 450.0, "documents leave Caldwell's account", "refused (security, day 86)"),
    ("B new managed vector service", "Caldwell AWS us-east-1", "Caldwell", 700.0, "new platform: architecture board, about six weeks", "deferred"),
    ("C pgvector on approved PostgreSQL", "Caldwell AWS us-east-1", "Caldwell", 38.0, "extension added to an approved runtime", "chosen (signed day 86)"),
]
print(f"library: {len(set(p.doc_id for p in ix.passages.values()))} files, {n:,} passages, {toks:,} tokens at {TOK_PER_PASSAGE} per passage")
print(f"vectors: {DIMS} dimensions, {vec_mb:.1f} MB; embedding the whole library once: USD {embed_once:.2f} (stand-in rate)")
print(f"re-embed event (pin replaced at most every {PIN_DAYS} days): compute USD {embed_once:.2f} + revalidation "
      f"{REVALIDATE_HOURS} h x USD {LOADED_USD:.0f} = USD {reembed_event:.2f}")
print()
print(f"{'option':36s} {'where vectors live':24s} {'key holder':11s} {'USD/month':>9s} {'USD/year incl. 4 re-embeds':>27s}  status")
for name, where, key, month, note, status in options:
    year = 12 * month + 4 * reembed_event
    print(f"{name:36s} {where:24s} {key:11s} {month:9.2f} {year:27.2f}  {status}; {note}")
print()
print("embedding model: Caldwell gateway deployment embed-2026-02, pinned day 86 under app identity nl-index")
print("rule: vectors from two embedding versions never share an index; a new pin means a full re-embed into a second")
print("      index, Anne's question set re-run on it, and a switch only if recall at ten does not fall")
