"""Route Harbourline's 200 questions and find engineering content sent to sales alone."""
import _path  # noqa: F401
from fieldkit.bid import triage
from harbourline import questions, SECTIONS

counts, by_sec, mis = triage(questions())
print(f"Harbourline RFP: {sum(counts.values())} questions")
print("section                               eng  joint  sales")
for sec, title, *_ in SECTIONS:
    c = by_sec[sec]
    print(f"  {sec} {title:<34} {c['engineering']:>3}  {c['joint']:>5}  {c['sales']:>5}")
t = sum(counts.values())
print(f"  total                                {counts['engineering']:>3}  {counts['joint']:>5}  {counts['sales']:>5}")
print(f"engineering owns or co-signs {counts['engineering'] + counts['joint']} of {t} "
      f"({(counts['engineering'] + counts['joint']) / t:.0%})")
print(f"misrouted in week 1 (engineering content sent to sales alone): {len(mis)}")
for k, o, text in mis:
    print(f"  {k} should be {o}: {text}")
