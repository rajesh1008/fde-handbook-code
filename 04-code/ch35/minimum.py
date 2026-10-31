"""Chapter 35: minimum necessary at Greystone. Fields the drafting service read against the fields the task needs."""
import hashlib

import _paths  # noqa: F401
from fieldkit.privacy import minimum_necessary
from world import NEEDED_FIELDS, PACKET_FIELDS, referrals


def draft(packet, allow):
    view = {k: packet.get(k, "") for k in sorted(allow) if k in NEEDED_FIELDS}
    return hashlib.sha256(repr(view).encode()).hexdigest()


refs = referrals()
for label, read in (("v1 (whole packet)", PACKET_FIELDS), ("v2 (allowlist)", NEEDED_FIELDS)):
    extra, share = minimum_necessary(read, NEEDED_FIELDS)
    print(f"{label:<18} fields read {len(read):>2}   needed {len(NEEDED_FIELDS)}   beyond need {len(extra):>2} ({share:.0%})")
    if extra:
        print("   beyond need:", ", ".join(extra))
same = sum(draft(r, PACKET_FIELDS) == draft(r, NEEDED_FIELDS) for r in refs)
print(f"drafts identical between v1 and v2 inputs: {same} of {len(refs)} sandbox-week referrals")
