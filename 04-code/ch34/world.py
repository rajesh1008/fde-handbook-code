"""Chapter 34 world: the contracts the forward deployed engineer reads.

Clause text is fictional, written for this lab. Amounts follow Chapter 2 (illustrative, labeled): Caldwell
subscription $1.6M a year from signature and a fixed deployment fee of $200,000; Greystone time and materials at
$260 an hour with a $450,000 not-to-exceed cap and a subscription that starts at production acceptance; Pennant a
fixed $120,000. Loaded rate $150 per FDE hour. Measurements quote earlier chapters where they exist; anything else
is a deterministic stand-in and says so.
"""
import _paths  # noqa: F401
from fieldkit.contract import Clause, Dependency, Decision, CostLine

LOADED_RATE = 150
BILL_RATE = 260
FEE_MONTH = 1_600_000 / 12          # Caldwell monthly subscription
CREDIT_MONTHS = 7                   # calendar months after go-live (day 158) inside year one
DAYS_PER_MONTH = 365 / 12
LIVE_DAY = 158

V3 = "caldwell AI production addendum v3 (agreed in principle, day 136)"
V5 = "caldwell AI production addendum v5 (signed, day 149)"

CALDWELL_V3 = [
    Clause("CA-01", "Northlight warrants that the System will be 98% accurate, as determined by Caldwell. For each "
                    "calendar month in which the System is not 98% accurate, Northlight shall credit 50% of the "
                    "monthly subscription fee.", V3),
    Clause("CA-02", "Northlight shall make the System available 99.9% of the time, measured at the adjuster console, "
                    "in each calendar month. For each calendar month below 99.9%, Northlight shall credit 10% of the "
                    "monthly subscription fee.", V3),
    Clause("CA-03", "Northlight shall respond to any Severity 1 incident within one hour, 24 hours a day, seven days "
                    "a week.", V3),
    Clause("CA-04", "Northlight shall provide two engineers on site at Caldwell for 90 days after the go-live date.", V3),
    Clause("CA-05", "Northlight shall deliver a monthly monitoring report on the System's accuracy and drift.", V3),
    Clause("CA-06", "Northlight shall keep the underlying model version unchanged for twelve months after go-live, "
                    "and shall not change it without 90 days' written notice and Caldwell's written approval.", V3),
    Clause("CA-07", "Northlight shall permit Caldwell and any regulator of Caldwell to audit the System, including "
                    "Northlight's evaluation suite and logs, on ten business days' notice.", V3),
    Clause("CA-08", "Northlight shall provide transition assistance for six months after termination at no "
                    "charge.", V3),
    Clause("CA-09", "Northlight shall indemnify Caldwell for all losses arising from the System's outputs, without "
                    "limit.", V3),
    Clause("CA-10", "Northlight shall delete all Caldwell data, including copies held by any model provider, within "
                    "30 days of termination and certify the deletion.", V3),
    Clause("CA-11", "Northlight shall train all adjusters and supervisors in the use of the System and deliver "
                    "operating runbooks, within the fixed deployment fee.", V3),
    Clause("CA-12", "Northlight shall transfer knowledge to Caldwell's support desk before the go-live date.", V3),
    Clause("CA-13", "Caldwell shall pay undisputed invoices within 60 days.", V3),
    Clause("CA-14", "This Addendum is governed by the law named in the Master Agreement.", V3),
    Clause("CA-15", "Northlight shall process Caldwell data only in Caldwell's AWS account in us-east-1, except for "
                    "model calls made through Caldwell's model gateway.", V3),
]

