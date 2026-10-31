"""Listing 7.8: one bank, four audiences. What each role is asked, and how much of it is a guess going in."""
import caldwell_bank as cb

b = cb.build()
for aud in ("data owner", "security lead", "model-risk officer", "operator"):
    qs = b.for_audience(aud)
    guess = sum(q.status in ("vendor position", "proposed design", "decision required") for q in qs)
    print(f"{aud:19s} {len(qs):2d} questions  {sum(q.minutes for q in qs):5.1f} min planned  "
          f"vendor or proposed expected answers {guess:2d}  top: {max(qs, key=lambda q: q.weight()).text}")
