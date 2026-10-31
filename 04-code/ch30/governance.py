"""The training-data record, the model-risk classification change and the switch gate."""
import _paths  # noqa: F401
from fieldkit.finetune import TrainingDataRecord, risk_class, SwitchGate

draft = TrainingDataRecord(dataset="history-6000 (clerk-coded claim documents, 2025-2026)",
                           source_system="claims document store", data_owner="Ruth Calloway",
                           label_owner="Anne Kessler", location="Caldwell AWS 111122223333 us-east-1")
print("day 135 draft, missing:", ", ".join(draft.missing()))
signed = TrainingDataRecord(
    dataset=draft.dataset, source_system=draft.source_system, data_owner="Ruth Calloway", label_owner="Anne Kessler",
    purpose="C06 document type only; no other task, no other customer",
    permitted_uses="train, evaluate and serve c06-ft models inside Caldwell's account",
    location="Caldwell AWS 111122223333 us-east-1, bucket claims-eval/ft",
    retention="training copy deleted 30 days after the model it trained is retired",
    derived_artifacts="weights and adapters are Caldwell data; no copy leaves the account",
    excluded="Anne's set (gold-set-300, cal-600), legal mail, finance cage P09",
    dedupe_against="Anne's set, audit-400", signed_by=["Ruth Calloway", "Anne Kessler", "Priya Natarajan"],
    signed_day=138)
print("day 138 signed, missing:", signed.missing() or "nothing")
print()
print("model-risk classification of C06")
print("  before (prompted vendor model):", risk_class(False, True))
print("  after (fine-tuned on Caldwell data):", risk_class(True, True))
print()
gate = SwitchGate(["training-data record signed", "paired comparison on Anne's set, p < 0.05",
                   "guard holds 60 of 60 on legal-60", "no in-scope class worse than c06-p4 by more than 2 points",
                   "10 shadow days behind the router", "model-risk validation signed", "rollback to c06-p4 tested"])
ev = {"training-data record signed": True, "paired comparison on Anne's set, p < 0.05": True,
      "guard holds 60 of 60 on legal-60": True, "no in-scope class worse than c06-p4 by more than 2 points": True,
      "10 shadow days behind the router": False, "model-risk validation signed": False, "rollback to c06-p4 tested": True}
ok, missing = gate.check(ev)
print(f"switch gate on day 150: {'open' if ok else 'closed'}; waiting on: {'; '.join(missing)}")
