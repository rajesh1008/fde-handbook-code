"""Listing 6.1: the five questions asked of every path, on the evening of day 12 (deterministic stand-in)."""
from caldwell_discovery import build_log
from discovery import QUESTIONS

log = build_log()
for key, q in QUESTIONS.items():
    print(f"{key:<7} {q}")
print()
print(log.coverage(12).render())
