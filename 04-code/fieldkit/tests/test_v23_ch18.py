"""fieldkit v2.3 (Chapter 18): the gateway adapter."""
import pytest
from fieldkit.gateway import (GatewayAdapter, GatewayStop, Response, RotationSchedule, VersionLedger,
                              DeprecationRegister, capability_gap, classify, cost_per_success, DAY)


class Fake:
    def __init__(self):
        self.t = 0
        self.key = ("k1", "s1")
        self.valid = {"s1"}
        self.version = "v1"
        self.status = None

    def secret(self):
        return self.key

    def transport(self, method, path, headers, body, ip, t):
        if self.status:
            return Response(self.status, {}, {"error": "ip_not_on_allowlist"})
        if headers["authorization"].split()[1] not in self.valid:
            return Response(401, {}, {"error": "invalid_key"})
        return Response(200, {"x-gw-model-version": self.version, "Deprecation": "@100",
                              "Sunset": "Fri, 06 Mar 1970 00:00:00 GMT"},
                        {"usage": {"input_tokens": 1000, "output_tokens": 500}})


def make(f):
    def sleep(s):
        f.t += s
    return GatewayAdapter(f.transport, f.secret, app_id="a", api_version="2026-02-01", clock=lambda: f.t,
                          sleep=sleep, source_ip="10.0.0.1", prices={"d": (0.001, 0.002)})


def test_refresh_on_401_survives_rotation():
    f = Fake(); a = make(f)
    f.key, f.valid = ("k2", "s2"), {"s2"}
    rec, _ = a.call("d", {})
    assert rec.kind == "ok" and rec.key_id == "k2" and rec.attempts == 2


def test_allowlist_stops_without_retry():
    f = Fake(); a = make(f); f.status = 403
    with pytest.raises(GatewayStop) as e:
        a.call("d", {})
    assert e.value.kind == "allowlist" and a.records[-1].attempts == 1


def test_classify_table():
    assert classify(429) == "rate_limited" and classify(410) == "retired"
    assert classify(400, {"error": "content_filter.violence"}) == "content_filtered"
    assert classify(400, {"error": "api-version required"}) == "bad_request"


def test_deprecation_register_and_cost():
    f = Fake(); a = make(f); a.call("d", {})
    (target, days, level, _), = a.deprecations.report(now=0)
    assert days == 64 and level == "info"
    assert cost_per_success(a.records, 1)[2] == 0.002


def test_version_ledger_flags_alias_move():
    v = VersionLedger({"d": "v1"})
    v.observe("d", "v1", 0); v.observe("d", "v2", 10); v.observe("d", "v1", 20)
    assert len(v.changes) == 2 and round(v.unexpected_share("d"), 2) == 0.33


def test_rotation_schedule_and_gap():
    r = RotationSchedule(weekday=3, hour=2, grace_s=3600)
    assert r.next_rotation(0) == 3 * DAY + 7200
    gap = capability_gap([{"capability": "chat"}], {"chat": ["x"], "embeddings": ["y"]})
    assert [g["offered"] for g in gap] == [True, False]
