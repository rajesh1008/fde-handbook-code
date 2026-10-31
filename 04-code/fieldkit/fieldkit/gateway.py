"""Gateway adapter (fieldkit v2.3, Chapter 18).

Every model call at a customer that mandates a gateway goes through this module. It does five
things the customer's platform will not do for you:

* reads the key from the customer's secret store, refreshes it before a scheduled rotation and once
  more on a 401, and never keeps a key in an environment variable;
* classifies every non-200 into an action (refresh, wait, stop, route to a person) instead of
  retrying everything;
* records Deprecation and Sunset headers in a register with days left and an alert level;
* records the model version the gateway actually served on every call, so an alias that moves, or a
  route that is diluted, shows up in a ledger and not in an accuracy number weeks later;
* writes one CallRecord per logical call, which is the evidence for cost per successful task.

Standard library only. The transport is a callable, so the same adapter runs against the lab
simulator, a recorded fixture, or the customer's real gateway.
"""
from __future__ import annotations

import email.utils
from collections import Counter
from dataclasses import dataclass, field
from typing import Callable

DAY = 86400

# Error kind -> what the adapter does. The order of the table is the order of Table 18.3.
ACTIONS = {
    "auth": "refresh the key from the secret store, retry once, then stop and page the key owner",
    "allowlist": "stop; open a ticket with the network owner; never retry",
    "rate_limited": "wait for Retry-After, then retry inside the retry budget",
    "content_filtered": "do not retry; route the item to a person; log the filter category",
    "retired": "stop; switch to the successor named in the deprecation register",
    "bad_request": "stop; a contract test should have caught this",
    "server": "retry with backoff inside the retry budget",
}
STOP_KINDS = {"allowlist", "retired", "bad_request"}


def classify(status: int, body: dict | None = None) -> str:
    """Map a gateway response to one error kind (or "ok")."""
    body = body or {}
    code = str(body.get("error", ""))
    if 200 <= status < 300:
        return "ok"
    if status == 401:
        return "auth"
    if status == 403:
        return "allowlist" if "allowlist" in code or "ip" in code else "auth"
    if status == 429:
        return "rate_limited"
    if status in (404, 410) and ("retired" in code or "sunset" in code or status == 410):
        return "retired"
    if status == 400 and "content_filter" in code:
        return "content_filtered"
    if 400 <= status < 500:
        return "bad_request"
    return "server"


class GatewayStop(Exception):
    """Raised for kinds that must not be retried. Carries the kind and the action."""

    def __init__(self, kind: str, detail: str = ""):
        super().__init__(f"{kind}: {ACTIONS.get(kind, '')} ({detail})")
        self.kind = kind
        self.detail = detail


@dataclass
class Response:
    status: int
    headers: dict
    body: dict


@dataclass
class CallRecord:
    t: int
    deployment: str
    status: int
    kind: str
    served_version: str | None
    request_id: str | None
    attempts: int
    key_id: str | None
    tokens_in: int = 0
    tokens_out: int = 0
    cost: float = 0.0


def parse_when(value: str | None) -> int | None:
    """Parse a Deprecation value ("@<seconds>", RFC 9745) or an HTTP-date Sunset (RFC 8594)."""
    if not value:
        return None
    value = value.strip()
    if value.startswith("@"):
        return int(value[1:])
    dt = email.utils.parsedate_to_datetime(value)
    return int(dt.timestamp())


def successor_from_link(link: str | None) -> str | None:
    """Pull rel="successor-version" out of a Link header, if the gateway sends one."""
    for part in (link or "").split(","):
        if 'rel="successor-version"' in part:
            return part.split(";")[0].strip().strip("<>")
    return None


@dataclass
class DeprecationEntry:
    target: str
    first_seen: int
    deprecated_at: int | None
    sunset_at: int | None
    successor: str | None

    def days_left(self, now: int) -> int | None:
        return None if self.sunset_at is None else (self.sunset_at - now) // DAY

    def level(self, now: int) -> str:
        d = self.days_left(now)
        if d is None:
            return "warn"          # deprecated with no date is worse than a date
        if d < 0:
            return "retired"
        if d <= 7:
            return "page"
        if d <= 30:
            return "warn"
        return "info"


class DeprecationRegister:
    """Every Deprecation or Sunset header the gateway sends, kept as data with an owner-facing level."""

    def __init__(self):
        self.entries: dict[str, DeprecationEntry] = {}

    def observe(self, target: str, headers: dict, now: int) -> DeprecationEntry | None:
        h = {k.lower(): v for k, v in headers.items()}
        if "deprecation" not in h and "sunset" not in h:
            return None
        e = self.entries.get(target)
        if e is None:
            e = DeprecationEntry(target, now, parse_when(h.get("deprecation")),
                                 parse_when(h.get("sunset")), successor_from_link(h.get("link")))
            self.entries[target] = e
        return e

    def report(self, now: int) -> list[tuple[str, int | None, str, str | None]]:
        return [(e.target, e.days_left(now), e.level(now), e.successor) for e in self.entries.values()]


class VersionLedger:
    """Served model version per deployment, per call. Flags changes and unexpected versions."""

    def __init__(self, expected: dict[str, str] | None = None):
        self.expected = dict(expected or {})
        self.last: dict[str, str] = {}
        self.counts: dict[str, Counter] = {}
        self.changes: list[tuple[int, str, str | None, str]] = []

    def observe(self, deployment: str, version: str | None, t: int):
        if version is None:
            version = "unreported"
        self.counts.setdefault(deployment, Counter())[version] += 1
        prev = self.last.get(deployment)
        if prev != version:
            if prev is not None or (deployment in self.expected and self.expected[deployment] != version):
                self.changes.append((t, deployment, prev, version))
            self.last[deployment] = version

    def unexpected_share(self, deployment: str) -> float:
        c = self.counts.get(deployment, Counter())
        n = sum(c.values())
        exp = self.expected.get(deployment)
        return 0.0 if n == 0 or exp is None else 1 - c[exp] / n


