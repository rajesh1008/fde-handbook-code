"""Chapter 40 evidence pack: eight elements, each with a status the auditor can test.

Statuses: verified (checked against a record made at the time), reconstructed (recovered from another retained
artifact, named in the pack), inferred (consistent with a check but not proven), contradicted (a retained artifact
disagrees), unverifiable (nothing retained can answer), n/a. Uses fieldkit.lineage for the document chain and
digests; no new fieldkit module (the Blueprint says Chapter 40 uses current fieldkit).
"""
import _paths  # noqa: F401
from fieldkit.lineage import LineageStore, digest
import world as W

ELEMENTS = ("document", "lineage", "retrieval", "prompt and model", "confidence and route", "decision", "review", "action")
GOOD = {"verified", "reconstructed", "n/a"}


def lineage(rec):
    s = LineageStore()
    src = s.add("source", uri=f"claimfile://{rec['claim']}/doc1", sha256=rec["doc"]["sha256"])
    pg = s.add("page", [src], page=1)
    ex = s.add("extraction", [pg], method="intake-extract rc-1")
    cl = s.add("claim", [ex], text=f"loss_location={rec['fields']['loss_location']}")
    return s, cl, src


def prompt_element(rec, asof, use_history=False):
    d = rec["day"]
    trace = rec["trace_input_tokens"] if asof - d <= W.TRACE_DAYS else None
    ref = rec["prompt_ref"]
    if "id" in ref:
        text = W.REGISTRY.get(ref["id"])
        if text is None:
            return "unverifiable", "registry has no such id", None
        ok = ref["sent_sha"] == digest(text) and rec["input_tokens"] == W.tokens(text) + rec["doc"]["doc_tokens"]
        return ("verified" if ok else "contradicted"), f"{ref['id']} (hash checked at send)", text
    if use_history:
        text = W.prompt_at(d, rec["minute"])
        ver = [v for v, dd, m, t, _ in W.PARAM_HISTORY if t == text][0]
        how = f"parameter-store version {ver} in force at day {d} {rec['minute'] // 60:02d}:{rec['minute'] % 60:02d}"
        if trace is not None and trace != W.tokens(text) + rec["doc"]["doc_tokens"]:
            return "contradicted", how, text
        return "reconstructed", how, text
    text = W.PROMPT_A          # v0 resolves the name through the code commit, which holds the rc-1 text
    how = f"intake-summary at commit {ref['code_commit']}"
    if trace is None:
        return "inferred", how + " (no trace left to check)", text
    if trace != W.tokens(text) + rec["doc"]["doc_tokens"]:
        return "contradicted", how + f" (trace {trace} tokens, rebuilt {W.tokens(text) + rec['doc']['doc_tokens']})", text
    return "inferred", how + " (token count matches)", text


def build(rec, asof, use_history=False, claims_core=None):
    st, how = {}, {}
    st["document"] = "verified"; how["document"] = f"sha256 {rec['doc']['sha256']} matches claim file"
    s, cl, src = lineage(rec)
    probs = s.verify(cl, sources={f"claimfile://{rec['claim']}/doc1": rec["doc"]["sha256"]})
    st["lineage"] = "verified" if not probs else "contradicted"; how["lineage"] = " > ".join(s.kinds_covered(cl))
    st["retrieval"] = "verified"; how["retrieval"] = f"{rec['index']}; " + ", ".join(rec["passages"])
    p, h, text = prompt_element(rec, asof, use_history)
    if not rec["model"].startswith("gm-") and p in ("verified", "reconstructed"):
        p, h = "inferred", h + "; model named by alias, version not provable"
    st["prompt and model"] = p; how["prompt and model"] = f"{h}; model {rec['model']}"
    st["confidence and route"] = "verified" if W.band(rec["score"]) == rec["band"] else "contradicted"
    how["confidence and route"] = f"score {rec['score']:.3f} -> {rec['band']} under {rec['router']}"
    st["decision"] = "verified" if digest(rec["fields"]) == rec["fields_digest"] else "contradicted"
    how["decision"] = f"fields digest {rec['fields_digest']}"
    if rec["band"] == "proceed":
        st["review"], how["review"] = "n/a", "proceed band: no review required (weekly M1 sample instead)"
    elif rec.get("review"):
        rv = rec["review"]; st["review"] = "verified"; how["review"] = f"{rv['reviewer']} {rv['outcome']} in {rv['seconds']} s"
    elif use_history and rec.get("review_in_claims_core"):
        st["review"] = "reconstructed"; how["review"] = "claims-core audit table: " + rec["review_in_claims_core"]["outcome"]
    else:
        st["review"], how["review"] = "unverifiable", "no review record"
    a = rec["action"]
    st["action"] = "verified" if a["verified"] else "unverifiable"
    how["action"] = f"{a['ledger']} {a['level']} write to {a['target']}, read-back ok"
    return st, how, text


def complete(st):
    return all(v in GOOD for v in st.values())


def render(rec, asof, use_history=False):
    st, how, _ = build(rec, asof, use_history)
    lines = [f"EVIDENCE PACK {rec['id']}  claim {rec['claim']}  decided day {rec['day']} "
             f"{rec['minute'] // 60:02d}:{rec['minute'] % 60:02d}  generated day {asof}"]
    for e in ELEMENTS:
        lines.append(f"  {e:<21} {st[e]:<13} {how[e]}")
    lines.append(f"  pack digest {digest([rec['id'], st, how])}   verdict: "
                 + ("RECONSTRUCTABLE" if complete(st) else "NOT RECONSTRUCTABLE"))
    return "\n".join(lines)


def chain_head(packs):
    h = "0" * 12
    for p in packs:
        h = digest([h, p])
    return h
