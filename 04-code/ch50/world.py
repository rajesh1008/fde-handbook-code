"""Chapter 50 world: Harbourline Bank, commercial lending. Deterministic stand-in data; every number is synthetic.
Days are Harbourline engagement days, counted from contract signature (Chapter 12). Currency: Canadian dollars (C$),
labeled at every use. Borrower fixture: Northgate Fabrication Ltd (synthetic). Not Harbourline's text or data."""
import _paths  # noqa: F401
from fieldkit import modelrisk as M

CUSTOMER = "Harbourline Bank"
PEOPLE = dict(model_risk="Helen Marsh", executive="David Okafor", architect="Martin Shaw", legal="Claire Dubois")

# 50.1 the workflow: twelve document formats, three accounting standards
FORMATS = (  # (format, documents in the 638 shadow-window packages)
    ("audited financial statements", 402), ("review engagement statements", 171), ("compilation statements", 65),
    ("interim management accounts", 590), ("receivables aging", 312), ("borrowing base certificate", 204),
    ("covenant compliance certificate", 611), ("corporate tax schedules", 280), ("appraisal report", 57),
    ("facility agreement", 638), ("relationship manager call notes", 1240), ("prior credit memo", 638))
STANDARDS = ("IFRS", "ASPE", "US GAAP")
PACKAGES = {"IFRS": 331, "ASPE": 241, "US GAAP": 66}          # packages in the shadow window, days 120 to 149
QUARANTINED = {"IFRS": 19, "ASPE": 15, "US GAAP": 4}          # failed cross-footing or unreadable: no draft

# 50.2 discovery
DISCOVERY = dict(days=(8, 21), relationship_managers=6, credit_officers=5, credit_review_analysts=2,
                 memos_observed=14, median_hours=5.2, spreading_and_ratio_hours=2.9)
STEPS = (  # (memo section, step, who does it)
    ("spread", "read the package and detect formats", "code"),
    ("spread", "capture tables from statements", "small model, checked by code"),
    ("spread", "map line items to the bank's chart", "reference table"),
    ("spread", "suggest a mapping for an unseen label", "small model, checked by code"),
    ("spread", "cross-foot every statement", "code"),
    ("spread", "quarantine a statement that fails", "code"),
    ("spread", "convert currency at the treasury rate", "reference table"),
    ("ratios", "compute DSCR, leverage, current ratio, TNW", "code"),
    ("ratios", "apply the policy definition per standard", "reference table"),
    ("covenants", "extract covenant terms from the agreement", "small model, checked by code"),
    ("covenants", "officer confirms the terms once per facility", "person"),
    ("covenants", "test each covenant against its threshold", "code"),
    ("covenants", "compute headroom", "code"),
    ("risk factors", "retrieve policy and prior memos", "code"),
    ("risk factors", "summarize relationship manager notes", "model drafts, cited"),
    ("narrative", "draft the financial analysis prose", "model drafts, cited"),
    ("narrative", "draft the borrower overview", "model drafts, cited"),
    ("narrative", "check every number against lineage", "code"),
    ("narrative", "check every amount carries a currency", "code"),
    ("recommendation", "write the recommendation", "person"),
)

# 50.3 deterministic first: Northgate Fabrication Ltd, fiscal 2025, ASPE, C$ thousands (synthetic)
BORROWER = "Northgate Fabrication Ltd"
STATEMENT = dict(standard="ASPE", currency="C$", unit="thousands", uri="hl-docs://pkg-0412/fs-2025.pdf",
                 sha256="6f1e0c2a9b", fields={
                     "revenue": (48200, 3), "ebitda": (6140, 4), "maintenance_capex": (1050, 6), "cash_taxes": (620, 4),
                     "interest": (1380, 4), "scheduled_principal": (2150, 9), "funded_debt": (19650, 9),
                     "current_assets": (14900, 2), "current_liabilities": (9800, 2), "total_assets": (42850, 2),
                     "total_liabilities": (29450, 2), "equity": (13400, 2), "intangibles": (2300, 2)})
