"""Cost per document, latency, monthly cost by volume and the crossover (stand-in prices, labeled)."""
import _paths  # noqa: F401
import numpy as np
from fieldkit.finetune import cost_per_doc, ServingOption, crossover

# Stand-in prices and sizes (assumptions; replace with the customer's rate card)
FR_IN, FR_OUT, FR_PIN, FR_POUT = 3600, 25, 3.00, 15.00       # prompt c06-p4: definitions, eight examples, page text
FT_IN, FT_OUT, FT_P = 1350, 2, 0.20                          # c06-ft1: page text only, one label token out
VOLUME = 14800
EXPERT_H, EXPERT_RATE, VAL_H, VAL_RATE, TRAIN_RUN = 12, 46.0, 10, 95.0, 2.10   # per quarterly retrain
own = (EXPERT_H * EXPERT_RATE + VAL_H * VAL_RATE + TRAIN_RUN) / 3
fr, ft = cost_per_doc(FR_IN, FR_OUT, FR_PIN, FR_POUT), cost_per_doc(FT_IN, FT_OUT, FT_P, FT_P)
print(f"cost per document  c06-p4 ${fr:.6f}   c06-ft1 ${ft:.6f}   ratio {fr/ft:.1f}x")
CACHED, CACHE_P = 2800, 0.30   # definitions and examples as a cached prefix at a tenth of the input price (assumption)
frc = ((FR_IN - CACHED) * FR_PIN + CACHED * CACHE_P + FR_OUT * FR_POUT) / 1e6
print(f"with prompt caching c06-p4 ${frc:.6f}   ratio {frc/ft:.1f}x  (the forty-times figure assumes no cache)")
rng = np.random.default_rng(30)
lat_fr = rng.lognormal(np.log(2.9), 0.52, 5000); lat_ft = rng.lognormal(np.log(0.31), 0.42, 5000)
for n, l in (("c06-p4", lat_fr), ("c06-ft1", lat_ft)):
    print(f"latency {n:<8} p50 {np.percentile(l, 50):.2f} s   p95 {np.percentile(l, 95):.2f} s")
print(f"ownership per month (quarterly retrain + revalidation): ${own:,.0f}")
opts = [ServingOption("frontier, prompted (c06-p4)", fr),
        ServingOption("A platform custom-model hosting, per token", ft, 0, own),
        ServingOption("B self-hosted GPU, two instances", 0.0, 2 * 0.805 * 730, own),
        ServingOption("C CPU encoder classifier", 0.0, 72.0, own)]
print()
print(f"{'option':<44}{'5,000':>9}{'14,800':>9}{'50,000':>9}{'150,000':>10}")
for o in opts:
    print(f"{o.name:<44}" + "".join(f"{o.monthly(v):>9,.0f}" if v < 1e5 else f"{o.monthly(v):>10,.0f}"
                                    for v in (5000, 14800, 50000, 150000)))
print()
for o in opts[1:]:
    x = crossover(opts[0], o)
    print(f"crossover vs prompted: {o.name:<44} {x:>9,.0f} documents/month" if x else f"{o.name}: never")
x = crossover(opts[1], opts[2])
print(f"crossover A vs B: {x:,.0f} documents/month")
print()
print(f"at Caldwell's {VOLUME:,}/month, cost alone: prompted ${opts[0].monthly(VOLUME):,.0f}, option A ${opts[1].monthly(VOLUME):,.0f}")
fewer = round((838 - 796) / 900 * VOLUME); rework = 2 / 60 * 46.0
print(f"accuracy value: {fewer} fewer misclassified documents x ${rework:.2f} rework = ${fewer * rework:,.0f}/month")
