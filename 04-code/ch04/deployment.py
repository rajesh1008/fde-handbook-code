"""Chapter 4 imports the readiness model from fieldkit (promoted from this lab; source in
04-code/fieldkit/fieldkit/deployment.py)."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "fieldkit"))
from fieldkit.deployment import *  # noqa: F401,F403
from fieldkit.deployment import Checklist, Proof, Verdict, DIMENSIONS, STATUSES, is_person  # noqa: F401
