"""Five-move check on a spoken answer. Usage: python moves.py weak|strong"""
import sys
import _paths  # noqa: F401
import world as W
from fieldkit.hiring import five_moves, MOVES

m = five_moves(W.ANSWERS[sys.argv[1]])
print(f"answer {sys.argv[1]} ({len(W.ANSWERS[sys.argv[1]].split())} words): " +
      "  ".join(f"{k} {'yes' if m[k] else 'NO'}" for k in MOVES) + f"  -> {sum(m.values())} of 5")
