"""Listing 50.1: the deterministic spread for Northgate Fabrication Ltd, ratios and covenant tests with lineage."""
import memo, world as W
print(f"{W.BORROWER}  fiscal 2025  {W.STATEMENT['standard']}  {W.STATEMENT['currency']} {W.STATEMENT['unit']}  (synthetic)")
print("cross-footing:", "; ".join(memo.crossfoot(W.STATEMENT)) or "foots")
store, ext, calc = memo.spread()
print(f"lineage nodes: {len(store.nodes)}  reference tables: {len(store.refs)}")
print(f"{'ratio':<15}{'value':>9}  covenant      result   headroom")
for r, v, op, t, res, head, unit in memo.covenant_lines(store, calc):
    if r == "tnw":
        print(f"{r:<15}{'C$' + format(v, ',.0f') + 'k':>9}  {op} C${t / 1000:,.0f}M{'':<5}  {res:<7}  C${head:,.0f}k")
    else:
        print(f"{r:<15}{v:>8.2f}x  {op} {t:.2f}x{'':<5}  {res:<7}  {head:.2f}x")
print("explain dscr:")
for line in store.explain(calc["dscr"]):
    print("  " + line)
bad = dict(W.STATEMENT, fields=dict(W.STATEMENT["fields"], equity=(13040, 2)))
print("injected statement (equity keyed as 13,040):", "; ".join(memo.crossfoot(bad)), "-> quarantined, no draft")
