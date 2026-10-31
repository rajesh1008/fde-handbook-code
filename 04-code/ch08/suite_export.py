"""What the evaluation suite enforces: the signed criteria, exported as configuration (deterministic stand-in).
The evaluation suite reads this file and nothing else; a criterion the lint rejects is not exported."""
import json, pathlib
from caldwell_scope import signed

doc = signed()
cfg = doc.suite_config()
out = pathlib.Path(__file__).parent / "output" / "suite_config.json"
out.write_text(json.dumps(cfg, indent=1))
print(f"wrote {out.name}: {len(cfg)} criteria")
for c in cfg:
    print(f"  {c['key']}  n={c['n']:<5} {c['threshold']:<10} scorer {c['scorer']:<16} report: {'; '.join(c['report'])}")
