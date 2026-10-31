"""Failure injection: draft v0.9 states a gateway capability as a direct customer fact. CL-17 contradicts it."""
import _path  # noqa: F401
from fieldkit.bid import extract, lint
from harbourline import RESPONSE_V09, RESPONSE_V10, clarifications

for name, resp in (("v0.9 (week 5)", RESPONSE_V09), ("v1.0 (submitted, week 6)", RESPONSE_V10)):
    claims = extract(resp)
    issues = lint(claims, clarifications())
    errs = [i for i in issues if i[1] == "ERROR"]
    print(f"response {name}: {len(claims)} claims, {len(errs)} errors, {len(issues) - len(errs)} warnings")
    for k, lvl, code, msg in issues:
        if name.startswith("v1.0") and lvl == "WARN":
            continue
        c = next(c for c in claims if c.key == k)
        print(f"  {lvl} {k} {c.answer} [{c.status}] {code}")
        print(f"       \"{c.text}\"")
        print(f"       {msg}")
    print("  submission " + ("BLOCKED" if errs else "allowed (warnings need a written reason)"))
