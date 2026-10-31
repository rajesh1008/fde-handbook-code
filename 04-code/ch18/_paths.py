"""Put fieldkit on the path when a script runs from this folder."""
import pathlib, sys
ROOT = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT.parent / "fieldkit"))
sys.path.insert(0, str(ROOT))
