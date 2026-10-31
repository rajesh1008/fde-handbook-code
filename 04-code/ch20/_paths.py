"""Puts fieldkit and this lab on the import path (listings omit this set-up)."""
import pathlib, sys
HERE = pathlib.Path(__file__).resolve().parent
for p in (HERE.parent / "fieldkit", HERE):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))
