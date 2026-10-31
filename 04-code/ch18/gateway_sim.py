"""A simulated customer model gateway (deterministic stand-in for Caldwell's, Pennant's, Greystone's).

Engagement day 0 is a Thursday, so day 73 is a Sunday and day 47 a Tuesday, as in the book.
The clock is seconds since day 0 00:00. Nothing here calls a real model or needs a key.
"""
import email.utils, hashlib, ipaddress
from fieldkit.gateway import Response, DAY

WEEKDAYS = ["Thu", "Fri", "Sat", "Sun", "Mon", "Tue", "Wed"]


def fmt(t):
    d, s = divmod(int(t), DAY)
    return f"day {d} {WEEKDAYS[d % 7]} {s // 3600:02d}:{s % 3600 // 60:02d}"


def h01(*parts):
    """A deterministic number in [0, 1) from any parts. Used instead of a random generator."""
    return int(hashlib.sha256("|".join(map(str, parts)).encode()).hexdigest()[:8], 16) / 0x100000000


class Clock:
    def __init__(self, t=0):
        self.t = t

    def now(self):
        return self.t

    def sleep(self, s):
        self.t += s


class SecretStore:
    """The customer's secret store. The platform's rotation job writes here; readers are counted."""

    def __init__(self):
        self.value = ("key-0", "s3cr3t-0")
        self.reads = 0

    def read(self):
        self.reads += 1
        return self.value


class SimGateway:
    def __init__(self, clock, store, *, rotation_weekday=3, rotation_hour=2, grace_s=3600, start_key=0,
                 allowlist=("10.20.0.0/16",), quota_per_min=60, alias_switch_day=None,
                 v1_deprecated_day=None, v1_sunset_day=None, dilution=0.0, report_version=True,
                 default_api_version="2024-06-01", filter_every=97, rotate=True):
        self.clock, self.store = clock, store
        self.rot_wd, self.rot_h, self.grace = rotation_weekday, rotation_hour, grace_s
        self.n = start_key
        self.valid = {f"s3cr3t-{start_key}": None}       # secret -> expiry (None = current)
        self.store.value = (f"key-{start_key}", f"s3cr3t-{start_key}")
        self.next_rot = self._next_rotation(clock.now()) if rotate else float("inf")
        self.allow = [ipaddress.ip_network(c) for c in allowlist]
        self.quota, self.window = quota_per_min, {}
        self.alias_switch_day = alias_switch_day
        self.v1_dep, self.v1_sun = v1_deprecated_day, v1_sunset_day
        self.dilution, self.report_version = dilution, report_version
        self.default_api = default_api_version
        self.filter_every = filter_every
        self.log, self.denied, self.rotations, self.seq = [], 0, [], 0

    def _next_rotation(self, now):
        day = now // DAY
        while True:
            t = day * DAY + self.rot_h * 3600
            if day % 7 == self.rot_wd and t > now:
                return t
            day += 1

    def tick(self, now):
        """Run the platform's rotation job if it is due. Old secret keeps working for the grace period."""
        while now >= self.next_rot:
            t = self.next_rot
            old = f"s3cr3t-{self.n}"
            self.valid[old] = t + self.grace
            self.n += 1
            self.valid[f"s3cr3t-{self.n}"] = None
            self.store.value = (f"key-{self.n}", f"s3cr3t-{self.n}")
            self.rotations.append(t)
            self.next_rot = self._next_rotation(t)

    def served_version(self, deployment, now, seq):
        if deployment != "extract-standard":
            return {"classify-small": "small-2026-02", "reason-frontier": "frontier-2026-03"}.get(deployment, "x")
        base = "extract-2026-01"
        if self.alias_switch_day is not None and now >= self.alias_switch_day * DAY:
            base = "extract-2026-04"
        if self.dilution and h01("dilute", seq) < self.dilution:
            return "extract-2026-04-mini"
        return base

    def __call__(self, method, path, headers, body, source_ip, now):
        self.tick(now)
        self.seq += 1
        rid = f"gw-{self.seq:06d}"
        base = {"x-gw-request-id": rid}
        if not any(ipaddress.ip_address(source_ip) in n for n in self.allow):
            self.denied += 1
            return self._log(now, path, Response(403, base, {"error": "ip_not_on_allowlist"}))
        secret = headers.get("authorization", "").replace("Bearer ", "")
        exp = self.valid.get(secret, -1)
        if exp == -1 or (exp is not None and now >= exp):
            return self._log(now, path, Response(401, base, {"error": "invalid_or_expired_key"}))
        minute = now // 60
        used = self.window.get(minute, 0)
        if used >= self.quota:
            return self._log(now, path, Response(429, {**base, "retry-after": str(60 - now % 60)},
                                                 {"error": "rate_limited"}))
        self.window[minute] = used + 1
        if path.startswith("/v1/"):
            if self.v1_sun is not None and now >= self.v1_sun * DAY:
                return self._log(now, path, Response(410, base, {"error": "endpoint_retired"}))
            if self.v1_dep is not None and now >= self.v1_dep * DAY:
                base = {**base, "Deprecation": f"@{self.v1_dep * DAY}",
                        "Sunset": email.utils.formatdate(self.v1_sun * DAY, usegmt=True),
                        "Link": f'<{path.replace("/v1/", "/v2/")}>; rel="successor-version"'}
        api = headers.get("api-version", self.default_api)
        if "response_format" in body and api < "2025-01-01":
            return self._log(now, path, Response(400, base, {"error": f"unsupported_parameter: response_format (api-version {api})"}))
        dep = path.split("/")[3] if path.count("/") >= 4 else "unknown"
        doc = body.get("doc", 0)
        if dep == "reason-frontier" and self.filter_every and doc % self.filter_every == 13:
            return self._log(now, path, Response(400, base, {"error": "content_filter.violence"}))
        v = self.served_version(dep, now, self.seq)
        hdr = {**base, **({"x-gw-model-version": v} if self.report_version else {})}
        tin = 900 + int(h01("in", dep, doc) * 2200) if body.get("text") != "smoke" else 5
        tout = 120 + int(h01("out", dep, doc) * 380) if body.get("text") != "smoke" else 1
        return self._log(now, path, Response(200, hdr, {"usage": {"input_tokens": tin, "output_tokens": tout},
                                                         "version": v}))

    def _log(self, now, path, r):
        self.log.append((now, path, r.status))
        return r


# Stand-in chargeback rates per 1,000 tokens (input, output), USD. Not any provider's price list.
PRICES = {"classify-small": (0.0004, 0.0016), "extract-standard": (0.0006, 0.0024),
          "reason-frontier": (0.0050, 0.0150)}
PIPELINE = ["classify-small", "extract-standard", "reason-frontier"]
