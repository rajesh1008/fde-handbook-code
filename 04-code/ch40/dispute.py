"""The disputed claim's pack: v0 on day 177, then rebuilt from the parameter-store history, then the rerun check."""
import _paths  # noqa: F401
import world as W, pack as P

recs = W.records(W.LIVE, W.DISPUTE)
r = W.disputed(recs)
print("V0 PACK, DAY 177 (prompt resolved through the code commit)")
print(P.render(r, W.REHEARSAL))
print()
print("REBUILT PACK, DAY 181 (prompt resolved from the parameter-store history by timestamp)")
print(P.render(r, W.BACKFILL, use_history=True))
print()
a = W.model(r["doc"], W.PROMPT_A)["loss_location"]; b = W.model(r["doc"], W.PROMPT_B)["loss_location"]
print("WHAT THE AGENT WROTE AND WHY")
print(f"  recorded loss_location      {r['fields']['loss_location']}")
print(f"  claimant letter address     {r['doc']['letter_addr']}")
print(f"  police report address       {r['doc']['police_addr']}  ({r['doc']['police_ref']})")
print(f"  rule in the commit (text A) {W.RULE_A}")
print(f"  rule in force (text B)      {W.RULE_B}")
print(f"  rerun under text A          {a}  -> {'matches' if a == r['fields']['loss_location'] else 'DOES NOT MATCH'} the record")
print(f"  rerun under text B          {b}  -> {'matches' if b == r['fields']['loss_location'] else 'DOES NOT MATCH'} the record")
print(f"  prompt tokens: text A {W.tokens(W.PROMPT_A)}, text B {W.tokens(W.PROMPT_B)}, difference {W.tokens(W.PROMPT_B) - W.tokens(W.PROMPT_A)}")
print(f"  gateway trace input tokens {r['trace_input_tokens']} = document {r['doc']['doc_tokens']} + {r['trace_input_tokens'] - r['doc']['doc_tokens']}")
