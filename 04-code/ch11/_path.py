"""Path set-up for the Chapter 11 lab: fieldkit (shared toolkit) and this lab directory."""
import pathlib, sys
_HERE = pathlib.Path(__file__).resolve().parent
for p in (_HERE.parents[0] / "fieldkit", _HERE):
    if str(p) not in sys.path:
        sys.path.append(str(p))
