"""Claim-scoped state under Caldwell's controls (Chapter 31 lab; deliberately not a fieldkit module).

Three scopes, agreed with Caldwell before the first write:
  claim        what one intake run needs to resume, be reviewed and be audited, keyed by the intake key that
               claims-core holds in the Agent Ref field; read by the claim's adjuster (live) or the shadow readers
  operational  numbers the agent may carry across claims: sender orientation counts, template fingerprints, band
               counts; numbers only, never text, never a person's details
  never        document text, page images and the listed identifiers: the agent keeps pointers into Caldwell's
               document store, never copies
Retention: shadow state 90 days (Priya Natarajan's storage decision, day 48); live working state 30 days after the
claims-core write is verified (proposal signed day 154, a Chapter 31 addition). A legal hold stops the retention
job and an erasure. Every deletion, refusal and read goes to a log Caldwell holds."""
from dataclasses import dataclass, field

SHADOW_DAYS_KEPT, LIVE_DAYS_KEPT = 90, 30
NEVER = ("document_text", "page_image", "ssn", "bank_account", "medical_narrative", "driver_license")
OPS_KEYS = ("sender_orientation", "template_fingerprint", "band_counts")
SHADOW_READERS = {"nl-shadow-readers"}


class ScopeViolation(Exception):
    pass


@dataclass(frozen=True)
class Value:
    value: object
    source_claim: str      # the intake key of the claim whose document the value was read from
    source_ref: str        # document, page and span: a pointer, not a copy


@dataclass
class ClaimRecord:
    key: str
    mode: str
    opened: int
    adjuster: str = ""
    items: dict = field(default_factory=dict)
    verified: int | None = None     # day the claims-core write was verified (live mode only)


class ClaimStateStore:
    def __init__(self, owner="Caldwell (Ruth Calloway, claims data; Priya Natarajan, platform)"):
        self.owner, self.claims, self.ops, self.holds, self.log = owner, {}, {}, {}, []

    def _log(self, day, actor, action, key, detail=""):
        self.log.append((day, actor, action, key, detail))

    def open(self, key, mode, day, adjuster=""):
        self.claims.setdefault(key, ClaimRecord(key, mode, day, adjuster))
        return self.claims[key]

    def put(self, key, name, v, day, actor="nl-shadow"):
        if name in NEVER:
            self._log(day, actor, "write refused", key, f"{name}: never stored")
            raise ScopeViolation(f"{name} is never stored by the agent; keep a pointer")
        if v.source_claim != key:
            self._log(day, actor, "write refused", key, f"{name} cites {v.source_claim}")
            raise ScopeViolation(f"{name} for {key} was read from {v.source_claim}: cross-claim write")
        self.claims[key].items[name] = v

    def put_ops(self, key, sub, value, day, actor="nl-shadow"):
        if key not in OPS_KEYS:
            self._log(day, actor, "ops write refused", key, "unknown key")
            raise ScopeViolation(f"{key} is not an operational memory key")
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            self._log(day, actor, "ops write refused", key, "not a number")
            raise ScopeViolation("operational memory holds numbers only, never text")
        self.ops.setdefault(key, {})[sub] = value

    def read(self, key, who, day):
        rec = self.claims[key]
        ok = who in SHADOW_READERS if rec.mode == "shadow" else who == rec.adjuster
        self._log(day, who, "read" if ok else "read refused", key)
        if not ok:
            raise PermissionError(f"{who} may not read {key}")
        return dict(rec.items)

    def hold(self, key, day, by, matter):
        self.holds[key] = (day, by, matter)
        self._log(day, by, "legal hold", key, matter)

    def due(self, rec, day):
        if rec.mode == "shadow":
            return rec.opened + SHADOW_DAYS_KEPT <= day
        return rec.verified is not None and rec.verified + LIVE_DAYS_KEPT <= day

    def retention(self, day, actor="retention job"):
        out = dict(deleted=0, items=0, held=0, kept=0)
        for key in sorted(self.claims):
            rec = self.claims[key]
            if not self.due(rec, day):
                out["kept"] += 1
            elif key in self.holds:
                out["held"] += 1
                self._log(day, actor, "delete skipped: legal hold", key, self.holds[key][2])
            else:
                out["deleted"] += 1; out["items"] += len(rec.items)
                self._log(day, actor, "deleted", key, f"{len(rec.items)} items")
                del self.claims[key]
        return out

    def erase(self, key, day, request, actor="privacy request"):
        if key in self.holds:
            self._log(day, actor, "erase refused: legal hold", key, request)
            return dict(erased=0, status="refused: legal hold " + self.holds[key][2])
        n = len(self.claims.pop(key).items) if key in self.claims else 0
        self._log(day, actor, "erased", key, request)
        return dict(erased=n, status="erased from the agent's store",
                    outside=["claim record in claims-core (Caldwell's record retention schedule)",
                             "original documents in Caldwell's document store"])


def scope_check(draft_key, values):
    """Every value in a draft must have been read from this claim's documents."""
    return sorted((n, v.source_claim) for n, v in values.items() if v.source_claim != draft_key)
