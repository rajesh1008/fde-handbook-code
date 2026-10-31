"""De-identification that is tested against re-identification (Chapter 16, fieldkit v2.1).

Pattern scrubbing alone leaks: it misses identifiers that OCR has bent, names inside narratives, and first-name
sign-offs. This module adds a known-value scan (the structured values the customer already holds for each file,
matched against the text with OCR look-alikes folded), k-anonymity over quasi-identifiers, and a linkage attack
against a public table. A release is acceptable only when the leak scan is clean, the smallest group is at least
k, and the linkage attack re-identifies no record uniquely. Legal sufficiency is the privacy office's call.
"""
from __future__ import annotations

import hashlib
import re
from collections import Counter, defaultdict
from dataclasses import dataclass

# OCR look-alike classes, folded to one representative after lower-casing
LOOKALIKE = str.maketrans({"0": "a", "o": "a", "1": "l", "i": "l", "|": "l", "5": "s", "8": "b", "6": "b",
                           "2": "z", "c": "e", "h": "n"})

PATTERNS = [
    ("POLICY", r"\bHP\d{6}\b"),
    ("REPORT", r"\b[A-Z]{2,4}-\d{2}-\d{6}\b"),
    ("CLAIM", r"\bCM-\d{10}\b"),
    ("PHONE", r"\b\d{3}[ .-]\d{3}[ .-]\d{4}\b"),
    ("EMAIL", r"\b[\w.]+@[\w.]+\b"),
    ("DATE", r"\b\d{1,2}/\d{1,2}/\d{2,4}\b"),
    ("ADDRESS", r"\b\d{1,5} [A-Z][a-z]+(?: [A-Z][a-z]+)? (?:St|Ave|Rd|Dr|Ln|Way|Tpke)\b"),
    ("NAME", r"(?:(?<=CLAIMANT: )|(?<=CUSTOMER: )|(?<=PATIENT: )|(?<=OPERATOR \d: ))[A-Z][a-z]+ [A-Z][a-z]+"),
    ("NAME", r"(?<=From: )[A-Z][a-z]+ [A-Z][a-z]+"),
    ("NAME", r"(?<=Sincerely,\n)[A-Z][a-z]+ [A-Z][a-z]+"),
]


def scrub_patterns(text):
    """The first attempt every team writes: regular expressions for the identifiers it can think of."""
    for tag, pat in PATTERNS:
        text = re.sub(pat, f"[{tag}]", text)
    return text


def fold(s):
    return re.sub(r"[^a-z0-9]", "", s.lower().translate(LOOKALIKE))


def _close(a, b):
    """Edit distance of at most one, for strings of six or more characters."""
    if a == b:
        return True
    if len(a) < 6 or abs(len(a) - len(b)) > 1:
        return False
    if len(a) == len(b):
        return sum(x != y for x, y in zip(a, b)) <= 1
    if len(a) > len(b):
        a, b = b, a
    return any(b[:i] + b[i + 1:] == a for i in range(len(b)))


def _targets(values, min_len=4):
    out = []
    for label, v in values.items():
        if not v:
            continue
        out.append((label, v, [fold(w) for w in v.split()]))
        if label.endswith("name"):
            out += [(label, p, [fold(p)]) for p in v.split() if len(fold(p)) >= min_len]
    return out


def _spans(text):
    return [(m.start(), m.end(), fold(m.group(0))) for m in re.finditer(r"[A-Za-z0-9|]+", text)]


def _find(text, values):
    toks = _spans(text)
    found = []
    for label, v, parts in _targets(values):
        w = len(parts)
        for i in range(len(toks) - w + 1):
            window = [t[2] for t in toks[i:i + w]]
            if all(_close(a, b) for a, b in zip(window, parts)):
                found.append((label, v, toks[i][0], toks[i + w - 1][1]))
    return found


def known_value_scan(text, values):
    """Find any known identifier (or a name part) in the text, tolerant of OCR look-alikes and one-character slips."""
    hits, seen = [], set()
    for label, v, _a, _b in _find(text, values):
        if (label, v) not in seen:
            seen.add((label, v))
            hits.append((label, v))
    return hits


def scrub_known(text, values):
    """Replace every span that matches a known value or a name part."""
    spans = sorted({(a, b, label.upper()) for label, _v, a, b in _find(text, values)}, reverse=True)
    last = len(text) + 1
    for a, b, label in spans:
        if b <= last:
            text = text[:a] + f"[{label}]" + text[b:]
            last = a
    return text


def k_anonymity(records, quasi):
    """Group sizes over the quasi-identifier columns. Returns (smallest group, Counter of group sizes)."""
    groups = Counter(tuple(r.get(q) for q in quasi) for r in records)
    sizes = Counter(groups.values())
    return (min(groups.values()) if groups else 0), sizes


def linkage_attack(released, public, keys):
    """Join released rows to a public table on shared keys; a released row matching exactly one public row is
    re-identified. Returns the list of (released index, public identity)."""
    index = defaultdict(list)
    for p in public:
        index[tuple(p.get(k) for k in keys)].append(p)
    hits = []
    for i, r in enumerate(released):
        m = index.get(tuple(r.get(k) for k in keys), [])
        if len(m) == 1:
            hits.append((i, m[0].get("identity")))
    return hits


def shift_days(key, secret, span=30):
    """A per-claim date shift that is stable for the claim (so intervals survive) and unknown without the secret."""
    h = int(hashlib.sha256(f"{secret}:{key}".encode()).hexdigest(), 16)
    return (h % (2 * span + 1)) - span


@dataclass
class ReleaseCheck:
    leaks: int
    documents: int
    min_group: int
    k: int
    linked: int

    @property
    def passed(self):
        return self.leaks == 0 and self.min_group >= self.k and self.linked == 0

    def render(self):
        return (f"  known-value leaks {self.leaks} of {self.documents} documents   smallest group {self.min_group} "
                f"(k={self.k})   linkage re-identifications {self.linked}   "
                f"{'PASS' if self.passed else 'FAIL'}")
