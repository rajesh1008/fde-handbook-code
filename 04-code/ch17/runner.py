"""How two builds of the shadow runner image resolve their configuration (a stand-in for the real image)."""
from urllib.parse import urlparse

PROVIDER_DEFAULT = "https://api.model-provider.example/v1"
TRACE_DEFAULT = "https://ingest.trace-vendor.example"


def resolve(image, env):
    """Image 0.9 came from the demo template: it read LLM_BASE_URL, fell back to the provider, and shipped traces
    to a vendor service unless told not to. Image 0.9.1 reads MODEL_BASE_URL, refuses to start without it, and
    exports traces only to an endpoint the deployer names."""
    if image == "0.9":
        base = env.get("LLM_BASE_URL", PROVIDER_DEFAULT)
        trace = None if env.get("OTEL_SDK_DISABLED") == "true" else env.get("OTEL_ENDPOINT", TRACE_DEFAULT)
    else:
        if "MODEL_BASE_URL" not in env:
            raise SystemExit("refusing to start: MODEL_BASE_URL not set")
        base = env["MODEL_BASE_URL"]
        t = env.get("TRACING", "off")
        trace = None if t == "off" else t
    return urlparse(base).hostname, (urlparse(trace).hostname if trace else None)
