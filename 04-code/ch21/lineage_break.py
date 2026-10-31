"""Listing 21.5: failure injection. A reconciliation output whose lineage breaks at an
un-versioned currency table, and the same output with the table versioned."""
import sys
import _paths  # noqa: F401
from fieldkit.lineage import LineageStore, RefTables

FX = {66: {"EUR/USD": 1.0853, "PLN/USD": 0.2511}, 81: {"EUR/USD": 1.0838, "PLN/USD": 0.2507}}
INVOICE_EUR, CONTRACT_USD = 9870.00, 10299.41
SHARED = {"file:/pennant-finance/shared/fx_rates.csv": FX[66]}   # overwritten every morning


def overbilling(eur, rate, contract):
    return round(round(eur * rate, 2) - contract, 2)


def build(store, fx_ref):
    src = store.add("source", uri="mail/2026/hls-inv-77310.pdf", sha256="9f2c41d0a7be", received="day 66 06:12",
                    sender="Harbor Line Shipping")
    pg = store.add("page", [src], page=1, legibility=0.91)
    ex = store.add("extraction", [pg], method="template HLS-INV-03 + OCR 4.1", fields={"total_eur": INVOICE_EUR},
                   scorer="pennant-qs-1.0")
    rc = store.add("source", uri="rates/blue-ridge-hls-2026q3.pdf", sha256="51aa0c93e8f7", received="day 40")
    rp = store.add("page", [rc], page=4)
    rx = store.add("extraction", [rp], method="rate-card parser 1.2", fields={"contract_usd": CONTRACT_USD})
    rate = (store.refs.get(fx_ref) if "@" in fx_ref else SHARED[fx_ref])["EUR/USD"]
    calc = store.add("calculation", [ex, rx], function="reconcile.overbilling", code="git 4be1c09",
                     refs={"fx_rates": fx_ref}, value=overbilling(INVOICE_EUR, rate, CONTRACT_USD))
    claim = store.add("claim", [calc], text="HLS invoice 77310 over-billed", value=overbilling(INVOICE_EUR, rate, CONTRACT_USD))
    return store.add("release", [claim], report="freight-audit weekly, day 66", approved_by="Dana Whitaker")


def recompute(node, store):
    ref = node.attrs["refs"]["fx_rates"]
    rate = (store.refs.get(ref) if "@" in ref else SHARED[ref])["EUR/USD"]
    return overbilling(INVOICE_EUR, rate, CONTRACT_USD)


SOURCES_NOW = {"mail/2026/hls-inv-77310.pdf": "9f2c41d0a7be", "rates/blue-ridge-hls-2026q3.pdf": "51aa0c93e8f7"}

if __name__ == "__main__":
    fixed = len(sys.argv) > 1 and sys.argv[1] == "fixed"
    refs = RefTables()
    store = LineageStore(refs)
    path = "file:/pennant-finance/shared/fx_rates.csv"
    ref = refs.register("fx_rates", FX[66], "day 66 07:00", "Marisol Vega (treasury)") if fixed else path
    rel = build(store, ref)
    claim = [n for n in store.chain(rel) if n.kind == "claim"][0]
    print(("FIXED" if fixed else "BROKEN") + f" run. Released on day 66: USD {claim.attrs['value']:,.2f} over-billed")
    print("chain:", " -> ".join(store.kinds_covered(rel)), f"({len(store.chain(rel))} nodes)")
    SHARED[path] = FX[81]   # day 81: finance has overwritten the file fifteen times since
    if fixed:
        refs.register("fx_rates", FX[81], "day 81 07:00", "Marisol Vega (treasury)")
    print("day 81, examiner asks how USD 412.50 was produced")
    probs = store.verify(rel, sources=SOURCES_NOW, recompute=recompute)
    print("verify:", "chain holds, recomputed value matches" if not probs else f"{len(probs)} problems")
    for p in probs:
        print("  " + p)
    if fixed:
        print(f"reference tables retained: {len(refs)}; cited version {ref} as_of {refs.meta(ref)['as_of']}, owner {refs.meta(ref)['owner']}")
