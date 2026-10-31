"""Path set-up for the Chapter 12 lab: fieldkit (the shared toolkit) on sys.path."""
import pathlib, sys
_HERE = pathlib.Path(__file__).resolve().parent
for p in (_HERE.parents[0] / "fieldkit", _HERE):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))
