"""Listing 29.3: layer one on pull request #231 (day 153), a routine bump of the date library from 3.9 to 4.0."""
import json
import common as C
import world as W
from fieldkit.pyramid import select_layers

v, detail, sec, usd, m = C.chk_rules(dict(C.BASE, datelib=4.0))
print(f"PR #231 'bump datelib 3.9 -> 4.0' (dependency); layers selected {select_layers(['requirements.txt'], C.PATH_RULES)[1]}")
print(f"L1 rule regression: {v.upper()}  {detail}")
print(f"   modeled time {sec:.1f} s, cost $0.00")
case = next(c for c in W.rule_cases() if c["family"] == "date normalization" and c["m"] <= 12 and c["d"] <= 12 and c["m"] != c["d"])
print(f"   example case {case['family']} #{case['i']}: '{case['date']}' 3.9 -> {W.parse_date(case['date'], 3.9)}, "
      f"4.0 -> {W.parse_date(case['date'], 4.0)}")
print("by family (failing of total):")
for fam, n in W.FAMILIES.items():
    print(f"  {fam:26} {m['by'].get(fam, 0):>3} of {n}")
print("gate: BLOCK at L1; fix: pin dayfirst=False explicitly in intake/dates.py, re-run L1 -> ",
      C.chk_rules(C.BASE)[0].upper())
json.dump(dict(by=m["by"], fam=W.FAMILIES), open("output/rules.json", "w"), indent=1)
