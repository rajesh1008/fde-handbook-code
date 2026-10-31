"""Lineage chain from the first commit (fieldkit v2.6, Chapter 21; Signature 10).

Every output carries a chain:
  source document -> page -> extraction method -> calculation -> claim -> release
Nodes are content-addressed, so the id changes if anything about the node changes.
Reference tables (currency rates, rate cards, code lists) are stored by content
hash in RefTables; a calculation that cites a reference by path instead of by
version is the classic break, because the path will hold different numbers later.
"""
import hashlib
import json
from dataclasses import dataclass, field

KINDS = ("source", "page", "extraction", "calculation", "claim", "release")


def digest(obj) -> str:
    return hashlib.sha256(json.dumps(obj, sort_keys=True, default=str).encode()).hexdigest()[:12]


class RefTables:
    """Versioned reference tables. A version id is name@content-hash."""

    def __init__(self):
        self._v = {}

    def register(self, name: str, rows: dict, as_of: str, owner: str) -> str:
        vid = f"{name}@{digest(rows)}"
        self._v[vid] = {"rows": dict(rows), "as_of": as_of, "owner": owner}
        return vid

    def get(self, vid: str) -> dict:
        return dict(self._v[vid]["rows"])

    def meta(self, vid: str) -> dict:
        m = self._v[vid]
        return {"as_of": m["as_of"], "owner": m["owner"]}

    def __contains__(self, vid):
        return vid in self._v

    def __len__(self):
        return len(self._v)


@dataclass
class Node:
    id: str
    kind: str
    attrs: dict
    parents: tuple = field(default_factory=tuple)


class LineageStore:
    def __init__(self, refs: RefTables = None):
        self.nodes = {}
        self.refs = refs

    def add(self, kind: str, parents=(), **attrs) -> str:
        if kind not in KINDS:
            raise ValueError(f"unknown kind {kind}")
        k = KINDS.index(kind)
        for p in parents:
            if p not in self.nodes:
                raise KeyError(f"parent {p} not recorded")
            pk = KINDS.index(self.nodes[p].kind)
            if not (pk < k or (kind == "calculation" and pk == k)):
                raise ValueError(f"{kind} cannot descend from {self.nodes[p].kind}")
        nid = f"{kind}:{digest([kind, attrs, sorted(parents)])}"
        self.nodes[nid] = Node(nid, kind, dict(attrs), tuple(parents))
        return nid

    def chain(self, nid: str):
        seen, todo = {}, [nid]
        while todo:
            n = self.nodes[todo.pop()]
            if n.id in seen:
                continue
            seen[n.id] = n
            todo.extend(n.parents)
        return sorted(seen.values(), key=lambda n: (KINDS.index(n.kind), n.id))

    def kinds_covered(self, nid: str):
        return [k for k in KINDS if any(n.kind == k for n in self.chain(nid))]

    def verify(self, nid: str, sources: dict = None, recompute=None):
        """Return a list of problems; an empty list means the chain holds.

        sources:   uri -> current sha256 of the stored document (detects edits)
        recompute: fn(node, store) -> value, run for every calculation node
        """
        problems = []
        missing = [k for k in KINDS if k not in self.kinds_covered(nid)]
        if missing and self.nodes[nid].kind == "release":
            problems.append("chain is missing " + ", ".join(missing))
        for n in self.chain(nid):
            if n.kind == "source" and sources is not None:
                now = sources.get(n.attrs.get("uri"))
                if now is None:
                    problems.append(f"{n.id}: source no longer retained")
                elif now != n.attrs.get("sha256"):
                    problems.append(f"{n.id}: source changed since extraction")
            if n.kind == "calculation":
                for name, ref in sorted(n.attrs.get("refs", {}).items()):
                    if "@" not in ref:
                        problems.append(f"{n.id}: reference '{name}' cited by path ({ref}), not by version")
                    elif self.refs is not None and ref not in self.refs:
                        problems.append(f"{n.id}: reference version {ref} not retained")
                if recompute is not None:
                    try:
                        value = recompute(n, self)
                    except KeyError as e:
                        problems.append(f"{n.id}: cannot recompute ({e})")
                    else:
                        if round(value, 2) != round(n.attrs.get("value"), 2):
                            problems.append(f"{n.id}: recomputed {value:,.2f}, recorded {n.attrs.get('value'):,.2f}")
        return problems

    def explain(self, nid: str):
        out = []
        for n in self.chain(nid):
            keys = [k for k in ("uri", "page", "method", "function", "text", "report", "value", "approved_by") if k in n.attrs]
            desc = ", ".join(f"{k}={n.attrs[k]}" for k in keys)
            refs = n.attrs.get("refs")
            if refs:
                desc += ", refs=" + ", ".join(f"{a}:{b}" for a, b in sorted(refs.items()))
            out.append(f"{n.kind:<11} {n.id.split(':')[1]}  {desc}")
        return out

    def size_bytes(self) -> int:
        return sum(len(json.dumps([n.kind, n.attrs, n.parents], default=str)) for n in self.nodes.values())
