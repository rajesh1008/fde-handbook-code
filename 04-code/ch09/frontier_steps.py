"""Cost per document against the number of frontier steps left in a pipeline, at a fixed 12-step length.
STAND-IN prices (costs.py). Shows that the saving follows the frontier steps, not the deterministic share."""
import costs as K
_, demo = K.demo_cost("scan")
print(f"demo agent, scanned document: {demo:.4f}")
print("frontier  det  small   $/doc   fall vs demo")
for f in range(0, 5):
    c = [12 - f - 2, 0, 2, f] if f <= 10 else None
    _, new = K.pipeline_cost(c, "scan")
    print(f"{f:>8} {c[0]:>4} {c[2]:>6} {new:>7.4f} {1 - new / demo:>8.0%}")
