"""Listing 44.9: what to learn, ranked by durable value = share of engagements using it x half-life (capped at 10 y)."""
import world as W
from practice import durable_value
rows = sorted(W.SKILLS, key=lambda s: -durable_value(s[1], s[2]))
print(f"{'skill':<40} {'half-life':>9} {'used':>5} {'value':>6}")
for s, hl, tr in rows:
    print(f"{s:<40} {hl:>8}y {tr:>5.0%} {durable_value(hl, tr):>6.2f}")
top = [s for s, hl, tr in rows if durable_value(hl, tr) >= 0.5]
print(f"\nvalue >= 0.50: {len(top)} skills; tool-specific skills in that group: "
      f"{sum(1 for s in top if 'framework' in s or 'model' in s or 'prompt' in s)}")
