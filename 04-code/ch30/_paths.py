import sys, pathlib
HERE = pathlib.Path(__file__).resolve().parent
for p in (HERE.parent / "fieldkit", HERE):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))
