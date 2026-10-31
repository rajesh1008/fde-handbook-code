# Chapter 6 lab: discovery as data

Deterministic stand-in for Caldwell Mutual's intake discovery, days 8 to 26. Every path, count and timing was built for the book to be consistent with the running project; every number re-runs to the same value.

| File | What it does |
|---|---|
| discovery.py | the module promoted to `fieldkit.discovery` (Note, DiscoveryLog, CoverageReport, Contradiction, Step, permission_gaps) |
| caldwell_discovery.py | the Caldwell notes, paths P01 to P11 and the 202 watched documents |
| five_questions.py | the five questions per path (Listing 6.1) |
| tracer.py | the Springfield tracer (Listing 6.2) |
| exceptions.py | exception kinds and minutes (Listing 6.3) |
| run_coverage.py | day-26 coverage report and the fortnight curve (Listing 6.6) |
| failure_interview_vs_shadow.py | failure injection: an interview that contradicts the shadowing log (Listing 6.7) |
| volumes.py | volumes, hours, cost and received-date lag (Listing 6.8) |
| permissions.py | permission gaps for the service account (Listing 6.9) |
| tryit.py | Try It Yourself a, b, c |
| test_ch06.py | ten tests |

Run `bash make_outputs.sh` with the book venv; printed output lands in `output/`.
