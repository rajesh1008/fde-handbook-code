"""Listing 16.2 (failure injection): a document set with no exceptions, and the collapse when real ones arrive.

The same extractor stand-in, unchanged since day 44, meets the 200-file sample (stand-in for the files Anne
Kessler's adjusters keyed on days 48 to 51)."""
import _paths  # noqa: F401
from claimsgen import generate, V1, FIELDS
from standin_sample import sample
from extract_standin import extract
from score import score, norm
from runs import SYN_SEED, SYN_N

syn = generate(V1, SYN_N, SYN_SEED)
real = sample()
s_syn = score(syn, [extract(d, "v1") for d in syn])
outs = [extract(d, "v1") for d in real]
s_real = score(real, outs)
print(f"synthetic v1   {s_syn['accuracy']:.1%}  ({s_syn['correct']:,} of {s_syn['fields']:,} fields, self-scored, 600 documents)")
print(f"real sample    {s_real['accuracy']:.1%}  ({s_real['correct']:,} of {s_real['fields']:,} fields, keyed by Kessler's adjusters, 200 documents)")
print(f"gap            {(s_syn['accuracy'] - s_real['accuracy']) * 100:.1f} points")
print("field               synthetic   real")
for f in FIELDS:
    a, b = s_syn["per_field"][f]
    c, d = s_real["per_field"][f]
    print(f"  {f:<18} {a / b:7.0%}  {c / d:6.0%}")
print("exception tag on the real 200    documents  field accuracy")
for t, (a, b) in sorted(s_real["per_tag"].items(), key=lambda kv: kv[1][0] / kv[1][1]):
    print(f"  {t:<30} {b // len(FIELDS):5d}      {a / b:5.0%}")
print("three wrong answers, as the reviewer saw them")
shown = set()
for d, o in zip(real, outs):
    for tag, f in (("agent sender", "claimant_name"), ("forwarded chain", "date_received"), ("faded scan", "policy_number")):
        if tag in d["tags"] and tag not in shown and norm(o[f]) != norm(d["gold"][f]):
            print(f"  {d['id']} [{tag}] {f}: extracted {o[f]!r}, adjuster keyed {d['gold'][f]!r}")
            shown.add(tag)
