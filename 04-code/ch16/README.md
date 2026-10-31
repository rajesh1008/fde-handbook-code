# Chapter 16 lab: synthetic, sampled and shadowed data

Real running Python, standard library only. No model is called: the build machine has no model keys, so the
extraction pipeline is a deterministic **extractor stand-in** (`extract_standin.py`), and Caldwell's 200 real files are
a **stand-in sample** (`standin_sample.py`) built on fieldkit's day-47 fixture manifest. Every number below is
printed by these scripts; `./make_outputs.sh` reruns all of them into `output/` and runs the tests.

| Script | Listing | What it shows |
|---|---|---|
| `synth_v1.py` | 16.1 | Synthetic v1 (600 documents, no exceptions); self-scored 94% |
| `failure_no_exceptions.py` | 16.2 | Failure injection: the same extractor on the real 200 falls to 71% |
| `claimsgen.py` | 16.3 (excerpt) | Generator: profile → structured gold record → rendered document → OCR noise |
| `represent.py` | 16.4 | Representativeness report: v1 NOT REPRESENTATIVE, v2 passes |
| `sample_plan.py` | 16.5 | Stratified 300-file gold-set plan with weights and a signed manifest |
| `shadow_tap.py` | 16.6 | Shadow tap keeps agreement and profile only; canary scan fails then passes |
| `gap_line.py` | 16.7 | The gap as a scoreboard line by slice, with the stop rule |
| `deid_attack.py` | 16.8 | Pattern scrub leaks; k-anonymity and linkage attack; v2 passes |
| `fieldkit/fieldkit/synthetic.py` (lines 1-25) | 16.9 | fieldkit v2.1 synthetic module; representativeness thresholds in the docstring |
| `tryit.py a|b|c` | Try It Yourself | Break the profile; bootstrap the sample size; choose quasi-identifiers |
| `test_ch16.py` | | The chapter's numbers as tests |

fieldkit v2.1 additions (in `04-code/fieldkit/fieldkit/`): `synthetic.py`, `deid.py`, `shadow.py`, `sampling.py`,
tested by `tests/test_v21_ch16.py`. The package version string is unchanged (0.1.0).
