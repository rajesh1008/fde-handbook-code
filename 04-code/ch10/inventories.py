"""Systems inventories for the three customers, as fieldkit.integration Lines.

Hours are Northlight's estimates (illustrative). Pennant's per-layout hours come from the timed spike on the first
Pennant sample (six layouts mapped and timed in the hours ledger, days 18 to 20); everything else is a labeled
deterministic stand-in. No customer data is in this lab.
"""
import _path  # noqa: F401
from fieldkit.integration import Inventory, Line

R, D, V, P, Q = ("reconstructed from supplied artifact", "direct customer fact", "vendor position",
                 "proposed design", "decision required")

# Pennant layouts in five kinds (41 in all, Chapter 4); hours per layout from the timed spike
PENNANT_KINDS = [  # kind, layouts, low, likely, high (hours per layout)
    ("X12 214 status", 17, 10, 13, 20),
    ("EDIFACT IFTSTA", 9, 13, 17, 26),
    ("carrier PDF", 8, 18, 24, 36),
    ("scanned paper", 4, 26, 34, 52),
    ("photo of a form", 3, 28, 36, 58),
]

def _tms_alt():
    return [
        Line("P-T1", "access", "TMS nightly export", "parse the 02:00 CSV drop, schema-drift guard", 45, 60, 85, D,
             "TMS status leaves only as a nightly CSV on the managed file transfer server", "integration architect"),
        Line("P-T2", "exceptions", "carrier EDI 214 stream", "rebuild intraday status from EDI, reconcile with CSV",
             140, 190, 260, P, "intraday status can be rebuilt from carrier messages", "VP Operations"),
        Line("P-T3", "environments", "replay environment", "30 days of CSV and EDI replayed (no TMS sandbox)",
             95, 120, 160, D, "no TMS test instance exists", "integration architect"),
        Line("P-T4", "gateways", "managed file transfer", "MFT route, firewall rule, two change-board cycles",
             50, 70, 100, R, "change board meets every second Thursday", "integration architect"),
        Line("P-T5", "identity", "MFT service identity", "service identity and key rotation for the SFTP pull",
             35, 50, 70, R, "MFT keys rotate every 90 days", "integration architect"),
    ]

def pennant(day=24, denied=True):
    """Pennant Logistics. day 21: the estimate as first written; day 24: after the architects' answer."""
    inv = Inventory("Pennant Logistics", (420, 500, 620), day=21)
    for i, (kind, n, lo, li, hi) in enumerate(PENNANT_KINDS, 1):
        inv.add(Line(f"P-F{i}", "formats", kind, f"{n} layouts x {li} h", n * lo, n * li, n * hi, R,
                     f"timed spike: {kind} mapped on the first sample"))
    inv.add(
        Line("P-A1", "access", "carrier EDI mailbox", "read the SFTP EDI mailbox", 15, 20, 30, D,
             "EDI mailbox readable by a service identity", "integration architect"),
        Line("P-A2", "access", "TMS status API", "pull shipment status from the TMS REST API (v2)", 30, 40, 60, V,
             "TMS vendor documentation lists a shipment-status API", "integration architect", alt=_tms_alt()),
        Line("P-A3", "access", "EU shipments", "data processing terms and EU residency for EU shipments", 25, 40, 70, Q,
             "EU shipment documents may be processed in the US region", "data protection officer",
             alt=[Line("P-A3b", "environments", "EU region", "second deployment in an EU region", 90, 120, 170, P,
                       "EU documents stay in an EU region", "data protection officer")]),
        Line("P-I1", "identity", "reconciliation clerks", "clerk identity stamped on every match decision", 25, 35, 55, P,
             "clerks sign in with Pennant's identity provider", "IT security lead"),
        Line("P-E1", "exceptions", "exception codes", "carrier exception codes (11 countries) to 14 reason codes",
             40, 55, 80, R, "reason-code table supplied on day 12"),
        Line("P-N1", "environments", "test project", "test project in Pennant's Google Cloud organization", 20, 30, 45, D,
             "test project granted day 16", "cloud platform lead"),
        Line("P-G1", "gateways", "API gateway", "onboard to Pennant's API gateway", 15, 20, 30, R,
             "gateway onboarding guide supplied on day 9"),
    )
    if denied:
        inv = inv.deny("P-A2", "Kofi Mensah, integration architect", 23)
        inv.day = day
    return inv