@dataclass
class RotationSchedule:
    """The customer's rotation, as published: weekday (0 = engagement day 0's weekday), hour, grace."""
    weekday: int
    hour: int
    grace_s: int
    period_days: int = 7

    def next_rotation(self, now: int) -> int:
        day = now // DAY
        for k in range(0, self.period_days + 1):
            t = (day + k) * DAY + self.hour * 3600
            if (day + k) % self.period_days == self.weekday and t > now:
                return t
        return (day + self.period_days) * DAY + self.hour * 3600


class GatewayAdapter:
    """The one door through which Northlight code calls a customer's model gateway."""

    def __init__(self, transport: Callable, read_secret: Callable[[], tuple[str, str]], *,
                 app_id: str, api_version: str, clock: Callable[[], int], sleep: Callable[[int], None],
                 source_ip: str, rotation: RotationSchedule | None = None, retry_budget: int = 3,
                 prices: dict[str, tuple[float, float]] | None = None, expected_versions: dict | None = None):
        self.transport, self.read_secret = transport, read_secret
        self.app_id, self.api_version = app_id, api_version
        self.clock, self.sleep, self.source_ip = clock, sleep, source_ip
        self.rotation, self.retry_budget = rotation, retry_budget
        self.prices = prices or {}
        self.deprecations = DeprecationRegister()
        self.versions = VersionLedger(expected_versions)
        self.records: list[CallRecord] = []
        self.refreshes: list[tuple[int, str]] = []
        self.key_id, self.secret = None, None
        self.key_read_at = None
        self._refresh("start")

    # -- keys -------------------------------------------------------------
    def _refresh(self, why: str):
        self.key_id, self.secret = self.read_secret()
        self.key_read_at = self.clock()
        self.refreshes.append((self.key_read_at, f"{why}:{self.key_id}"))

    def _maybe_refresh_for_rotation(self):
        if self.rotation is None or self.key_read_at is None:
            return
        last_rot = self.rotation.next_rotation(self.key_read_at)
        if self.clock() >= last_rot + 300:      # five minutes after a rotation, read again
            self._refresh("scheduled")

    # -- the call ---------------------------------------------------------
    def headers(self) -> dict:
        return {"authorization": f"Bearer {self.secret}", "x-app-id": self.app_id,
                "api-version": self.api_version}

    def call(self, deployment: str, payload: dict, path: str | None = None) -> tuple[CallRecord, dict]:
        self._maybe_refresh_for_rotation()
        path = path or f"/v2/deployments/{deployment}/chat"
        attempts, refreshed = 0, False
        while True:
            attempts += 1
            t = self.clock()
            r = self.transport("POST", path, self.headers(), payload, self.source_ip, t)
            kind = classify(r.status, r.body)
            self.deprecations.observe(path, r.headers, t)
            if kind == "ok":
                v = r.headers.get("x-gw-model-version")
                self.versions.observe(deployment, v, t)
                usage = r.body.get("usage", {})
                pin, pout = self.prices.get(deployment, (0.0, 0.0))
                ti, to = usage.get("input_tokens", 0), usage.get("output_tokens", 0)
                rec = CallRecord(t, deployment, r.status, kind, v, r.headers.get("x-gw-request-id"), attempts,
                                 self.key_id, ti, to, round(ti / 1000 * pin + to / 1000 * pout, 6))
                self.records.append(rec)
                return rec, r.body
            if kind == "auth" and not refreshed:
                refreshed = True
                self._refresh("on-401")
                continue
            if kind in ("rate_limited", "server") and attempts <= self.retry_budget:
                wait = int(r.headers.get("retry-after", 2 ** attempts))
                self.sleep(wait)
                continue
            rec = CallRecord(t, deployment, r.status, kind, r.headers.get("x-gw-model-version"),
                             r.headers.get("x-gw-request-id"), attempts, self.key_id)
            self.records.append(rec)
            if kind in STOP_KINDS or kind == "auth":
                raise GatewayStop(kind, f"{deployment} {r.status} {r.body.get('error', '')}")
            return rec, r.body          # content_filtered or exhausted budget: the caller routes it

    def smoke_test(self, deployments: list[str]) -> list[tuple[str, str]]:
        """The post-rotation check: one tiny call per deployment, reported as (deployment, kind)."""
        out = []
        for d in deployments:
            try:
                rec, _ = self.call(d, {"text": "smoke", "max_tokens": 1})
                out.append((d, rec.kind))
            except GatewayStop as e:
                out.append((d, e.kind))
        return out


def capability_gap(catalog: list[dict], required: dict[str, list[str]]) -> list[dict]:
    """Compare what the design needs with what the gateway's live catalog offers (not its docs)."""
    offered = {c["capability"] for c in catalog if c.get("status", "active") == "active"}
    return [{"capability": cap, "needed_for": uses, "offered": cap in offered}
            for cap, uses in required.items()]


def cost_per_success(records: list[CallRecord], ok_tasks: int) -> tuple[float, float, float]:
    """(total cost, cost per successful call, cost per successful task) from the call records."""
    total = round(sum(r.cost for r in records), 4)
    ok_calls = sum(1 for r in records if r.kind == "ok")
    return total, round(total / max(ok_calls, 1), 5), round(total / max(ok_tasks, 1), 5)
