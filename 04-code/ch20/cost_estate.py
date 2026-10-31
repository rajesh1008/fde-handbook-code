"""Listing 20.x: cost per scored document on each estate, read from that estate's own records."""
import _paths  # noqa: F401
from deploy import deploy
from estate_configs import CALDWELL, GREYSTONE, PENNANT_EU, with_
from fieldkit.estates import ModelPin, estate_cost

# Stand-in rates per 1,000 tokens (input, output) as each customer's bill or chargeback states them.
PRICES = {"caldwell": (0.0060, 0.0238), "greystone": (0.0055, 0.0220), "pennant": (0.0050, 0.0200)}
# Stand-in monthly fixed costs that exist only because the estate is private, logged and separate.
FIXED = {
    "caldwell": {"interface endpoints": 146.0, "log ingestion and retention": 85.0, "secret reads": 4.0,
                 "suite runner": 190.0},
    "greystone": {"private endpoints (4)": 29.0, "diagnostic log ingestion": 310.0, "key vault operations": 3.0,
                  "suite runner": 190.0},
    "pennant": {"service connect endpoints (2 regions)": 58.0, "logging": 40.0, "secret reads": 2.0,
                "suite runners (2 regions)": 380.0},
}
VOLUME = {"caldwell": 11244, "greystone": 2400, "pennant": 19500}   # documents a month (Caldwell canon; others stand-in)
EU_PIN = ModelPin("extract", "extract-2026-01", ("europe-west4",), "EU gold, day 114")

rows = {}
for label, cfg in (("Caldwell (AWS)", CALDWELL), ("Greystone (Azure)", GREYSTONE),
                   ("Pennant (Google Cloud)", with_(PENNANT_EU, model="extract-2026-01", pin=EU_PIN))):
    ev, rep, sinks = deploy(cfg)
    pin, pout = PRICES[cfg["customer"]]
    spend = sum(r["tokens_in"] / 1000 * pin + r["tokens_out"] / 1000 * pout for r in sinks.customer)
    per_doc = spend / len(sinks.customer)
    tin = sum(r["tokens_in"] for r in sinks.customer) / len(sinks.customer)
    c = estate_cost(per_doc, FIXED[cfg["customer"]], VOLUME[cfg["customer"]])
    rows[label] = c
    print(f"--- {label}: {len(sinks.customer)} records in the customer's sink, mean input tokens {tin:,.0f} ---")
    print(f"model cost per scored document   USD {c['model']:.4f}")
    print(f"fixed monthly                    USD {c['fixed_monthly']:,.2f}  ("
          + ", ".join(f"{k} {v:.0f}" for k, v in FIXED[cfg['customer']].items()) + ")")
    print(f"fixed per document at {VOLUME[cfg['customer']]:,}/month  USD {c['fixed_per_doc']:.4f}")
    print(f"total per scored document        USD {c['total']:.4f}")
    print(f"volume where fixed equals model  {c['volume_where_fixed_equals_model']:,} documents a month")
print("--- summary ---")
for k, c in rows.items():
    print(f"{k:24s} model {c['model']:.4f}  fixed {c['fixed_per_doc']:.4f}  total {c['total']:.4f}")
