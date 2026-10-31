"""Three stand-in clouds for Chapter 20 (deterministic; no network, no SDKs, no keys).

Each exposes a different native call shape on purpose, because the real ones do: a gateway in front
of a managed model (Caldwell on AWS), a chat-completions deployment (Greystone on Azure) and a regional
predict endpoint (Pennant on Google Cloud). Version availability by region is stand-in data shaped like
the public pattern (a new version reaches some regions weeks after others, and some not at all). It is
not any provider's real catalog.
"""
import hashlib, json
from fieldkit.gateway import Response

FAMILY = "extract"
SKILL = {"extract-open-2026-02": 0.86, "extract-2025-10": 0.845, "extract-2026-01": 0.885, "extract-2026-04": 0.915}

# Days after a version's first release before a region offers it. None: not offered.
LAG = {
    "aws": {"us-east-1": {"extract-2025-10": 0, "extract-2026-01": 0, "extract-2026-04": 0},
            "us-west-2": {"extract-2025-10": 9, "extract-2026-01": 7, "extract-2026-04": 14}},
    "azure": {"eastus2": {"extract-2025-10": 0, "extract-2026-01": 3, "extract-2026-04": 4},
              "westus3": {"extract-2025-10": 21, "extract-2026-01": 18, "extract-2026-04": 27},
              "centralus": {"extract-2025-10": 30, "extract-2026-01": 44, "extract-2026-04": None}},
    "gcp": {"us-central1": {"extract-2025-10": 0, "extract-2026-01": 0, "extract-2026-04": 3},
            "europe-west4": {"extract-2025-10": 35, "extract-2026-01": 62, "extract-2026-04": None}},
}
NOW = 75   # days since extract-2026-04 was first released, when this chapter's deployments happen


def h01(*parts):
    return int(hashlib.sha256("|".join(map(str, parts)).encode()).hexdigest()[:8], 16) / 0x100000000


def catalog(cloud, now=NOW):
    """region -> {family: [versions offered now]} for one cloud."""
    return {region: {FAMILY: sorted(v for v, lag in vs.items() if lag is not None and lag <= now)}
            for region, vs in LAG[cloud].items()}


FIELDS = {
    "caldwell": ["policy_number", "claimant_name", "loss_date", "date_received", "loss_type",
                 "loss_location", "injury_reported", "police_report_ref", "other_party", "intake_channel"],
    "greystone": ["patient_name", "date_of_birth", "member_id", "referring_provider", "specialty",
                  "diagnosis_code", "urgency", "payer"],
    "pennant": ["shipper", "consignee", "origin", "destination", "pieces", "weight_kg", "incoterm", "ship_date"],
}
TOKENS = {"caldwell": (1450, 220), "greystone": (5200, 300), "pennant": (1100, 160)}


def items(customer, n, tag="gold"):
    return [f"{customer[0].upper()}{tag[0].upper()}{i:04d}" for i in range(n)]


def extract(customer, item, version):
    """The model stand-in: correctness depends on item difficulty and, a little, on the version."""
    out = {}
    for f in FIELDS[customer]:
        d, j = h01("d", customer, item, f), h01("j", item, f, version)
        out[f] = f"{item}:{f}" if d + 0.12 * (j - 0.5) < SKILL[version] else f"{item}:{f}?"
    return out


def tokens(customer, item):
    i, o = TOKENS[customer]
    return i + int(h01("t", item) * i * 0.6), o + int(h01("o", item) * o * 0.5)


class CallFailed(Exception):
    pass


class Network:
    """The customer's network as the workload sees it."""

    def __init__(self, private_endpoint=True, public_access=False, egress_allow=()):
        self.private_endpoint, self.public_access, self.egress_allow = private_endpoint, public_access, set(egress_allow)

    def reach(self, target):
        if target == "model-private":
            return self.private_endpoint
        if target == "model-public":
            return self.public_access
        return target in self.egress_allow


class Sinks:
    def __init__(self):
        self.customer, self.vendor = [], []


class Credentials:
    """The cloud's secret store and token service. rotate() is the platform's rotation job."""

    def __init__(self):
        self.generation = 0

    def rotate(self):
        self.generation += 1

    def current(self):
        return f"cred-{self.generation}"

    def valid(self, cred):
        return cred == self.current()


class CaldwellGateway:
    """AWS: Caldwell's gateway (Chapter 18) in front of the managed model. Dated deployments only."""

    def __init__(self, region, creds, net):
        self.region, self.creds, self.net, self.n = region, creds, net, 0
        self.cat = catalog("aws")[region][FAMILY]

    def transport(self, method, path, headers, payload, source_ip, t):
        if not self.net.reach("model-private"):
            raise CallFailed("no route to gateway")
        if not self.creds.valid(headers["authorization"].split()[-1]):
            return Response(401, {}, {"error": "invalid key"})
        dep = path.split("/")[3]
        if dep not in self.cat:
            return Response(404, {}, {"error": "deployment not found"})
        self.n += 1
        ti, to = tokens(payload["customer"], payload["item"])
        return Response(200, {"x-gw-model-version": dep, "x-gw-request-id": f"cw-{self.n:05d}"},
                        {"output": extract(payload["customer"], payload["item"], dep),
                         "usage": {"input_tokens": ti, "output_tokens": to}})


class AzureDeployments:
    """Azure: chat-completions deployments the platform team creates; a deployment name maps to a version."""

    def __init__(self, region, creds, net, deployments, current_api="2026-03-01", retired_api=("2024-06-01",)):
        self.region, self.creds, self.net, self.deps, self.n = region, creds, net, dict(deployments), 0
        self.current_api, self.retired_api = current_api, retired_api

    def chat_completions(self, deployment, api_version, body, bearer):
        if not self.net.reach("model-private"):
            raise CallFailed("private endpoint not reachable")
        if not self.creds.valid(bearer):
            raise CallFailed("401 token or key not valid")
        version = self.deps[deployment]
        self.n += 1
        ti, to = tokens("greystone", body["item"])
        hdr = {"x-request-id": f"gs-{self.n:05d}"}
        if api_version in self.retired_api:
            hdr["deprecation"] = "past-warning"
        return hdr, {"model": version, "id": f"gs-{self.n:05d}",
                     "choices": [{"message": {"content": json.dumps(extract("greystone", body["item"], version))}}],
                     "usage": {"prompt_tokens": ti, "completion_tokens": to}}


class RegionalPredict:
    """Google Cloud: a regional predict endpoint. 'model@latest' resolves to whatever the region offers."""

    def __init__(self, project, creds, net):
        self.project, self.creds, self.net, self.n = project, creds, net, 0
        self.cat = catalog("gcp")

    def predict(self, endpoint, instances, access_token):
        if not self.net.reach("model-private"):
            raise CallFailed("Private Service Connect endpoint not reachable")
        if not self.creds.valid(access_token):
            raise CallFailed("401 access token expired")
        parts = endpoint.split("/")
        region, model = parts[3], parts[-1]
        offered = self.cat[region][FAMILY]
        version = max(offered) if model.endswith("@latest") else model
        if version not in offered:
            raise CallFailed(f"404 {version} not offered in {region}")
        self.n += 1
        inst = instances[0]
        ti, to = tokens("pennant", inst["item"])
        return {"predictions": [extract("pennant", inst["item"], version)], "modelVersionId": version,
                "metadata": {"tokenMetadata": {"inputTokenCount": ti, "outputTokenCount": to}},
                "requestId": f"pn-{self.n:05d}"}
