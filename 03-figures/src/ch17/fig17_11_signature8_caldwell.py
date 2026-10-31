"""Figure 17.10: Signature 8 for Caldwell (AWS), the environment design Natarajan approved on day 67."""
from _common import S  # noqa: F401  (sets paths)
import signature8
signature8.STATES.setdefault("caldwell", dict(
    title="Caldwell Mutual: AWS, us-east-1",
    identity="role|on-behalf-of", keys="Caldwell KMS", logs="Caldwell|90 days",
    network="VPC, no route out", runner="ECS task|no public IP", gateway="Caldwell's",
    tenancy="team account", model="via gateway", vendor="no data path",
    changes={}))
signature8.render("caldwell", "fig17-11", __file__)
