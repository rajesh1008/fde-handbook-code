"""Chapter 15, Stage 0: Caldwell Mutual, day 47. The status report the access tracker prints the morning
the first 200 real claim files arrive, and the readiness check run on their manifest."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "fieldkit"))
from fieldkit.fixtures import caldwell_tracker, caldwell_sample, caldwell_register

tracker = caldwell_tracker()
print(tracker.status_report(today=47))
print()
print(caldwell_register().assess("caldwell-claims-sample", caldwell_sample()).summary())
