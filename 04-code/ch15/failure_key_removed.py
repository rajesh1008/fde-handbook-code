"""Chapter 15 failure injection: the same 200-file delivery with the key column removed.

Export tools drop key columns more often than anyone expects: a column filter saved by a previous
user, a de-identification step that treats every identifier as personal data, a spreadsheet that
promotes the key to a row label. The register must refuse the delivery and say what it stops.
"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "fieldkit"))
from fieldkit.fixtures import caldwell_sample, caldwell_register
from fieldkit.histories import caldwell_fields

broken = caldwell_sample(drop_column="claim_id")
print("v1 register (Chapter 3):")
print(caldwell_register().assess("caldwell-claims-sample", broken).summary())
print()
print("v2 register (this chapter):")
res = caldwell_fields().assess("caldwell-claims-sample", broken, extracted_day=41, delivered_day=47)
print(res.summary())
print()
print("blocking:", "; ".join(res.blocking))
