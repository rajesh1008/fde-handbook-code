"""Generate the one page taken into the oral defense."""
import _path  # noqa: F401
from fieldkit.bid import extract, safety_net
from harbourline import RESPONSE_V10, standards, NOT_PROMISED, BOUNDARY

page = safety_net("Harbourline", extract(RESPONSE_V10), standards(), NOT_PROMISED, BOUNDARY)
print("\n".join(page))
print(f"--- {len(page)} lines of a 60-line page")
