# Chapter 21 lab: data readiness, quality scoring and lineage

Deterministic stand-in: 2,000 synthetic Pennant documents (41 layouts, five kinds, eleven countries) with defects injected at known rates. Run `bash 04-code/ch21/make_outputs.sh` from the project root with `/workspace/books/.venv`; every file in `output/` is regenerated from fixed seeds.

| Listing | File | Output | What it shows |
|---|---|---|---|
| 21.1 | register.py | output/register.txt | six-source register, findings, use checks; weight 48.8% vs 1.7% |
| 21.2 | variability.py | output/variability.txt | top 12 of 41 layouts = 76.0%; one parser silently misreads 918 amounts |
| 21.3 | scorer.py, checks.py | output/scorer.txt | held 11.1%, 0 clean held; exceptions 372 to 230 (minus 38%) |
| 21.4 | ask_vs_guess.py | output/ask_vs_guess.txt | guessing currency wrong on 36 of 140; asking 0 wrong |
| 21.5 | lineage_break.py | output/lineage_broken.txt, lineage_fixed.txt | FX table cited by path; day-81 recompute 397.70 vs 412.50; fixed chain |
| 21.6 | reconstruct.py | output/reconstruct.txt | about 240 min (impossible step) vs about 4 min |
| 21.7 | retrofit.py | output/retrofit.txt | lineage start day vs hours and unrecoverable outputs |
| WED box | granularity.py | output/granularity.txt | every output 40/40, decisions only 24/40 |
| 21.8 | ../fieldkit/fieldkit/lineage.py, test_ch21.py | output/tests.txt | 3 lab tests, 111 fieldkit tests |
| Try It a, b, c | tryit.py | output/tryit_a.txt, tryit_b.txt, tryit_c.txt | gate sweep; mean vs weakest dimension; broken sources |

Fixture data: pennant.py (documents), checks.py (scorer pennant-qs-1.0). fieldkit v2.6 (book layer; package 0.1.0): `fieldkit/quality.py`, `fieldkit/lineage.py`, tests in `fieldkit/tests/test_v26_ch21.py`.
