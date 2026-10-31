"""Listing 33.5: the model-risk pack generated from the evaluation suite (v1, as first submitted on day 140)."""
import sys
from world import M, DESIGNS, CALDWELL, EVIDENCE, METRICS_V1, METRICS_V2


def build(version="v1"):
    cl = M.classify_all(CALDWELL, DESIGNS[153])
    return M.Pack("Caldwell Mutual", version, cl, EVIDENCE, METRICS_V1 if version == "v1" else METRICS_V2)


def render(p):
    out = [f"# Model-risk pack {p.version}, Caldwell Mutual claims intake", ""]
    for k in p.classes:
        if k.outcome in (M.NOT_MODEL,):
            continue
        out.append(f"## {k.cid}: {k.outcome}")
        for item in M.PLAN[k.outcome]:
            for e in p.find(k.cid, item):
                out.append(f"- {item}: {e.claim} (measured by {e.measured_by}, on {e.on}; {e.source})")
        out.append("")
    out.append("## Monitoring")
    for m in p.metrics:
        out.append(f"- {m.mid} {m.name}; threshold {m.threshold}; read by {m.owner}; covers {', '.join(m.covers)}")
    return "\n".join(out) + "\n"


if __name__ == "__main__":
    v = sys.argv[1] if len(sys.argv) > 1 else "v1"
    p = build(v)
    print(f"pack {v}: {len(p.classes)} components, {p.items()} plan items, {len(p.evidence)} evidence records, "
          f"{len(p.metrics)} monitoring metrics")
    by = {}
    for k in p.classes:
        by.setdefault(k.outcome, []).append(k.cid)
    for o, ids in by.items():
        print(f"  {o:<26} {len(M.PLAN[o]):>2} items each: {', '.join(ids)}")
    print(f"  gaps: {len(p.gaps())}   lint problems: {len(p.lint())}")
    print(f"  evidence measured by: {', '.join(sorted({e.measured_by for e in p.evidence}))}")
    open(f"output/pack_{v}.md", "w").write(render(p))
    print(f"  written: output/pack_{v}.md ({len(render(p).splitlines())} lines)")
