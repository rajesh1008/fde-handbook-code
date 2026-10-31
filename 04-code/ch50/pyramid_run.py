"""Listing 50.4: the draft as a system under test, through the fieldkit pyramid (layers 1 to 4), clean and injected.
Run without stopping so the reader sees which layers catch each injection independently."""
import _paths  # noqa: F401
from fieldkit.pyramid import Layer, Pyramid, caught_at, PASS, FAIL, LAYER_NAMES
import memo, boundary

LAYERS = [Layer(1, "unit", "every number and currency in the draft", "every change", 0.1, 0.0),
          Layer(2, "component", "every claim's lineage, recomputed", "every change", 0.5, 0.0),
          Layer(3, "integration", "the release boundary holds", "every change", 0.5, 0.0),
          Layer(4, "system", "covenant results match the officer-confirmed set", "every release", 1.0, 0.0)]


def run(mode):
    store, ext, calc = memo.spread()
    claims = memo.draft(store, ext, calc, inject=None if mode == "clean" else mode)
    g, c, lin = memo.check(store, claims)
    return dict(store=store, calc=calc, g=g, c=c, lin=lin)


def l1(s):
    p = s["g"] + s["c"]
    return (FAIL if p else PASS), "; ".join(p) or "every number matches a calculation; every amount labeled", 0, 0, {}


def l2(s):
    return (FAIL if s["lin"] else PASS), "; ".join(s["lin"]) or "every claim descends from a recomputed calculation", 0, 0, {}


def l3(s):
    b = boundary.release_one()
    ok_d, _ = b.check("draft_memo", "production"); ok_w, why = b.check("write_origination", "production")
    good = ok_d and not ok_w
    return (PASS if good else FAIL), f"draft allowed; write {why}", 0, 0, {}


def l4(s):
    res = [r[4] for r in memo.covenant_lines(s["store"], s["calc"])]
    want = ["pass", "pass", "pass", "pass"]
    return (PASS if res == want else FAIL), f"{res.count('pass')} of 4 covenant results match", 0, 0, {}


pyr = Pyramid(LAYERS).add(1, "numeric gate", l1).add(2, "lineage", l2).add(3, "boundary", l3).add(4, "covenants", l4)
if __name__ == "__main__":
    for mode, name in (("clean", "clean draft"), ("model_ratio", "drafter computes DSCR in the prose (failure injection)"),
                       ("model_calc", "drafter records its own DSCR calculation (failure injection)"),
                       ("unlabeled", "amount without a currency (failure injection)")):
        res = pyr.run(run(mode), stop_on_fail=False)
        at = caught_at(res)
        print(f"{name}: " + (f"caught at layer {at} ({LAYER_NAMES[at]})" if at else "passes layers 1 to 4"))
        for r in res:
            print(f"  L{r.layer} {r.check:<13}{r.verdict:<6} {r.detail}")