CALDWELL_V5 = [
    Clause("CA-01", "Northlight warrants that the post-review document error, scored by Caldwell's claims quality team "
                    "on a stratified sample of 310 documents each calendar month under the gold-set rubric, will not "
                    "reach 2.26%. For each calendar month in breach, Northlight shall credit 5% of the monthly "
                    "subscription fee, capped at 15% of annual fees.", V5),
    Clause("CA-02", "Northlight shall make the System available 99.5% of the time, measured at the vendor service "
                    "boundary, in each calendar month, excluding outages of Caldwell's model gateway and scheduled key "
                    "rotations. For each calendar month below 99.5%, Northlight shall credit 5% of the monthly "
                    "subscription fee.", V5),
    Clause("CA-03", "Northlight shall respond to any Severity 1 incident within one hour between 07:00 and 19:00 "
                    "Eastern on business days, and within four hours otherwise.", V5),
    Clause("CA-04", "Northlight shall provide one engineer on site at Caldwell for 30 days after the go-live date; "
                    "further on-site support is available at the time and materials rate.", V5),
    Clause("CA-05", "Northlight shall deliver the data feed and runbook Caldwell needs to produce its own monitoring "
                    "report.", V5),
    Clause("CA-06", "Northlight shall give Caldwell written notice of any change to the model version within two "
                    "business days of the provider's announcement; Northlight shall revalidate the System under the "
                    "model-risk validation plan before the change takes effect.", V5),
    Clause("CA-07", "Northlight shall permit Caldwell and any regulator of Caldwell to audit the System, including the "
                    "evaluation suite and run records Caldwell holds, once a year on twenty business days' notice and "
                    "at any time a regulator requires.", V5),
    Clause("CA-08", "Northlight shall provide transition assistance for three months after termination at the time "
                    "and materials rate.", V5),
    Clause("CA-09", "Northlight shall indemnify Caldwell for losses arising from the System's outputs, capped at the "
                    "fees paid in the prior twelve months, except that losses from a breach of data protection are "
                    "capped at twice that amount; decisions taken by Caldwell staff on drafts the System produced are "
                    "Caldwell's.", V5),
    Clause("CA-10", "Northlight shall delete all Caldwell data that Northlight holds within 30 days of termination and "
                    "certify the deletion; copies held by the provider are governed by the provider terms in "
                    "Exhibit D.", V5),
    Clause("CA-11", "Northlight shall train Caldwell's three claims supervisors as trainers and deliver operating "
                    "runbooks.", V5),
    Clause("CA-12", "Northlight shall transfer knowledge to Caldwell's support desk before the go-live date.", V5),
    Clause("CA-13", "Caldwell shall pay undisputed invoices within 60 days.", V5),
    Clause("CA-14", "This Addendum is governed by the law named in the Master Agreement.", V5),
    Clause("CA-15", "Northlight shall process Caldwell data only in Caldwell's AWS account in us-east-1, except for "
                    "model calls made through Caldwell's model gateway.", V5),
]

CALDWELL_DEPS = [
    Dependency("adjuster console", "Caldwell",
               "console availability includes Caldwell's model gateway, whose key rotates every seven days"),
    Dependency("underlying model", "the model provider", "the provider retires dated model versions"),
    Dependency("model provider", "the model provider", "provider copies sit under the provider's own retention terms"),
]
CALDWELL_DECISIONS = [
    Decision("R2", "deliver a monthly monitoring report",
             "Caldwell produces the monthly monitoring report itself (review condition R2, Ch33)"),
    Decision("GW-90", "unchanged for twelve months",
             "Caldwell's own gateway pins a dated model version for at most 90 days (Ch18)"),
]

# One accuracy clause, four readings that already exist in the engagement record (percent accurate).
READINGS = [
    ("post-review document error, 4,000 documents", 99.1, "Ch27: 36 errors in 4,000 after review"),
    ("field accuracy on the gold set", 88.2, "Ch27: Anne Kessler's gold set, router v0"),
    ("shadow agreement with adjusters", 88.0, "Ch31: shadow agreement"),
    ("pilot accuracy scored by Anne Kessler", 84.0, "Ch31: pilot"),
]
AVAILABILITY = {"adjuster console": 99.71, "vendor service boundary": 99.93}   # stand-in, days 106 to 135

