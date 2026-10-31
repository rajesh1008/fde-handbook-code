"""Listing 21.1: Pennant's per-source register, and the weight field that meant two things."""
import _paths  # noqa: F401
from fieldkit.quality import SourceSpec, SourceRegister
from pennant import u

SOURCES = [
    SourceSpec("tms_nightly_csv", "Kofi Mensah", {"shipment_id": "TMS shipment key", "weight_kg": "gross kg declared by shipper",
               "dims_cm": "L x W x H per package", "status": "TMS leg status"}, "read; no write-back", 26,
               ("reconciliation", "status"), True),
    SourceSpec("carrier_edi_210_214", "Dana Whitaker", {"invoice_no": "carrier invoice number", "weight": "chargeable kg (max of gross and volumetric)",
               "amount": "invoice total in invoice currency", "status": "carrier status code"}, "read", 24,
               ("reconciliation", "status"), True),
    SourceSpec("mailbox_scans", "Dana Whitaker", {"page": "scanned page image", "invoice_no": "printed invoice number"},
               "read; retained 30 days by mail policy", 48, ("reconciliation",), True),
    SourceSpec("eu_customs_declarations", None, {"declarant_id": "EORI", "hs_codes": "HS codes", "value": "customs value"},
               "read; GDPR applies to named individuals", None, (), True),
    SourceSpec("fx_rates_csv", None, {"EUR/USD": "rate used by finance that morning"}, "read", 24, ("reconciliation",), False),
    SourceSpec("carrier_rate_cards", "Dana Whitaker", {"lane": "origin-destination lane", "rate": "contracted USD per chargeable kg"},
               "read", 24 * 90, ("reconciliation", "audit"), True),
]


def weights(n=600):
    """TMS gross kg against the carrier's billed weight on n freight legs."""
    naive = registered = 0
    for i in range(n):
        gross = round(300 + 9000 * u(i, "g"), 1)
        vol = round(gross * (0.4 + 1.1 * u(i, "v")), 1)       # volumetric kg from TMS dims / 6000
        chargeable = max(gross, vol)
        billed = chargeable * (1.12 if u(i, "over") < 0.024 else 1.0)  # a real overbilling
        if abs(billed - gross) > 0.5:
            naive += 1
        if abs(billed - chargeable) > 0.5:
            registered += 1
    return n, naive, registered


if __name__ == "__main__":
    reg = SourceRegister(SOURCES)
    print("Pennant data-readiness register, day 62 (deterministic stand-in)")
    for s in SOURCES:
        f = reg.findings(s.name)
        print(f"  {s.name:<24} owner {s.owner or '-':<14} fresh {str(s.freshness_hours or '-'):>5} h  "
              f"{'READY' if not f else 'FINDINGS ' + str(len(f))}")
        for x in f:
            print("      " + x)
    print("use checks:")
    for args in [("fx_rates_csv", ["EUR/USD"], 3, "audit"), ("eu_customs_declarations", ["value"], 3, "reconciliation"),
                 ("tms_nightly_csv", ["weight_kg"], 31, "reconciliation")]:
        print(f"  {args[0]} for {args[3]}: " + ("; ".join(reg.check_use(*args)) or "ok"))
    print("same meaning of weight in TMS and carrier invoice?",
          reg.specs["tms_nightly_csv"].meanings["weight_kg"] == reg.specs["carrier_edi_210_214"].meanings["weight"])
    n, naive, registered = weights()
    print(f"freight legs compared: {n}")
    print(f"  weight mismatches, raw field against raw field: {naive} ({naive / n:.1%})")
    print(f"  weight mismatches, chargeable against chargeable: {registered} ({registered / n:.1%})")
