"""Listing 22.2: failure injection. A bill of lading photographed with a thumb over the container number."""
import _paths  # noqa: F401
import sys
from collections import Counter
from week import feed, fx_registry
from pipeline import door, link, index, rules, bk_ref, run, grade


def thumb_doc(bk):
    s = next(s for s, b in bk.items() if b["sibling"] == s + 1 and not b["customs_hold"] and not b["late"] and s > 300)
    b = bk[s]
    d = dict(doc_id="T00001", day=126, channel="photo", kind="bill of lading", layout="L03", sender="Northgate Fabrication Ltd",
             carrier=b["carrier"], shipper="Northgate Fabrication Ltd", consignee="Pennant consignee", gross_kg=b["gross_kg"],
             container=b["container"][:6], bol_no=b["bol_no"], delivery_day=b["delivered_day"], date_conf=0.96,
             legibility=0.81, zone_conf={"container": 0.14, "bol_no": 0.93}, _ship=s, _truth={"occluded"}, _sha256="injected")
    return d, s


def trace(d, bk, fx, version, mode):
    decision, line, seen = door(d, bk, version)
    print(f"  door ({version}): {decision}" + (f"  [{line.strip()}]" if decision != "accept" else
          f"; fields seen: container {seen['container']}, bol_no {seen['bol_no']}, page confidence {d['legibility']:.2f}"))
    if decision != "accept":
        print(f"  routed: sender request + clerk read of the crop; nothing linked, nothing reconciled")
        return
    s, how = link(seen, index(bk), mode)
    if s is None:
        print(f"  N07 linkage ({mode}): {how}; routed to clerk read")
        return
    rs = rules(seen, bk[s], fx)
    print(f"  N07 linkage ({mode}): {how} -> {bk_ref(s)}" + ("" if s == d["_ship"] else f"  (true booking {bk_ref(d['_ship'])})"))
    print("  rules: " + ", ".join(f"{k} {v[0]}" for k, v in sorted(rs.items())))
    bad = [k for k, v in rs.items() if v[0] == "disagree"]
    print(f"  outcome: {'exception' if bad else 'matched'}" + ("  <- silently wrong: the true shipment now lacks a bill of lading" if not bad and s != d["_ship"] else ""))


if __name__ == "__main__":
    docs, bk = feed()
    refs, fxv = fx_registry()
    fx = refs.get(fxv)
    d, s = thumb_doc(bk)
    print(f"injected: {d['doc_id']} photo of a bill of lading for {bk_ref(s)}, thumb over container characters 7 to 11")
    print(f"  true container {bk[s]['container']}; sibling {bk_ref(s + 1)} container {bk[s + 1]['container']} on the packing list in the same message")
    print("v1, as run in the shadow week")
    trace(d, bk, fx, "pennant-qs-1.0", "first key")
    print("v2, day 133 fix")
    trace(d, bk, fx, "pennant-qs-1.1", "two keys")
    print("v1.0 with two-key linkage only (no door change)")
    trace(d, bk, fx, "pennant-qs-1.0", "two keys")
    print()
    print("occluded identifiers in the week, by version")
    for ver, mode in (("pennant-qs-1.0", "first key"), ("pennant-qs-1.1", "two keys")):
        res, _ = run(docs, bk, refs, fxv, version=ver, link_mode=mode, lineage=False)
        g = grade(docs, bk, res)
        occ = [i for i, dd in enumerate(docs) if "occluded" in dd["_truth"]]
        c = Counter(g[i] for i in occ)
        print(f"  {ver}, {mode:<9}: {len(occ)} occluded ({sum(docs[i]['channel'] == 'photo' for i in occ)} photos): "
              + ", ".join(f"{k} {v}" for k, v in sorted(c.items())))
