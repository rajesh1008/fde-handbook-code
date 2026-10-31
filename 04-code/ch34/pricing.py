"""Listing 34.7: fixed price versus time and materials when the integration tax is unknown."""
import random
import _paths  # noqa: F401
from fieldkit.contract import services_net
import world as W

# Pre-production work from the Ch2 field estimates; integration hours = model hours x tax.
# Tax ranges are triangular (low, mode, high) around the Ch10 measured taxes; ranges are stand-ins.
CUST = {
    "Caldwell": dict(other=220 + 260 + 380 + 200, model=700, tax=(0.60, 0.84, 1.40), billing="fixed", fee=200_000),
    "Greystone": dict(other=260 + 420 + 560 + 240, model=900, tax=(1.00, 1.40, 2.40), billing="tm", cap=450_000),
    "Pennant": dict(other=200 + 160 + 200 + 160, model=500, tax=(2.00, 3.00, 4.50), billing="fixed", fee=120_000),
}


def draws(c, n=10_000, seed=34):
    rnd = random.Random(seed)
    lo, mode, hi = c["tax"]
    return sorted(c["other"] + c["model"] * (1 + 0) * rnd.triangular(lo, hi, mode) + c["model"] for _ in range(n))


def q(xs, p):
    return xs[int(p * (len(xs) - 1))]


def main():
    print("SERVICES NET BY CONTRACT FORM  (loaded $150/h; T&M bill rate $260/h; 10,000 seeded draws of the tax)")
    print("  customer   form        P50 h   P90 h   P90/P50   net at P50     net at P90     who carries the tail")
    for name, c in CUST.items():
        h = draws(c)
        p50, p90 = q(h, 0.5), q(h, 0.9)
        kw = dict(fee=c.get("fee", 0), bill_rate=W.BILL_RATE, cap=c.get("cap"))
        n50 = services_net(p50, W.LOADED_RATE, c["billing"], **kw)
        n90 = services_net(p90, W.LOADED_RATE, c["billing"], **kw)
        who = "Northlight" if c["billing"] == "fixed" else ("Greystone to the cap, then Northlight")
        form = "fixed" if c["billing"] == "fixed" else "T&M + cap"
        print(f"  {name:10} {form:10} {p50:7,.0f} {p90:7,.0f}   {p90 / p50:6.2f}   ${n50:>11,.0f}   ${n90:>11,.0f}   {who}")
    print("\nBREAKEVEN AND CAP POINTS")
    print(f"  Caldwell fixed $200,000 covers {200_000 / W.LOADED_RATE:,.0f} h; Pennant fixed $120,000 covers "
          f"{120_000 / W.LOADED_RATE:,.0f} h")
    print(f"  Greystone cap $450,000 is reached at {450_000 / W.BILL_RATE:,.0f} billable h; past that each hour "
          f"costs Northlight $150 and earns nothing")
    print("\nTHE SAME WORK, PRICED THREE WAYS  (Pennant, tax unknown between 2.0 and 4.5)")
    c = CUST["Pennant"]
    h = draws(c)
    p50, p90 = q(h, 0.5), q(h, 0.9)
    disc = 160
    for label, f in [("fixed $120,000", lambda x: services_net(x, 150, "fixed", fee=120_000)),
                     ("T&M at $260, no cap", lambda x: services_net(x, 150, "tm", bill_rate=260)),
                     ("phased: T&M discovery 160 h, then fixed at P90 x $260",
                      lambda x: services_net(disc, 150, "tm", bill_rate=260) +
                      services_net(x - disc, 150, "fixed", fee=(p90 - disc) * 260))]:
        vals = [f(x) for x in h]
        loss = sum(v < 0 for v in vals) / len(vals)
        print(f"  {label:54} net P50 ${f(p50):>10,.0f}  P90 ${f(p90):>10,.0f}  P(loss) {loss:5.1%}  "
              f"customer pays P50 ${f(p50) + 150 * p50:>9,.0f}")


if __name__ == "__main__":
    main()