def caldwell():
    inv = Inventory("Caldwell Mutual", (560, 640, 760), day=26)
    inv.add(
        Line("C-A1", "access", "claims-core", "read-only service account via architecture board", 45, 60, 90, D,
             "a read-only account needs an architecture board review", "Priya Natarajan"),
        Line("C-A2", "access", "claims-core", "attach document to an existing claim (write path)", 50, 70, 110, P,
             "attach-to-claim allowed as a proposal accepted by a senior adjuster", "Daniel Reyes",
             alt=[Line("C-A2b", "exceptions", "adjuster queue", "proposal queue only, adjuster attaches by hand",
                       30, 40, 60, P, "no write path", "Anne Kessler")]),
        Line("C-I1", "identity", "adjuster SSO group", "acting-for identity stamped on every read", 40, 55, 80, R,
             "SSO group per claims unit, from the day-24 session"),
        Line("C-F1", "formats", "nine intake paths", "mail scan, fax, email, portal and broker formats", 150, 190, 260, R,
             "path inventory P01 to P11, P09 and P11 out of scope"),
        Line("C-E1", "exceptions", "name search", "draft a service-desk request when no policy number", 30, 45, 70, P,
             "underwriting service desk accepts drafted requests", "Priya Natarajan",
             alt=[Line("C-E1b", "exceptions", "name search", "route to an adjuster queue", 15, 25, 40, P,
                       "adjuster searches by hand", "Anne Kessler")]),
        Line("C-N1", "environments", "AWS sandbox", "sandbox account, S3 with a Caldwell-held key", 30, 40, 60, D,
             "sandbox account offered on day 22", "Priya Natarajan"),
        Line("C-G1", "gateways", "model gateway", "mandated gateway, keys rotate every 7 days", 60, 80, 110, D,
             "gateway is the only route to a model", "Priya Natarajan"),
    )
    return inv

def greystone():
    inv = Inventory("Greystone Health", (450, 520, 640), day=18)
    inv.add(
        Line("G-A1", "access", "EHR referrals", "referral data through an EHR provider change", 160, 220, 320, Q,
             "the EHR provider will build a referral export", "Michael Hart",
             alt=[Line("G-A1b", "formats", "print-to-file", "print-to-file export plus fax-grade OCR", 300, 400, 560, P,
                       "referrals printed to file by the EHR", "Michael Hart")]),
        Line("G-A2", "access", "fax path", "fax server capture for the 38% fax path", 70, 90, 130, R,
             "fax volumes at two clinics over four days (stand-in)"),
        Line("G-I1", "identity", "Entra coordinators", "coordinator identity and minimum-necessary stamping", 80, 110, 160, P,
             "coordinators sign in with Microsoft Entra ID", "Sam Oakley"),
        Line("G-F1", "formats", "referral packets", "four referral paths plus fax packets", 90, 120, 170, R,
             "referral paths R01 to R05 from discovery"),
        Line("G-E1", "exceptions", "red flags", "red flags always route to a clinician", 35, 50, 75, D,
             "Michael Hart's ruling, day 18"),
        Line("G-N1", "environments", "no EHR test system", "de-identified replay on Azure private endpoints", 80, 110, 160, P,
             "no EHR test environment is available to vendors", "Sam Oakley"),
        Line("G-G1", "gateways", "model gateway", "Greystone's gateway offers the model calls we need", 20, 30, 45, V,
             "gateway documentation lists chat and embedding endpoints", "Sam Oakley",
             alt=[Line("G-G1b", "gateways", "model gateway", "work around a missing endpoint inside the tenant", 100, 140, 210, P,
                       "a missing endpoint is replaced inside Greystone's tenant", "Sam Oakley")]),
    )
    return inv

ALL = {"caldwell": caldwell, "greystone": greystone, "pennant": pennant}
