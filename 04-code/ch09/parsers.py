"""The deterministic services behind C02 and C03: real code, run on the lab's synthetic documents.

Policy numbers at Caldwell (stand-in format for the lab): two letters, seven digits, one check digit (Luhn mod 10
over the seven digits). A received date is read from a stamp or a header, never inferred from the content.
"""
import re
from datetime import date

POLICY_RE = re.compile(r"\b([A-Z]{2})-?(\d{7})-?(\d)\b")
STAMP_RE = re.compile(r"RECEIVED\s+(\d{2})\s+([A-Z]{3})\s+(\d{4})")
MONTHS = {m: i + 1 for i, m in enumerate("JAN FEB MAR APR MAY JUN JUL AUG SEP OCT NOV DEC".split())}


class Unreadable(ValueError):
    """Raised, never guessed: the document goes to the exception queue with this reason."""


def luhn_digit(digits):
    total = 0
    for i, ch in enumerate(reversed(digits)):
        d = int(ch)
        if i % 2 == 0:
            d *= 2
            if d > 9: d -= 9
        total += d
    return (10 - total % 10) % 10


def parse_policy(text):
    found = POLICY_RE.findall(text)
    if not found:
        raise Unreadable("policy number missing")
    good = [f"{a}{b}{c}" for a, b, c in found if luhn_digit(b) == int(c)]
    if not good:
        raise Unreadable("policy number fails check digit")
    if len(set(good)) > 1:
        raise Unreadable("two valid policy numbers")
    return good[0]


def received_date(text):
    m = STAMP_RE.search(text)
    if not m:
        raise Unreadable("no received stamp")
    d, mon, y = m.groups()
    return date(int(y), MONTHS[mon], int(d))
