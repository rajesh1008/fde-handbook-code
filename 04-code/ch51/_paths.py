"""Put fieldkit and the Chapter 11 sponsor-map lab on the path when a script runs from this folder."""
import pathlib, sys
ROOT = pathlib.Path(__file__).resolve().parent
for p in (ROOT.parent / "fieldkit", ROOT.parent / "ch11", ROOT):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))
