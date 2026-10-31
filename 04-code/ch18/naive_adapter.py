"""The adapter as first written: key read once at start, every error retried the same way."""


class NaiveAdapter:
    def __init__(self, transport, read_secret, *, app_id, api_version, clock, sleep, source_ip):
        self.transport, self.clock, self.sleep, self.ip = transport, clock, sleep, source_ip
        self.key_id, self.secret = read_secret()        # read once, at process start
        self.app_id, self.api_version = app_id, api_version
        self.attempts = 0

    def call(self, deployment, payload, path=None):
        path = path or f"/v2/deployments/{deployment}/chat"
        headers = {"authorization": f"Bearer {self.secret}", "x-app-id": self.app_id,
                   "api-version": self.api_version}
        for attempt in range(4):                       # one try plus three retries, for every error
            self.attempts += 1
            r = self.transport("POST", path, headers, payload, self.ip, self.clock())
            if r.status == 200:
                return r
            self.sleep(2 ** attempt)
        raise RuntimeError(f"{deployment}: HTTP {r.status} {r.body.get('error')}")
