"""Chapters 50.3 and 50.6: deterministic spread and ratios with lineage, a stand-in drafter, the numeric gate,
the currency lint and the lineage check. Lab-local; uses fieldkit.lineage unchanged. Deterministic stand-in: the
'drafter' is a template, not a model call, so the same input gives the same draft every run."""
import re
import _paths  # noqa: F401
from fieldkit.lineage import RefTables, LineageStore
import world as W

FUNCS = {
    "dscr": lambda v: (v["ebitda"] - v["maintenance_capex"] - v["cash_taxes"]) / (v["interest"] + v["scheduled_principal"]),
    "debt_to_ebitda": lambda v: v["funded_debt"] / v["ebitda"],
    "current_ratio": lambda v: v["current_assets"] / v["current_liabilities"],
    "tnw": lambda v: v["equity"] - v["intangibles"],
}


def crossfoot(st):
    f = {k: v for k, (v, _) in st["fields"].items()}
    problems = []
    if f["total_liabilities"] + f["equity"] != f["total_assets"]:
        problems.append(f"balance sheet does not foot: liabilities {f['total_liabilities']:,} + equity "
                        f"{f['equity']:,} != assets {f['total_assets']:,}")
    if f["current_assets"] > f["total_assets"]:
        problems.append("current assets exceed total assets")
    return problems


def spread(st=W.STATEMENT):
    """Build the lineage for one statement: source, pages, extractions, calculations, covenant tests."""
    refs = RefTables()
    rdef = refs.register("harbourline-ratio-definitions", W.RATIO_DEFS, "policy rev 2026-2", "Harbourline credit policy")
    cov = refs.register("northgate-facility-covenants", {k: f"{op} {t}" for k, (op, t) in W.COVENANTS.items()},
                        "confirmed by credit officer, day 131", "Harbourline credit officer")
    store = LineageStore(refs)
    src = store.add("source", uri=st["uri"], sha256=st["sha256"], standard=st["standard"])
    pages, ext = {}, {}
    for name, (value, page) in st["fields"].items():
        if page not in pages:
            pages[page] = store.add("page", [src], page=page)
        ext[name] = store.add("extraction", [pages[page]], field=name, value=value, method="H03 table capture v4",
                              currency=st["currency"], unit=st["unit"])
    calc = {}
    for r, ins in W.INPUTS.items():
        vals = {i: st["fields"][i][0] for i in ins}
        value = round(FUNCS[r](vals), 2)
        calc[r] = store.add("calculation", [ext[i] for i in ins], function=r, value=value,
                            refs={"definition": rdef, "covenant": cov})
    return store, ext, calc


def recompute(node, store):
    vals = {store.nodes[p].attrs["field"]: store.nodes[p].attrs["value"] for p in node.parents}
    return FUNCS[node.attrs["function"]](vals)


def covenant_lines(store, calc):
    out = []
    for r, (op, t) in W.COVENANTS.items():
        v = store.nodes[calc[r]].attrs["value"]
        ok = v >= t if op == ">=" else v <= t
        head = (v - t) if op == ">=" else (t - v)
        unit = "" if r == "tnw" else "x"
        out.append((r, v, op, t, "pass" if ok else "BREACH", head, unit))
    return out


LABEL = {"dscr": "Debt service coverage", "debt_to_ebitda": "Funded debt to EBITDA", "current_ratio": "The current ratio",
         "tnw": "Tangible net worth"}


def fmt(r, v):
    return f"C${v / 1000:,.1f} million" if r == "tnw" else f"{v:.2f}x"


