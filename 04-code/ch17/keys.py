"""Day 57 template against day 63 module: literal secrets in configuration, and who holds and owns each key."""
import pathlib
import _paths  # noqa: F401
from fieldkit.environment import KeyRecord, find_secrets, key_findings

HERE = pathlib.Path(__file__).resolve().parent
for name in ("template-v1.tf.json", "main.tf.json"):
    hits = find_secrets((HERE / "terraform" / name).read_text(), name)
    print(f"{name}: {len(hits)} literal secret(s)" + "".join(f"\n  line {n}: {k}" for _, n, k in hits))

v1 = [KeyRecord("gateway sandbox key", "Northlight", "Caldwell", "task environment, in the repo", 7, "runner"),
      KeyRecord("tracing ingest token", "Northlight", "Northlight", "task environment", None, "tracing library"),
      KeyRecord("results bucket key", "AWS (default key)", "AWS (default key)", "default bucket encryption", None, "results")]
v2 = [KeyRecord("gateway key", "Caldwell", "Caldwell", "Secrets Manager, written by Caldwell's rotation job", 7, "runner"),
      KeyRecord("data key", "Caldwell", "Caldwell", "KMS customer-managed key", 365, "slice, results, logs"),
      KeyRecord("claims-core access", "Caldwell", "Caldwell", "IAM database authentication, 15-minute tokens", 1,
                "svc-nl-claims-ro")]
for name, keys in (("keys v1", v1), ("keys v2", v2)):
    out = key_findings(keys, "Caldwell")
    print(f"\n{name}: {len(keys)} keys, {len(out)} findings" + "".join(f"\n  {f}" for f in out))
    if not out:
        for k in keys:
            print(f"  {k.name:20} holder {k.holder:8} rotation {k.rotation_days:>3} d  {k.store}")
