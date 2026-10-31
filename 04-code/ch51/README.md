# Chapter 51 lab: a linter for fieldkit engagements

**Deterministic stand-in.** The manifests in `world.py` are typed from facts the earlier chapters recorded
(chapter and day beside each). No live system is read; rerunning gives byte-identical output.

- `catalog.py`: fifteen pattern and anti-pattern pairs, R01 to R15, with the story that exposed each.
- `linter.py`: one rule per pair. `gated=False` is v0, kept for the failure injection.
- `lint_run.py`: v0 and v1 over the fifteen stories and the injected case (Greystone's day-2 map, no operator).
- `audit.py`: the four engagements audited for the Scoreboard.
- `tryit.py a|b|c`: the three Try It Yourself exercises.
- `make_outputs.sh`: regenerates `output/` and runs `test_ch51.py` with the fieldkit suite (fieldkit unchanged, 0.1.0).

Uses fieldkit as it stands (`gates.wilson`, `scoping.RANK`, `playbooks.lint_engagement`) and the Chapter 11 lab.
