"""Chapter 15: the field-level register entry, reviewed before the sample exists, then run on the delivery."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "fieldkit"))
from fieldkit.fixtures import caldwell_sample
from fieldkit.histories import caldwell_fields

reg = caldwell_fields()
print(reg.card("caldwell-claims-sample"))
print()
# extracted by Caldwell's claims operations team on day 41, delivered on day 47
print(reg.assess("caldwell-claims-sample", caldwell_sample(), extracted_day=41, delivered_day=47).summary())
