"""Path set-up for the Chapter 9 lab: fieldkit (shared toolkit) and, read only, the Chapter 14 Greystone pipeline."""
import pathlib, sys
_HERE = pathlib.Path(__file__).resolve().parent
for p in (_HERE.parents[0] / "fieldkit", _HERE):
    if str(p) not in sys.path:
        sys.path.append(str(p))
