"""The catalog: fifteen patterns that held and the fifteen anti-patterns they prevent, one pair per rule.

Each anti-pattern carries the story that exposed it (chapter and day) so the linter can print where the
rule came from. Nothing here is a measurement; it is the index the linter and the chapter share.
"""
from dataclasses import dataclass


@dataclass(frozen=True)
class Pair:
    rule: str          # R01..R15, the linter rule id
    pattern: str       # what held
    anti: str          # what it prevents
    exposed: str       # the story that exposed the anti-pattern
    chapters: str      # where the pattern is built


CATALOG = [
    Pair("R01", "An exit rule signed before the pilot starts", "The endless pilot",
         "15 of 38 Northlight customers never reached production; Greystone's last vendor pilot ran nine months", "2, 39"),
    Pair("R02", "A sponsor map with an observed operator and spread roles", "The sponsor-only engagement",
         "Pennant day 28: Jenna Ruiz held 4 of 5 roles; readiness 0.40, 0.30 without her", "11, 41"),
    Pair("R03", "Customer-owned alert routes after hand-over", "The vendor-owned alert",
         "Caldwell day 176: A-07 paged Northlight during the hand-over drill", "41, 42"),
    Pair("R04", "Commitments with a measurer, a document set, a computation and an interval", "The accuracy promise",
         "Caldwell CA-01 '98% accurate, as determined by Caldwell'; margin 17.9% read naively, -8.0% read honestly", "4, 34"),
    Pair("R05", "Deterministic first, model last", "The agent that did arithmetic",
         "Harbourline loan-to-value from three documents given whole to a model (Chapter 9 injection)", "9, 50"),
    Pair("R06", "A status on every claim, raised only by an evidence event", "The proposal that became a fact",
         "Caldwell: one sentence rose from vendor position (day -34) to customer fact (day 24) with no evidence", "8, 12"),
    Pair("R07", "Gates judged per slice, never on the aggregate alone", "The aggregate that passed",
         "Caldwell day 156: 84.0% aggregate passed while fax first notices sat at 74.4%", "29, 37"),
    Pair("R08", "The customer's expert scores on the customer's documents", "The vendor-scored accuracy",
         "Caldwell: 91% on Northlight's suite, 68% on Anne Kessler's gold set", "3, 26"),
    Pair("R09", "A gateway adapter that rereads its key", "The key read once",
         "Caldwell: the v0 client read its key at start-up against a weekly rotation", "18, 41"),
    Pair("R10", "Thresholds chosen by a named person from a calibration", "The threshold nobody chose",
         "Caldwell router v0: 0.98 with no name beside it; proceed-band error 14.8%", "27"),
    Pair("R11", "Pinned model versions with recorded changes", "The floating model alias",
         "Pennant EU project asked for 'latest' and got a different version from the US project", "20, 42"),
    Pair("R12", "A data map generated from the running system", "The drawn data map",
         "Greystone: 5 flows drawn, 14 generated; 187 of 600 provider entries held PHI", "35"),
    Pair("R13", "Runbooks the customer can execute with the vendor hands off", "The runbook only the vendor can run",
         "Pennant exit drill v0 blocked 02:37 at a vendor bastion (day 272)", "41, 43"),
    Pair("R14", "Evidence packs pinned to content", "The evidence that cannot be rebuilt",
         "Caldwell: 0 of 40 early production decisions reconstructable after the day-166 hotfix", "40"),
    Pair("R15", "Playbook steps that declare the estate they need", "The playbook that assumed an API",
         "Pennant P-A2 denied day 23 with no alternative priced; the next insurer's PB-04 needed a document API", "10, 46"),
]
BY_RULE = {p.rule: p for p in CATALOG}
