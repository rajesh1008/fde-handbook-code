"""Figure 21.1: Pennant's six sources in the data-readiness register on day 62, owner and status per source."""
import re
from _common import S, save, blank, text
t = text("register")
rows = re.findall(r"^  (\w+)\s+owner (.+?)\s+fresh .*?(READY|FINDINGS \d)$", t, re.M)
short = {"tms_nightly_csv": "TMS nightly CSV", "carrier_edi_210_214": "carrier EDI 210/214", "mailbox_scans": "mailbox scans",
         "eu_customs_declarations": "EU customs", "fx_rates_csv": "FX rates CSV", "carrier_rate_cards": "rate cards"}
fig, ax = S.figure(height=3.9)
blank(ax, (0, 10), (0, 6))
for i, (name, owner, status) in enumerate(rows):
    x, y = 0.15 + (i % 3) * 3.3, 3.3 if i < 3 else 0.6
    ok = status == "READY"
    S.box(ax, x, y, 3.0, 1.9, short[name], role="approval" if ok else "blocker", fs=11, ls="-" if ok else "--")
    S.label(ax, x + 1.5, y + 0.45, owner if owner != "-" else "no owner", fs=10, ha="center")
    S.label(ax, x + 1.5, y + 0.12, "ready" if ok else status.lower().replace("findings", "findings:"), fs=10, ha="center",
            color=S.PAL["ink"], weight="bold")
save(fig, 1, kind="diagram", data="04-code/ch21/output/register.txt")
