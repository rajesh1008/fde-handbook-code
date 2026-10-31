"""Try It Yourself, Chapter 20. Usage: python tryit.py a|b|c"""
import _paths  # noqa: F401
import sys
from adapters import ADAPTERS, Port
from deploy import check_line
from estate_configs import PENNANT_EU, BASE, CALDWELL, GREYSTONE, with_
from fieldkit.estates import ModelPin, ModelResult, resolve_pin
from sim_clouds import catalog, extract, tokens, CallFailed
import contextlib, io
with contextlib.redirect_stdout(io.StringIO()):  # the module prints its listing on import
    from cost_estate import FIXED, rows  # noqa: F401


def a():
    """Widen the EU pin's regions to include the US region and see which check catches it."""
    pin = ModelPin("extract", "extract-2026-04", ("europe-west4", "us-central1"))
    region, version = resolve_pin(pin, catalog("gcp"))
    print(f"resolve_pin with regions {pin.regions} -> {region}, {version}")
    n, failing, _, rep = check_line(with_(PENNANT_EU, region=region, pin=pin))
    print(f"deployed there: {n}/14, failing {' '.join(failing)}; accuracy {rep['accuracy']:.1%}")
    print("the pin resolved; the residency check (M1) and the policy scan (C1) are what stop it")


class LocalServer:
    """A stand-in for an inference server on the customer's own hardware: one model, OpenAI-shaped."""

    def __init__(self, creds, net):
        self.creds, self.net = creds, net

    def complete(self, model, prompt, api_key):
        if not self.net.reach("model-private"):
            raise CallFailed("no route to the plant network")
        if not self.creds.valid(api_key):
            raise CallFailed("401")
        ti, to = tokens("caldwell", prompt["item"])
        return {"model": model, "output": extract("caldwell", prompt["item"], model), "usage": [ti, to]}


class OnPrem(Port):
    """A fourth estate: the customer's own servers."""

    def __init__(self, cfg, creds, net, sinks):
        super().__init__(cfg, creds, net, sinks)
        self.svc = LocalServer(creds, net)

    def call(self, payload):
        r = self.svc.complete(self.cfg["model"], payload, self.credential())
        return ModelResult(r["output"], r["model"], r["usage"][0], r["usage"][1], self.cfg["region"])


def b():
    import inspect
    with contextlib.redirect_stdout(io.StringIO()):
        from loc import code_lines
    ADAPTERS["onprem"] = OnPrem
    cfg = with_(CALDWELL, cloud="onprem", region="plant-1", allowed_regions=("plant-1",),
                model="extract-open-2026-02", pin=ModelPin("extract", "extract-open-2026-02", ("plant-1",)))
    n, failing, _, rep = check_line(cfg)
    print(f"fourth estate adapter: {code_lines(inspect.getsource(OnPrem))} lines; "
          f"inference server stand-in {code_lines(inspect.getsource(LocalServer))} lines")
    print(f"parity {n}/14 failing {' '.join(failing) or '-'}; accuracy {rep['accuracy']:.1%} on {rep['model'] if 'model' in rep else cfg['model']}")
    print(f"Caldwell's managed estate on extract-2026-04 for comparison: {check_line(CALDWELL)[3]['accuracy']:.1%}")


def c():
    print("--- total cost per scored document by monthly volume ---")
    print("volume    " + "  ".join(f"{k.split()[0]:>10s}" for k in rows))
    for v in (1000, 2400, 5000, 11244, 20000, 50000):
        cells = [r["model"] + sum(FIXED[k.split()[0].lower()].values()) / v for k, r in rows.items()]
        print(f"{v:6d}    " + "  ".join(f"{x:10.4f}" for x in cells))


if __name__ == "__main__":
    print(f"=== exercise {sys.argv[1]} ===")
    {"a": a, "b": b, "c": c}[sys.argv[1]]()