RATIO_DEFS = {  # Harbourline credit policy definitions (stand-in), one row per ratio
    "dscr": "(EBITDA - maintenance capex - cash taxes) / (interest + scheduled principal)",
    "debt_to_ebitda": "funded debt / EBITDA",
    "current_ratio": "current assets / current liabilities",
    "tnw": "equity - intangibles (C$ thousands)"}
INPUTS = {"dscr": ("ebitda", "maintenance_capex", "cash_taxes", "interest", "scheduled_principal"),
          "debt_to_ebitda": ("funded_debt", "ebitda"), "current_ratio": ("current_assets", "current_liabilities"),
          "tnw": ("equity", "intangibles")}
COVENANTS = {"dscr": (">=", 1.25), "debt_to_ebitda": ("<=", 3.50), "current_ratio": (">=", 1.20), "tnw": (">=", 10000)}
IFRS_LEASE_RULE = "IFRS 16 borrowers: lease payments deducted from EBITDA before DSCR (policy normalization)"
FX = {"USD/CAD": 1.3640, "as_of": "engagement day 118", "owner": "Harbourline treasury"}

# 50.7 classification: Harbourline's components (stand-in)
C = M.Component
COMPONENTS = [
    C("H01", "package intake from the document store", "code", False, False, False),
    C("H02", "format detection and text capture", "code", False, False, False),
    C("H03", "statement table capture", "vendor layout model, prompted", True, False, True, True, ("numbers reach the spread",)),
    C("H04", "chart-of-accounts mapping table", "reference table", False, False, False),
    C("H05", "unseen-label mapping suggestion", "vendor model, prompted", True, False, True, True, ("numbers reach the spread",)),
    C("H06", "cross-footing and quarantine", "code", False, False, False),
    C("H07", "ratio and covenant calculation", "code", False, False, False),
    C("H08", "covenant term extraction", "vendor model, prompted", True, False, True, True, ("thresholds reach the test",)),
    C("H09", "policy and prior-memo retrieval", "vendor embedding model", True, False, False, True),
    C("H10", "risk-factor summary", "vendor model, prompted", True, False, True, True, ("text reaches the memo",)),
    C("H11", "memo narrative drafting", "vendor model, prompted", True, False, True, True, ("text reaches the memo",)),
    C("H12", "development judge (offline)", "vendor model, prompted", True, False, False, True),
    C("H13", "numeric gate and lineage check", "code", False, False, False),
    C("H14", "suite add-in surface", "code", False, False, False),
]
R = M.Rule
NORTHLIGHT_READING = M.Framework("northlight-proposal", (
    R({"quantitative": False}, M.NOT_MODEL, "not a model"),
    R({"vendor_model": True}, M.REGISTERED, "vendor model, not trained on bank data"),
    R({}, M.FULL, "a model the vendor built")), "the reading in Northlight's day 22 draft")
HARBOURLINE_READING = M.Framework("harbourline-e23-reading", (
    R({"quantitative": False}, M.NOT_MODEL, "not a model"),
    R({"core_decision": True}, M.FULL, "a model in a material use, vendor or not: risk-rated, validated before use"),
    R({}, M.REGISTERED, "a model in a supporting use: inventoried, low risk rating")),
    "a stand-in reading of a bank policy written to OSFI E-23 [VERIFY]; not Harbourline's text")


def tier(c, cls):
    """Harbourline's risk rating inside full scope (stand-in): high when a number reaches the credit file."""
    if cls.outcome != M.FULL:
        return ""
    return "high" if any("numbers" in d or "thresholds" in d for d in c.design_choices) else "medium"


# calendar (Harbourline engagement days)
DAYS = dict(classification_agreed=40, sample_raised=45, architecture=61, build_complete=112, submission_1=118,
            returned=126, shadow=(120, 149), shadow_exit=150, submission_2=152, model_risk=158, live=171)
