"""Which tenancy option each customer's required controls allow (Table 17.1 data)."""
import _paths  # noqa: F401
from fieldkit.environment import CONTROLS, TENANCY, choose_tenancy, tenancy_gaps

need = {"Caldwell Mutual": ["network", "identity", "keys", "logs"],
        "Greystone Health": list(CONTROLS),
        "Pennant Logistics": ["network", "keys", "logs"],
        "Harbourline Bank": list(CONTROLS)}
print("options, least customer burden first:")
for k, v in TENANCY.items():
    print(f"  {k:18} {v['label']:38} customer holds: {', '.join(v['customer_holds']) or 'nothing'}")
print()
for cust, req in need.items():
    pick = choose_tenancy(req)
    print(f"{cust:18} requires {len(req)} -> {pick:18} vendor-shared would leave {len(tenancy_gaps('vendor-shared', req))} with the vendor")