# Cost lines per commitment (year one). Service-level credits are computed, not listed.
V3_COSTS = {
    "CA-03.1": CostLine("CA-03.1", "24x7 one-hour Severity 1 rota, four engineers, 7 months", 96_000, "estimated"),
    "CA-04.1": CostLine("CA-04.1", "two engineers on site for 90 days (840 h)", 840 * LOADED_RATE, "estimated"),
    "CA-05.1": CostLine("CA-05.1", "monthly monitoring report, 24 h a month for 7 months", 168 * LOADED_RATE,
                        "estimated"),
    "CA-06.1": CostLine("CA-06.1", "forced migration, revalidation and dual running inside the freeze", 94_500, "assumed"),
    "CA-07.1": CostLine("CA-07.1", "two audits with ten days' notice (120 h)", 120 * LOADED_RATE, "estimated"),
    "CA-08.1": CostLine("CA-08.1", "six months of free transition assistance, provision", 40_000, "assumed"),
    "CA-09.1": CostLine("CA-09.1", "uncapped indemnity: liability cover for year one", 120_000, "assumed"),
    "CA-10.1": CostLine("CA-10.1", "deletion including provider copies, attestations (180 h)", 180 * LOADED_RATE,
                        "estimated"),
    "CA-11.1": CostLine("CA-11.1", "train 14 adjusters and supervisors, runbooks (160 h)", 160 * LOADED_RATE,
                        "estimated"),
    "CA-12.1": CostLine("CA-12.1", "knowledge transfer to the support desk (216 h)", 216 * LOADED_RATE, "estimated"),
    "CA-15.1": CostLine("CA-15.1", "in-account processing: already the design (Ch17)", 0, "measured"),
}
V5_COSTS = {
    "CA-03.1": CostLine("CA-03.1", "business-hours one-hour rota, four hours otherwise", 21_000, "estimated"),
    "CA-04.1": CostLine("CA-04.1", "one engineer on site for 30 days (140 h)", 140 * LOADED_RATE, "estimated"),
    "CA-05.1": CostLine("CA-05.1", "data feed and runbook for Caldwell's own report (40 h)", 40 * LOADED_RATE,
                        "estimated"),
    "CA-06.1": CostLine("CA-06.1", "notice within two days of the provider's announcement", 0, "estimated"),
    "CA-06.2": CostLine("CA-06.2", "revalidation under the Ch33 plan before a change", 30_000, "estimated"),
    "CA-07.1": CostLine("CA-07.1", "one audit a year plus regulator requests (120 h)", 120 * LOADED_RATE, "estimated"),
    "CA-08.1": CostLine("CA-08.1", "transition assistance billed at the T&M rate", 0, "estimated"),
    "CA-09.1": CostLine("CA-09.1", "capped indemnity: increment over standard cover", 15_000, "assumed"),
    "CA-10.1": CostLine("CA-10.1", "deletion of Northlight-held data, certificate (80 h)", 80 * LOADED_RATE,
                        "estimated"),
    "CA-11.1": CostLine("CA-11.1", "train three supervisors as trainers (53 h)", 8_000, "estimated"),
    "CA-12.1": CostLine("CA-12.1", "knowledge transfer to the support desk, scoped (67 h)", 10_000, "estimated"),
    "CA-15.1": CostLine("CA-15.1", "in-account processing: already the design (Ch17)", 0, "measured"),
}

# Caldwell year one before the addendum, as of day 136 (hours ledger to day 136; forecast to go-live).
HOURS_TO_DAY_136 = 2_750
HOURS_DAY_136_TO_LIVE = 400
SUSTAIN_FTE = 0.5
HOURS_PER_FTE_MONTH = 140
RENEWAL = 0.80                      # Ch2 renewal band for Caldwell, forecast

