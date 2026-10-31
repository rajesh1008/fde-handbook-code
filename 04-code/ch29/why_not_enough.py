"""Listing 29.1: what Caldwell's API and UI tests saw while the agent was wrong (days 106 to 140 defect log).
Deterministic stand-in: the defect log's categories and counts are the chapter's, the cases are generated."""
import json
import world as W

# defect log kept by Northlight and Anne Kessler's team, days 106 to 140 (shadow mode, Chapter 25)
LOG = [("rule or pure-function bug (dates, V-118 codes)", 9, 1, 0),
       ("extraction regression on one document class", 8, 2, 0),
       ("retrieval answer not supported by its citation", 5, 2, 0),
       ("contract or wiring fault (claims-core, gateway)", 7, 3, 3),
       ("multi-step scenario (duplicates, page order)", 6, 4, 0),
       ("drift or live-only behavior (templates, volume)", 6, 5, 0)]

print("Caldwell QE regression suite against the agent: 312 API tests, 58 UI tests")
doc, stratum = "GT-0010", W.STRATUM["GT-0010"]
resp = dict(status=201, body=dict(claim_id="CLM-0418877", date_received="2026-03-02", policy_number="CM-HO-2291847"))
api_ok = resp["status"] == 201 and all(isinstance(v, str) and v for v in resp["body"].values())
gold = "2026-02-26"
print(f"  example: POST /intake for {doc} ({stratum})")
print(f"    API test: status {resp['status']}, schema valid -> {'PASS' if api_ok else 'FAIL'}")
print(f"    gold value for date_received {gold}, agent wrote {resp['body']['date_received']} -> WRONG")
print()
print(f"{'defect category':50} {'found':>5} {'layer':>5} {'API/UI':>6}")
tot = api = 0; rows = {}
for name, n, layer, caught in LOG:
    print(f"{name:50} {n:>5} {'L' + str(layer):>5} {caught:>6}")
    tot += n; api += caught; rows[name] = [n, layer, caught]
print(f"{'total':50} {tot:>5} {'':>5} {api:>6}")
print(f"API and UI tests caught {api} of {tot} ({api / tot:.0%}); every one was a wiring fault with an HTTP error.")
json.dump(dict(rows=rows, total=tot, api=api), open("output/why_not_enough.json", "w"), indent=1)
