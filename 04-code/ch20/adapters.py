"""The only cloud-specific code in the lab: one thin adapter per estate, each implementing the five ports.

Every adapter returns the same ModelResult and writes the same log record. Nothing here decides a
version, a region or a network rule; those come from the estate's configuration, which the customer reads.
"""
import json
from fieldkit.estates import ModelResult
from fieldkit.gateway import GatewayAdapter, GatewayStop
from sim_clouds import CaldwellGateway, AzureDeployments, RegionalPredict, CallFailed


class Port:
    """Shared plumbing: the identity port, the secrets port, the log port and the network probe."""

    def __init__(self, cfg, creds, net, sinks):
        self.cfg, self.creds, self.net, self.sinks = cfg, creds, net, sinks
        self.cached = creds.current()             # what a key in an environment variable looks like

    def identity(self):
        return self.cfg["credential"]

    def credential(self):
        if self.cfg["secret_at_call"]:
            return self.creds.current()           # read from the customer's store or token service per call
        return self.cached

    def log(self, record):
        if self.cfg["log_sink"] == "customer":
            self.sinks.customer.append(record)
        elif self.cfg["log_sink"] == "vendor":     # a Northlight project or workspace: the failure L1 catches
            self.sinks.vendor.append(record)       # "none": diagnostics removed, records go nowhere

    def probe(self):
        egress_host = "pypi.org"
        return dict(private_ok=self.net.reach("model-private"), public_refused=not self.net.reach("model-public"),
                    egress_refused=not self.net.reach(egress_host))


class CaldwellAws(Port):
    """AWS at Caldwell: the Chapter 18 gateway adapter, unchanged, behind the model port."""

    def __init__(self, cfg, creds, net, sinks):
        super().__init__(cfg, creds, net, sinks)
        self.gw = CaldwellGateway(cfg["region"], creds, net)
        self.inner = GatewayAdapter(self.gw.transport, lambda: ("k", self.credential()), app_id="northlight-suite",
                                    api_version=cfg.get("api_version", "2026-03-01"), clock=lambda: 0,
                                    sleep=lambda s: None, source_ip="10.20.4.17")

    def call(self, payload):
        try:
            rec, body = self.inner.call(self.cfg["model"], payload)
        except GatewayStop as e:
            raise CallFailed(str(e))
        if rec.kind != "ok":
            raise CallFailed(rec.kind)
        return ModelResult(body["output"], rec.served_version, rec.tokens_in, rec.tokens_out,
                           self.cfg["region"], rec.request_id)


class GreystoneAzure(Port):
    """Azure at Greystone: a named deployment, a managed identity token and an explicit api-version."""

    def __init__(self, cfg, creds, net, sinks):
        super().__init__(cfg, creds, net, sinks)
        self.svc = AzureDeployments(cfg["region"], creds, net, cfg["deployments"])
        self.deprecations = 0

    def call(self, payload):
        hdr, body = self.svc.chat_completions(self.cfg["model"], self.cfg["api_version"], payload, self.credential())
        self.deprecations += hdr.get("deprecation") == "past-warning"
        u = body["usage"]
        return ModelResult(json.loads(body["choices"][0]["message"]["content"]), body["model"],
                           u["prompt_tokens"], u["completion_tokens"], self.cfg["region"], body["id"])


class PennantGcp(Port):
    """Google Cloud at Pennant: a regional endpoint inside the perimeter, a service account's short token."""

    def __init__(self, cfg, creds, net, sinks):
        super().__init__(cfg, creds, net, sinks)
        self.svc = RegionalPredict(cfg["project"], creds, net)

    def call(self, payload):
        ep = f"projects/{self.cfg['project']}/locations/{self.cfg['region']}/models/{self.cfg['model']}"
        r = self.svc.predict(ep, [payload], self.credential())
        tm = r["metadata"]["tokenMetadata"]
        return ModelResult(r["predictions"][0], r["modelVersionId"], tm["inputTokenCount"],
                           tm["outputTokenCount"], self.cfg["region"], r["requestId"])


ADAPTERS = {"aws": CaldwellAws, "azure": GreystoneAzure, "gcp": PennantGcp}
