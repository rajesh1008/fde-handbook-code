"""Failure injection: a provider deprecation during a customer change freeze (Chapter 42).
Usage: python deprecation.py v0|v1
The provider retires extract-2026-01, the pin for Pennant's EU lanes (Chapter 20), with 21 days' notice. The
retirement falls inside Pennant's peak-season change freeze. v0 is the engagement as handed over: the notice goes
to the provider account's owner of record, Jenna Ruiz, who left the role on day 14. v1 uses liveops.deprecation_plan
with the account moved to Kofi Mensah and the upgrade gate run under a freeze exception."""
import sys
import _paths  # noqa: F401
from world import CAL, volume, EU_SHARE, SHARE
from fieldkit.liveops import deprecation_plan, upgrade_gate

mode = sys.argv[1] if len(sys.argv) > 1 else "v1"
N, R, F = CAL["notice"], CAL["retire"], CAL["freeze"]
eu_docs = lambda a, b: round(sum(volume(d) * sum(SHARE) * EU_SHARE for d in range(a, b + 1)))
print(f"PROVIDER DEPRECATION  extract-2026-01 (Pennant EU pin, europe-west4)  mode {mode}")
print(f"notice day {N}  retirement day {R}  change freeze days {F[0]}-{F[1]}  evidence needs 7 days")
if mode == "v0":
    read = 52
    p = deprecation_plan(N, R, [F], evidence_days=7, read_day=read)
    print(f"notice sent to: jenna.ruiz (account owner of record; left the sponsor role day {CAL['jenna_last']})")
    print(f"notice first read: day {read}, by the FDE checking the provider's console; {read - N} days lost")
    print(f"plan: {p['action']}; slack {p['slack_days']} days")
    print("change board: freeze exception refused on day 53 (no named business owner to request it, no evidence)")
    print(f"day {R}: retirement. The estate pin refuses substitution (Chapter 20): EU extraction calls fail closed")
    lost = eu_docs(R, F[1] + 1)
    print(f"days {R}-{F[1] + 1}: EU lane documents to the clerks: {lost} (peak season, {F[1] + 2 - R} days)")
    print("what the gateway's 410 rule would have done instead: move to the successor, an unrecorded model change "
          "inside a freeze, on a model Pennant never approved for EU documents")
    print("result: outage on the EU lane; no model change recorded; Live Stable criterion 5 open")
else:
    p = deprecation_plan(N, R, [F], evidence_days=7)
    print(f"notice sent to: jenna.ruiz, forwarded since day {CAL['grant_accepts']} to the provider-notices list; read day {CAL['notice']} by Kofi Mensah (account itself moved day {CAL['account_moved']})")
    print(f"plan: retirement in freeze: {p['retire_in_freeze']}; last normal change day {p['last_safe_normal_day']}; "
          f"evidence ready day {p['earliest_ready']}; freeze exception needed: {p['freeze_exception']}")
    print(f"      {p['action']}; slack {p['slack_days']} days")
    print(f"day 43: freeze exception requested at the change board by Kofi Mensah, with the plan and a rollback path")
    dims = {"evaluation suite (EU gold set, pass 85)": (89.3, 87.2, 85.0, True),
            "fully correct documents of 200": (103, 76, 76, True),
            "silently wrong on 200 (Dana's team)": (0, 0, 0, False),
            "cost per document, USD": (0.0358, 0.0358, 0.0400, False),
            "p95 latency, s": (4.1, 3.8, 6.0, False)}
    v, why = upgrade_gate(dims, lost_critical=15)
    print(f"days 48-52: upgrade gate extract-2026-04 vs extract-2026-01: {v}")
    for w in why:
        print(f"  {w}")
    v2, why2 = upgrade_gate(dims, lost_critical=15, signoff="Dana Whitaker",
                            accepted={"p95 latency, s": "Kofi Mensah"})
    print(f"day 53: Dana Whitaker signs off the 15 lost fields (1 piece count, 0 Incoterms, 14 in other fields); "
          f"Kofi Mensah accepts the latency against the batch budget: {v2}")
    for w in why2:
        print(f"  {w}")
    print(f"day {CAL['mr_approval']}: model-risk approval, Joanne Pruitt, Pennant finance controller; recorded model change MC-EU-02")
    print(f"day {CAL['migrate']}: migrated in the exception window 14:00-15:00 Memphis time, outside the 02:00 batch")
    print(f"days {CAL['migrate']}-{R - 1}: rollback to extract-2026-01 available for {R - CAL['migrate']} days; not used")
    print("EU lane documents to the clerks: 0")
