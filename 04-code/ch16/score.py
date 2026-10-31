"""Field-level scoring against gold values: a field is correct when the normalized strings match (None == None)."""
from claimsgen import FIELDS


def norm(v):
    return None if v is None else " ".join(str(v).split()).lower()


def score(docs, outputs):
    per_field = {f: [0, 0] for f in FIELDS}
    per_tag, per_doc = {}, []
    for d, o in zip(docs, outputs):
        ok = 0
        for f in FIELDS:
            c = norm(o.get(f)) == norm(d["gold"].get(f))
            per_field[f][0] += c
            per_field[f][1] += 1
            ok += c
        per_doc.append(ok / len(FIELDS))
        for t in d["tags"] or ["no exception"]:
            a = per_tag.setdefault(t, [0, 0])
            a[0] += ok
            a[1] += len(FIELDS)
    total = sum(v[0] for v in per_field.values()), sum(v[1] for v in per_field.values())
    return dict(accuracy=total[0] / total[1], correct=total[0], fields=total[1], per_field=per_field,
                per_tag=per_tag, per_doc=per_doc)
