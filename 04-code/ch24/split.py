"""Listing 24.1: the surface/brain split. A simulated productivity-suite surface makes one call per turn; the brain
in Caldwell's cloud checks the mode, exchanges tokens, fans out, drafts, verifies and audits (deterministic stand-in;
the drafting step stands in for the model behind Caldwell's gateway)."""
import json, random, hashlib
import _paths  # noqa: F401
from fieldkit.surface import (Token, TokenBroker, TurnRequest, TurnResponse, ModeFlag, run_turn)
from caldwell import SOURCES, TIMEOUT_MS

RECORDS = {  # what each source returns for claim CL-2026-118204 (synthetic)
    "policy-admin": {"policy": "HO-7731-0442", "status": "in force", "deductible": 1000},
    "claims-core": {"claim": "CL-2026-118204", "state": "open", "loss": "water", "cause_code": None},
    "retrieval": {"passage": "Water damage guide v7 s4.2: cause code required before reserve"},
    "loss-history": {"prior_losses_5y": 1},
    "rules-catalog": {"V-118": "water loss needs a cause code", "V-127": "loss date within 365 days"},
    "fnol-docs": {"documents": 3, "photos": 4},
}
AUDIT = []


class Brain:
    def __init__(self, flag, broker):
        self.flag, self.broker = flag, broker

    def handle(self, req: TurnRequest, now: float, slow_claims=False) -> TurnResponse:
        self.broker.accept(req.assertion, now)                    # refuse foreign or expired assertions first
        mode = self.flag.mode_at(now)
        tokens = {s.name: self.broker.exchange(req.assertion, s.audience, now)[0] for s in SOURCES}
        turn = run_turn(SOURCES, random.Random(sum(map(ord, req.turn_id))), "parallel",
                        timeout_ms=TIMEOUT_MS)
        if slow_claims and "claims-core" not in turn.partial:
            turn.partial.append("claims-core")   # injected: claims-core held past the 2.5 s timeout
        got = {k: v for k, v in RECORDS.items() if k not in turn.partial}
        draft = self.draft(got)
        verdict = self.verify(draft, got)
        audit_id = hashlib.sha256(f"{req.turn_id}{mode}".encode()).hexdigest()[:12]
        AUDIT.append(dict(audit_id=audit_id, turn=req.turn_id, user=req.assertion.subject, mode=mode,
                          sources={k: tokens[k].audience for k in tokens}, partial=turn.partial,
                          verification=verdict, ms=round(turn.total_ms)))
        answer = draft if mode == "live" and verdict.startswith("pass") else None
        return TurnResponse(req.turn_id, mode, answer, sorted(got), turn.partial, verdict, audit_id)

    @staticmethod
    def draft(got):
        out = []
        if "claims-core" in got:
            c = got["claims-core"]
            out.append(f"Claim {c['claim']} is {c['state']}, {c['loss']} loss; cause code not set, so V-118 blocks the reserve.")
        else:
            out.append("Claim status not available from claims-core within 2.5 s; shown as of the last sync.")
        p = got["policy-admin"]
        out.append(f"Policy {p['policy']} {p['status']}, deductible ${p['deductible']:,}.")
        out.append(f"{got['loss-history']['prior_losses_5y']} prior loss in five years; {got['fnol-docs']['documents']} documents, {got['fnol-docs']['photos']} photos.")
        return " ".join(out)

    @staticmethod
    def verify(draft, got):
        facts = [("HO-7731-0442", "policy-admin"), ("$1,000", "policy-admin"), ("V-118", "rules-catalog")]
        missing = [f for f, src in facts if f in draft and src not in got]
        return "pass: 3 facts traced to source records" if not missing else f"fail: {missing}"


class Surface:
    """Thin: holds the user's sign-in assertion for the brain, sends one request, renders what comes back."""
    version = "surface-1.4.0"

    def __init__(self, brain, assertion):
        self.brain, self.assertion, self.calls = brain, assertion, 0

    def ask(self, turn_id, text, now, slow=False):
        self.calls += 1
        r = self.brain.handle(TurnRequest(turn_id, "conv-88", self.version, text, self.assertion), now, slow)
        if r.answer is None:
            return f"[{r.mode}] Open claim in claims-core | Open policy | Ask a colleague"
        banner = f" [partial: {', '.join(r.partial)}]" if r.partial else ""
        return f"{r.answer}{banner}\n    sources: {', '.join(r.citations)} | {r.verification} | audit {r.audit_id}"


if __name__ == "__main__":
    flag = ModeFlag("live"); broker = TokenBroker()
    tom = Token("tom.whitfield@caldwellmutual.com", "api://nl-brain", 0, 3600)
    s = Surface(Brain(flag, broker), tom)
    print("turn t1:", s.ask("t1", "What is holding up CL-2026-118204?", 100))
    print("turn t2:", s.ask("t2", "Same claim, again", 400, slow=True))
    flag.set("shadow", 500, "rollback rehearsal")
    print("turn t3:", s.ask("t3", "And now?", 560))
    print(f"calls across the boundary: {s.calls} for 3 turns")
    fat = 2 * len(SOURCES) + 2   # option D: per source a token call and a data call, plus model and verify
    print(f"option D (orchestration in the suite) would make {fat} crossings per turn, {3*fat} for 3 turns")
    print("broker:", dict(broker.stats))
    print("audit record t3:", json.dumps(AUDIT[-1]))
