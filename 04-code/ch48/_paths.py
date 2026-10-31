"""Put fieldkit and this folder on sys.path so every script runs from 04-code/ch48."""
import sys, pathlib
HERE = pathlib.Path(__file__).resolve().parent
for p in (HERE.parent / "fieldkit", HERE):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))
OUT = HERE / "output"
OUT.mkdir(exist_ok=True)
