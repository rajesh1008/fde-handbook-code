"""Listing 9.3: why a chain of model decisions loses more than any one step suggests.
Route success = product of per-step success when every step must be right and no check catches a miss.
Pure arithmetic; no model involved."""
NS = (1, 3, 5, 12)
PS = (0.99, 0.97, 0.95, 0.90)
print("route success when n steps are each decided by a model (no checks)")
print("per-step " + "".join(f"{f'n={n}':>8}" for n in NS))
for p in PS:
    print(f"{p:>8.2f} " + "".join(f"{p ** n:>8.1%}" for n in NS))
demo = 0.97 ** 12
pipe = (1 - 0.02) * (1 - 0.035) * (1 - 0.03)   # silent rates of the three checked model steps
print(f"Caldwell demo agent, 12 model-decided steps at 0.97: {demo:.1%} of documents with every step right")
print(f"Caldwell pipeline, 9 code steps + 3 checked model steps (stand-in silent rates): {pipe:.1%}")