# ---- Greystone: Marcus Bell's clauses ------------------------------------------------------------------------
G108 = "greystone amendment 1, procurement redline (Marcus Bell, day 108)"
G127 = "greystone amendment 1, signed (day 127)"
GREYSTONE_108 = [
    Clause("GA-01", "Greystone will accept the System in production when it performs to Greystone's satisfaction.", G108),
    Clause("GA-02", "Northlight shall ensure that every subcontractor that receives protected health information, "
                    "including any model provider, signs a business associate agreement no less protective than "
                    "this Agreement.", G108),
    Clause("GA-03", "Northlight shall indemnify Greystone for any harm to a patient arising from the System, including "
                    "any submission to a payer or contact with a patient.", G108),
    Clause("GA-04", "Northlight shall remediate all security findings within the not-to-exceed amount.", G108),
    Clause("GA-05", "Northlight shall notify Greystone of any suspected security incident within 24 hours of "
                    "discovery.", G108),
    Clause("GA-06", "Northlight shall ensure that no model provider retains prompts or outputs containing protected "
                    "health information.", G108),
    Clause("GA-07", "Greystone shall pay invoices for time and materials monthly.", G108),
]
GREYSTONE_127 = [
    Clause("GA-01", "Greystone will accept the System when it meets the acceptance criteria in Exhibit A, or ten "
                    "business days after Northlight certifies that it does unless Greystone gives written notice of "
                    "a failed criterion.", G127),
    Clause("GA-01A", "Northlight warrants that the share of drafts needing material correction, counted per referral, "
                     "scored by Greystone's clinical reviewers on a sample of 110 referrals in the acceptance window, "
                     "will not reach 21.8%. If it does, Greystone may withhold acceptance and Northlight shall re-test "
                     "within 15 business days at its own cost.", G127),
    Clause("GA-02", "Northlight shall flow down business associate terms to every subcontractor that receives "
                    "protected health information; the provider's retention terms are those confirmed under finding "
                    "F-10 and set out in Exhibit C.", G127),
    Clause("GA-03", "Northlight shall indemnify Greystone for losses arising from drafts the System produces, capped "
                    "at the fees paid in the prior twelve months; the System does not submit to payers, set urgency "
                    "or contact patients, and clinical decisions on drafts are Greystone's.", G127),
    Clause("GA-04", "Northlight shall remediate the twelve findings of the day-104 security review at the time and "
                    "materials rate inside the not-to-exceed amount, and shall raise a change order before the cap is "
                    "reached.", G127),
    Clause("GA-05", "Northlight shall notify Greystone of any confirmed security incident within 24 hours of "
                    "confirmation, and of a suspected incident within 72 hours of discovery.", G127),
    Clause("GA-06", "Northlight shall configure every model call under the provider terms confirmed in finding F-10 "
                    "and shall report any change to those terms within five business days.", G127),
    Clause("GA-07", "Greystone shall pay invoices for time and materials monthly.", G127),
]
GREYSTONE_DEPS = [Dependency("model provider", "the model provider",
                             "abuse-monitoring retention of prompts is the provider's (finding F-10, owner Marcus Bell)")]
GREYSTONE_DECISIONS = [
    Decision("REL-1", "submission to a payer",
             "release boundary: the system drafts only; submit to a payer is refused (Ch25)", "AUTHORITY"),
    Decision("TM-1", "within the not-to-exceed",
             "time and materials with a $450,000 cap (Ch2): open-ended remediation inside the cap is a fixed price"),
]

# ---- Pennant data-processing terms ---------------------------------------------------------------------------
PENNANT = [
    Clause("PA-01", "Northlight shall process personal data of EU shipments only in the europe-west4 region."),
    Clause("PA-02", "Northlight shall not access personal data from outside the European Economic Area."),
    Clause("PA-03", "Northlight warrants that at least 80% of shipments will be matched each calendar month."),
    Clause("PA-04", "Pennant shall provide carrier invoices within five business days of receipt."),
]
PENNANT_DECISIONS = [Decision("SUP-1", "from outside the european economic area",
                              "Northlight's on-call engineers sit outside the EEA; access needs a transfer mechanism "
                              "in the data-processing agreement [VERIFY]")]

# ---- Harbourline: Schedule A is the bid response (Ch12) -------------------------------------------------------
HARBOURLINE_SCHEDULE_A = [
    Clause("HA-01", "Northlight will deliver every credit memo with a citation for each figure."),
    Clause("HA-02", "Northlight will keep all bank data in Canada."),
    Clause("HA-03", "Northlight will send log events to the bank's security operations center in its SIEM format."),
    Clause("HA-04", "Northlight will reach 90% agreement rate with the bank's credit reviewers."),
    Clause("HA-05", "Northlight will substitute a model within 30 days if the provider withdraws one."),
    Clause("HA-06", "Northlight will notify the bank of any material model change within five business days."),
    Clause("HA-07", "Our platform is trusted by leading financial institutions."),
]
HARBOURLINE_DEPS = [Dependency("provider withdraws", "the model provider", "the provider's withdrawal schedule")]