def draft(store, ext, calc, inject=None):
    """The stand-in drafter. Each claim is one sentence and cites the nodes its numbers came from.
    inject='model_ratio': the drafter computes DSCR itself from EBITDA and debt service (the wrong definition)
    and cites only the extracted inputs. inject='round': it rounds a correct ratio to one decimal.
    inject='unlabeled': it writes an amount without a currency."""
    n = store.nodes
    rev = n[ext["revenue"]].attrs["value"]
    claims = [(f"{W.BORROWER} reported revenue of C${rev / 1000:,.1f} million for fiscal 2025 under ASPE.", [ext["revenue"]])]
    for r in ("dscr", "debt_to_ebitda", "current_ratio", "tnw"):
        v = n[calc[r]].attrs["value"]
        claims.append((f"{LABEL[r]} is {fmt(r, v)} against a covenant of "
                       f"{W.COVENANTS[r][0]} {fmt(r, W.COVENANTS[r][1])}.", [calc[r]]))
    if inject == "model_ratio":
        e, ds = n[ext["ebitda"]].attrs["value"], n[ext["interest"]].attrs["value"] + n[ext["scheduled_principal"]].attrs["value"]
        claims[1] = (f"Debt service coverage is {e / ds:.2f}x against a covenant of >= 1.25x, comfortable headroom.",
                     [ext["ebitda"], ext["interest"], ext["scheduled_principal"]])
    elif inject == "model_calc":
        e, ds = n[ext["ebitda"]].attrs["value"], n[ext["interest"]].attrs["value"] + n[ext["scheduled_principal"]].attrs["value"]
        own = store.add("calculation", [ext[i] for i in W.INPUTS["dscr"]], function="dscr", value=round(e / ds, 2),
                        refs=dict(n[calc["dscr"]].attrs["refs"]), written_by="drafter")
        claims[1] = (f"Debt service coverage is {e / ds:.2f}x against a covenant of >= 1.25x.", [own])
    elif inject == "round":
        claims[1] = ("Debt service coverage is 1.3x against a covenant of >= 1.25x.", [calc["dscr"]])
    elif inject == "unlabeled":
        claims[0] = (f"{W.BORROWER} reported revenue of ${rev / 1000:,.1f} million for fiscal 2025 under ASPE.", [ext["revenue"]])
    return claims


NUM = re.compile(r"(C\$|US\$|\$)?(\d[\d,]*\.?\d*)\s*(x|million)?")


def numbers(text):
    out = []
    for cur, num, unit in NUM.findall(text):
        if num.strip(".") in ("2025",) or not unit:
            continue
        out.append((cur, float(num.replace(",", "")), unit))
    return out


def numeric_gate(store, claims):
    """Every ratio or amount in the draft must equal, at display precision, a value recorded in the lineage of the
    claim that states it; a covenant threshold must equal the confirmed covenant table. Deterministic; runs before
    anything reaches the credit officer."""
    problems = []
    limits = {round(t / 1000, 1) if r == "tnw" else t for r, (_, t) in W.COVENANTS.items()}
    for i, (text, parents) in enumerate(claims, 1):
        body, _, cov = text.partition("against a covenant of")
        recorded = [(node.kind, node.attrs.get("function") or node.attrs.get("field"), node.attrs["value"])
                    for p in parents for node in store.chain(p) if "value" in node.attrs]
        for cur, x, unit in numbers(body):
            ok = any((unit == "x" and kind == "calculation" and abs(round(v, 2) - x) < 1e-9) or
                     (unit == "million" and abs(round(v / 1000, 1) - x) < 1e-9) for kind, _, v in recorded)
            if not ok:
                calcs = [f"{nm} {v:.2f}" for kind, nm, v in recorded if kind == "calculation"]
                problems.append(f"claim {i}: {x:g}{unit} matches no recorded calculation "
                                f"({'; '.join(calcs) if calcs else 'the claim cites extracted inputs only'})")
        for cur, x, unit in numbers(cov):
            if not any(abs(x - t) < 1e-9 for t in limits):
                problems.append(f"claim {i}: covenant {x:g}{unit} is not in the confirmed covenant table")
    return problems


def lineage_check(store, claim_ids, rel, sources):
    """fieldkit verify on the release, then one rule per claim: a claim that states a ratio must descend from a
    calculation node, so the number was computed by code from recorded inputs and can be recomputed."""
    problems = [p for p in store.verify(rel, sources=sources, recompute=recompute)]
    for i, cid in enumerate(claim_ids, 1):
        n = store.nodes[cid]
        if any(u == "x" for _, _, u in numbers(n.attrs["text"].partition("against")[0])) and \
                "calculation" not in store.kinds_covered(cid):
            problems.append(f"claim {i} states a ratio but its chain is " + " > ".join(store.kinds_covered(cid))
                            + ": no calculation node")
    return problems


def currency_lint(claims):
    return [f"claim {i}: amount without a currency label" for i, (t, _) in enumerate(claims, 1)
            for cur, x, unit in numbers(t) if unit == "million" and cur not in ("C$", "US$")]


def release(store, claims, approved_by="credit officer (draft only)"):
    cl = [store.add("claim", ps, text=t) for t, ps in claims]
    return cl, store.add("release", cl, report="draft memo, financial analysis", approved_by=approved_by)


def check(store, claims):
    """All three deterministic checks on one draft: (numeric gate, currency lint, lineage) problem lists."""
    cl, rel = release(store, claims)
    return numeric_gate(store, claims), currency_lint(claims), lineage_check(store, cl, rel, {W.STATEMENT["uri"]: W.STATEMENT["sha256"]})
