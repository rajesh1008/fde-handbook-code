"""Listing 34.3: one accuracy clause, four readings already in the engagement record."""
import _paths  # noqa: F401
import world as W

print("CA-01 v3: 'Northlight warrants that the System will be 98% accurate, as determined by Caldwell.'")
print("  reading                                        value   vs 98%   source")
for r, v, src in W.READINGS:
    print(f"  {r:45} {v:5.1f}%   {'met   ' if v >= 98 else 'missed'}   {src}")
met = sum(v >= 98 for _, v, _ in W.READINGS)
print(f"  {met} of {len(W.READINGS)} readings meet the clause; the clause does not say which reading counts, and "
      f"'as determined by Caldwell' gives Caldwell the choice")
print("  missing to compute it the same way twice: unit, scorer, sample (window only in the credit sentence)")
