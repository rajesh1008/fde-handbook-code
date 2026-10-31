"""The evaluation suite core: identical on every estate. It sees only the model and log ports."""
from collections import Counter
from fieldkit.gateway import VersionLedger
from sim_clouds import FAMILY, CallFailed


def run(port, customer, gold_ids, pinned, rotate_at=None, rotate=None):
    ledger = VersionLedger({FAMILY: pinned})
    correct = fields = failures = calls = with_tokens = 0
    per_item = {}
    for k, item in enumerate(gold_ids):
        if rotate_at is not None and k == rotate_at:
            rotate()
        try:
            res = port.call({"customer": customer, "item": item})
        except CallFailed:
            failures += 1
            continue
        calls += 1
        ledger.observe(FAMILY, res.served_version, k)
        ok = {f: v == f"{item}:{f}" for f, v in res.output.items()}
        per_item[item] = ok
        correct += sum(ok.values())
        fields += len(ok)
        rec = {"item": item, "served": res.served_version, "region": res.region, "request_id": res.request_id,
               "tokens_in": res.tokens_in, "tokens_out": res.tokens_out}
        with_tokens += rec["tokens_in"] > 0
        port.log(rec)
    acc = correct / fields if fields else 0.0
    return dict(accuracy=acc, correct=correct, fields=fields, failures=failures, calls=calls,
                attempted=len(gold_ids), with_tokens=with_tokens, served=Counter(ledger.counts.get(FAMILY, {})),
                per_item=per_item)
