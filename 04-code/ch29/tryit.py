"""Try It Yourself, Chapter 29: python tryit.py a|b|c"""
import sys
import io
import contextlib
import common as C
import world as W
from fieldkit.pyramid import independence, Mutant, control_run


def a():
    """Loosen and tighten the slice rule: which verdict does the mail class get?"""
    b, p9 = W.extract("p8.3"), W.extract("p9")
    for margin, alpha in ((0.02, 0.05), (0.05, 0.01), (0.10, 0.001)):
        rows = [r for r in C.slice_table(b, p9, margin, alpha) if r["kind"] == "stratum" and r["verdict"] != "pass"]
        print(f"margin {margin:.2f} alpha {alpha}: " + (", ".join(f"{r['slice']} {r['verdict']} (p={r['p']:.1e})" for r in rows) or "all pass"))
    half = [d for d in W.gold_test() if int(d[0][3:]) % 4 == 0]
    hb, ha = W.extract("p8.3", half), W.extract("p9", half)
    rows = [r for r in C.slice_table(hb, ha) if r["kind"] == "stratum" and r["slice"] == "first notice, mail"]
    print(f"a quarter of the set ({len(half)} docs): mail class {rows[0]['verdict']} (n={rows[0]['n']}, p={rows[0]['p']:.2f})")


def b():
    """Remove one stream at a time: how many wrong fields reach the router with no stream objecting?"""
    with contextlib.redirect_stdout(io.StringIO()):
        import streams as S
    c = S.catches(False)
    base = independence(c, S.wrong)
    print(f"all six: missed {base['missed']} of {base['n']}")
    for s in c:
        r = independence({k: v for k, v in c.items() if k != s}, S.wrong)
        print(f"  without {s:20} missed {r['missed']:>3} (+{r['missed'] - base['missed']})")


def c():
    """Which control-run design flaws hide which mutants?"""
    p = C.build()
    ms = [Mutant("M07", "superseded wording retrieved", 2, lambda s: dict(s, lifecycle_filter=False)),
          Mutant("M11", "judge passes more failures", 5, lambda s: dict(s, judge_fp_rate=0.35))]
    for subset in ("first40", "stratified40"):
        for rule in ("20 docs, >3 false passes", "40 docs, TNR >= 0.80"):
            rows = control_run(p, dict(C.BASE, faith_subset=subset, judge_rule=rule), ms)
            print(f"subset {subset:12} judge rule '{rule:24}': " +
                  ", ".join(f"{r['id']} {r['status']}" + (f" at L{r['caught_at']}" if r["caught_at"] else "") for r in rows))


if __name__ == "__main__":
    dict(a=a, b=b, c=c)[sys.argv[1]]()
