"""Greystone Health referral pipeline, as walked with two referral coordinators and Michael Hart, days 15 to 17.

Electronic path (EHR referral orders and the outside-provider e-referral portal): 25 steps.
Fax path (outside referrals faxed to clinic fax inboxes and re-keyed), found on day 19: 25 more steps.
Step names are the coordinators' words, shortened. Volumes are the day-16 two-clinic count (stand-in, see README).
"""
from decision_tree import Step

H = "Michael Hart"
OPS = "VP ambulatory operations"
D, R, C = dict(determined=True, written_rules=False, closed_output=False), \
          dict(determined=False, written_rules=True, closed_output=False), \
          dict(determined=False, written_rules=False, closed_output=True)
O = dict(determined=False, written_rules=False, closed_output=False)

ELECTRONIC = [
    Step("E01", "receive referral order from EHR interface queue", **D),
    Step("E02", "parse referral message into fields", **D),
    Step("E03", "match patient on medical record number", **D),
    Step("E04", "flag duplicate referral (same patient, specialty, 30 days)", **D),
    Step("E05", "look up referring provider in directory", **D),
    Step("E06", "map order code to receiving specialty", **D),
    Step("E07", "check insurance eligibility with payer", **D),
    Step("E08", "decide whether prior authorization is required", **R, rule_owner="revenue-cycle lead"),
    Step("E09", "check required attachments against specialty list", **D),
    Step("E10", "request missing attachments (template)", **D),
    Step("E11", "classify reason for referral into intake category", **C, michael="draft only"),
    Step("E12", "extract problems, medications, results from notes", **C, michael="draft only"),
    Step("E13", "apply local clinic routing rules", **R, rule_owner="clinic managers"),
    Step("E14", "carry order priority into the work queue", **D),
    Step("E15", "send red-flag terms to clinician urgency review", **R, rule_owner=H),
    Step("E16", "draft referral summary for receiving clinician", **O, michael="draft only"),
    Step("E17", "draft prior-authorization letter", **O, michael="draft only"),
    Step("E18", "fill payer form fields from structured data", **D),
    Step("E19", "check letter against payer criteria checklist", **R, rule_owner="revenue-cycle lead"),
    Step("E20", "suggest diagnosis codes from notes", **C, michael="draft only"),
    Step("E21", "write referral status to EHR work queue", **D),
    Step("E22", "notify scheduling queue when ready", **D),
    Step("E23", "track prior-authorization status with payer", **D),
    Step("E24", "age the backlog and run service-level timers", **D),
    Step("E25", "write the audit record for the referral", **D),
]

FAX = [
    Step("F01", "receive fax image from clinic fax server", **D),
    Step("F02", "split a multi-referral fax into packets", **C),
    Step("F03", "run optical character recognition on typed pages", **D),
    Step("F04", "read handwritten referral forms", **O, michael="draft only"),
    Step("F05", "classify each page (form, notes, card, labs)", **C),
    Step("F06", "extract patient demographics from the form", **C),
    Step("F07", "match patient without a record number", **R, rule_owner="health-information management"),
    Step("F08", "register a new patient when no match", **R, rule_owner="patient access"),
    Step("F09", "identify the referring provider from letterhead", **C),
    Step("F10", "look up provider in directory", **D),
    Step("F11", "infer receiving specialty from free-text request", **C, michael="draft only"),
    Step("F12", "flag duplicates against the electronic path", **R, rule_owner="clinic managers"),
    Step("F13", "read insurance details from a scanned card", **C),
    Step("F14", "check insurance eligibility with payer", **D),
    Step("F15", "decide whether prior authorization is required", **R, rule_owner="revenue-cycle lead"),
    Step("F16", "check required attachments against specialty list", **D),
    Step("F17", "fax back a request for missing documents", **D),
    Step("F18", "classify reason for referral into intake category", **C, michael="draft only"),
    Step("F19", "extract problems, medications, results from scans", **O, michael="draft only"),
    Step("F20", "apply local clinic routing rules", **R, rule_owner="clinic managers"),
    Step("F21", "send red-flag terms to clinician urgency review", **R, rule_owner=H),
    Step("F22", "draft referral summary for receiving clinician", **O, michael="draft only"),
    Step("F23", "draft prior-authorization letter", **O, michael="draft only"),
    Step("F24", "create the referral order in the EHR", **D),
    Step("F25", "write the audit record for the referral", **D),
]

# Things Michael Hart refused on day 17, recorded as steps that do not exist in the pipeline.
REFUSED = [
    ("submit prior-authorization request to payer without a coordinator", "a person submits; the system drafts"),
    ("set clinical urgency or decline a referral", "clinicians decide acuity; the system routes red flags to them"),
    ("send any message to a patient", "out of scope for release 1"),
]

# Day-16 count at two clinics, Monday to Thursday (coordinators' tally sheets; stand-in volumes, see README).
VOLUME = dict(electronic=412, fax=253)
