"""Per-customer evidence conventions: the same eight elements, a different home, reader, retention and identifier rule."""
import _paths  # noqa: F401
from fieldkit.lineage import digest

CONV = {
    "Caldwell": dict(home="claim file and model inventory entry", reader="internal audit; model risk (Catherine Doyle)",
                     retention=2555, ids="claim number; adjuster IDs A-1xx", text="fields in pack (validation recomputes)",
                     anchor="Caldwell log account, daily chain head"),
    "Greystone": dict(home="prior-authorization case record", reader="compliance; CMIO office (Michael Hart)",
                      retention=2190, ids="keyed referral token, never MRN", text="minimum necessary: field names and hashes",
                      anchor="Greystone Azure immutable blob, daily chain head"),
    "Pennant": dict(home="freight-audit file per invoice", reader="Dana Whitaker; internal audit", retention=365,
                    ids="invoice and shipment numbers; consignee keyed", text="hash-only run records; subject fields keyed store",
                    anchor="Pennant log store, daily chain head"),
    "Harbourline": dict(home="model inventory and credit memo file (bid stage)", reader="Helen Marsh (model risk)",
                        retention=None, ids="to be set with the bank", text="to be set with the bank",
                        anchor="to be set with the bank"),
}
ELEMENTS = ("document", "lineage", "retrieval", "prompt and model", "confidence and route", "decision", "review", "action")
print("PER-CUSTOMER EVIDENCE CONVENTIONS (one model, four homes)")
for c, v in CONV.items():
    print(f"  {c}")
    for k in ("home", "reader", "retention", "ids", "text", "anchor"):
        val = v[k] if k != "retention" else (f"{v[k]:,} days" if v[k] else "not yet agreed")
        print(f"    {k:<10} {val}")
    print(f"    config digest {digest([c, v, ELEMENTS])}")
print(f"  elements identical across customers: {len(ELEMENTS)} of {len(ELEMENTS)}")
