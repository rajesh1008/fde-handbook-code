"""Put fieldkit and the Chapter 21 door (pennant-qs-1.0) on the path when a script runs from this folder."""
import pathlib, sys
ROOT = pathlib.Path(__file__).resolve().parent
for p in (ROOT.parent / "ch21", ROOT.parent / "fieldkit", ROOT):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))
