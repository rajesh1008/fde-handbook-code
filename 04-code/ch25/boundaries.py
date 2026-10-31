"""Listing 25.1: the release boundaries, one level at a time, and what each customer approved."""
from policy import CALDWELL, GREYSTONE

for b in (CALDWELL, GREYSTONE):
    print(f"== {b.customer}")
    print(b.table())
for op, env in [("create_claim", "preprod"), ("create_claim", "prod"), ("set_reserve", "preprod"),
                ("draft_prior_auth", "sandbox"), ("submit_prior_auth", "sandbox")]:
    b = CALDWELL if op in ("create_claim", "set_reserve") else GREYSTONE
    ok, why = b.check(op, env)
    print(f"check {op:<18} {env:<8} -> {'ALLOW' if ok else 'DENY '} {why}")
