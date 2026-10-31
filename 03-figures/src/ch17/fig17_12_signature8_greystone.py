"""Figure 17.11: Signature 8 for Greystone (Azure), day 89 review with four required changes."""
from _common import S  # noqa: F401  (sets paths)
import signature8
signature8.STATES.setdefault("greystone", dict(
    title="Greystone Health: Azure, centralus",
    identity="app secret", keys="Key Vault", logs="Greystone|workspace",
    network="VNet, own DNS zone", runner="container app|no public IP", gateway="Greystone's",
    tenancy="provider operates", model="via gateway", vendor="no data path",
    changes={"identity": "1, 4", "network": "2, 3"}))
signature8.render("greystone", "fig17-12", __file__)
