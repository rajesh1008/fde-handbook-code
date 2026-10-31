"""The year after: Pennant (managed service with retention, as signed) and Caldwell (runs it alone, 12-hour
retainer) at month 12 of the model. Usage: python yearafter.py   Stand-in values, labeled."""
import world as W
from fieldkit.service import two_year, summary

pn = W.PENNANT_PATHS["managed"]; cw = W.CALDWELL_PATHS["hybrid"]
rp, rc = two_year(pn, W.items(W.PENNANT0)), two_year(cw, W.items(W.CALDWELL0))
sp, sc = summary(pn, rp), summary(cw, rc)
print("THE YEAR AFTER  month 12 of the model  (deterministic stand-in)")
print(f"Pennant: managed service with retention, month 12 ends engagement day {W.PN_START + 360}")
print(f"Caldwell: runs it alone, 12-hour retainer, month 12 ends engagement day {W.CW_START + 360}")
print(f"{'measure':<44}{'Pennant':>12}{'Caldwell':>12}")
rows = [("readiness at start", f"{W.score(W.items(W.PENNANT0)).gated:.2f}", f"{W.score(W.items(W.CALDWELL0)).gated:.2f}"),
        ("readiness at month 12 (with use-decay)", f"{sp[1]['readiness']:.3f}", f"{sc[1]['readiness']:.3f}"),
        ("lowest readiness in year one", f"{min(r.readiness for r in rp[:12]):.3f}", f"{min(r.readiness for r in rc[:12]):.3f}"),
        ("takeover hours at month 12", f"{sp[1]['takeover']}", f"{sc[1]['takeover']}"),
        ("customer cost, year one", f"${sp[1]['customer']:,}", f"${sc[1]['customer']:,}"),
        ("Northlight operations revenue, year one", f"${sp[1]['revenue']:,}", f"${sc[1]['revenue']:,}"),
        ("Northlight gross profit, year one", f"${sp[1]['gp']:,}", f"${sc[1]['gp']:,}"),
        ("Northlight margin on the line, year one", f"{sp[1]['margin']*100:.1f}%", f"{sc[1]['margin']*100:.1f}%"),
        ("FDE share consumed, year one", f"{sp[1]['fde']:.2f}", f"{sc[1]['fde']:.2f}"),
        ("vendor-only runbook steps", f"{pn.vendor_only_steps}", f"{cw.vendor_only_steps}"),
        ("readiness at month 24", f"{sp[2]['readiness']:.3f}", f"{sc[2]['readiness']:.3f}")]
for m, a, b in rows:
    print(f"{m:<44}{a:>12}{b:>12}")
