"""Listings 50.2 and 50.3: the draft, the numeric gate, the currency lint and the lineage check, clean and injected."""
import sys, memo
mode = sys.argv[1] if len(sys.argv) > 1 else "clean"
store, ext, calc = memo.spread()
claims = memo.draft(store, ext, calc, inject=None if mode == "clean" else mode)
for i, (t, _) in enumerate(claims, 1):
    print(f"[{i}] {t}")
g, c, lin = memo.check(store, claims)
print("numeric gate:", "pass" if not g else "BLOCK"); [print("  " + p) for p in g]
print("currency lint:", "pass" if not c else "BLOCK"); [print("  " + p) for p in c]
print("lineage check:", "holds" if not lin else "FAILS"); [print("  " + p) for p in lin]
print("draft reaches the credit officer:", "yes" if not (g or c or lin) else "no; regenerated, then routed for review if it fails twice")
