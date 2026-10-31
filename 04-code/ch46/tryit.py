"""Try It Yourself, Chapter 46.
a: a fourth engagement misses its integration P50 by 45%. Recompute the reserve and the next insurer's fee.
b: run the Caldwell playbook's transfer check against Greystone and price the credit that survives.
c: price the Pennant phase-one package as a sole practitioner with a PI cap; under-reserve it and watch the margin.
"""
import sys
import _paths  # noqa: F401
import reserve as R
import price_next as P
import playbook as B
import independent as I


def a():
    m = R.misses({"fourth": 1.45}); r = R.reserve(m)
    print(f"misses {', '.join(f'{k} {v:.2f}' for k, v in m.items())} -> reserve {r:.0%}")
    for res in (0.35, r):
        h, _ = P.priced_hours("checked", res=res)
        rh = h["integration"] - h["integration"] / (1 + res)
        fee = P.fee_for(h, overrun=rh)
        print(f"  reserve {res:.0%}: priced {sum(h.values()):,.0f} h, reserve line {rh:,.0f} h, fee ${fee:,}")
    h35, _ = P.priced_hours("checked", res=0.35)
    fee35 = P.fee_for(h35, overrun=h35["integration"] - h35["integration"] / 1.35)
    ah, over = P.actual_hours(h35, 0.35, 1.45)
    print(f"  priced at 35%, integration lands at 1.45: margin {P.year_one(ah, fee35, over)[0]:.1%}")


def b():
    B.main("checked", "greystone")
    print(f"credit that survives at Greystone {B.credit('greystone'):,} h of {B.credit('greystone', 'naive'):,} h")


def c():
    I.main(0.0, False); I.main(0.15, False); I.main(0.35, True)


if __name__ == "__main__":
    {"a": a, "b": b, "c": c}[sys.argv[1]]()
