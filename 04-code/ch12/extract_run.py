"""Extract the commitments and estate claims from Northlight's submitted response (v1.0) and lint them."""
import _path  # noqa: F401
from fieldkit.bid import extract, lint, strip, LAYER
from harbourline import RESPONSE_V10, clarifications

claims = extract(RESPONSE_V10)
issues = lint(claims, clarifications())
print(f"fieldkit.bid {LAYER}: response v1.0, {len(RESPONSE_V10)} answers, {len(claims)} claims")
for s in "FRVPD":
    print(f"  {s} {sum(c.status == s for c in claims):>2}")
print(f"  estate claims {sum(c.kind == 'estate' for c in claims)}, every one F or R: "
      f"{all(c.status in 'FR' for c in claims if c.kind == 'estate')}")
print("strip by answer:")
for a in RESPONSE_V10:
    print(f"  {a}  {strip([c for c in claims if c.answer == a])}")
errors = [i for i in issues if i[1] == "ERROR"]
print(f"errors {len(errors)}, warnings {len(issues) - len(errors)}")
for k, lvl, code, msg in issues:
    c = next(c for c in claims if c.key == k)
    print(f"  {lvl} {k} {c.answer} {code}: {msg}")
    print(f"       \"{c.text}\"")
