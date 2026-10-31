import pathlib, sys
_FK = pathlib.Path(__file__).resolve().parents[1] / "fieldkit"
if str(_FK) not in sys.path:
    sys.path.insert(0, str(_FK))
