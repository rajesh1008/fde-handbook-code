# The Forward Deployed Engineer Handbook — Companion Code

Companion code and figures for *The Forward Deployed Engineer Handbook* by Rajesh Ranjan Mahapatra.

## Layout

| Path | Contents |
|---|---|
| `04-code/fieldkit/` | The `fieldkit` package built up across the book, with its full test suite |
| `04-code/chNN/` | One folder per chapter lab: scripts, a `README.md`, `make_outputs.sh`, and the expected `output/` |
| `03-figures/chNN/` | Source and rendered figures for each chapter |

## Requirements

- Python 3.10 or later (3.11+ recommended)
- `pytest` (the only package to install; everything else is the standard library)

## Quick start

```bash
git clone https://github.com/rajesh1008/fde-handbook-code.git
cd fde-handbook-code
python -m venv .venv
source .venv/bin/activate
pip install pytest
pytest 04-code/fieldkit          # expect 274 passed

cd 04-code/ch07
PY=python ./make_outputs.sh      # regenerate output/, then compare with the chapter listings
```

Each chapter folder's README names the script behind every listing in the book.

## Data

All customer names, companies, logs, and datasets in this repository are synthetic and were created for teaching. Any resemblance to real organizations is coincidental.

## License

MIT, see [LICENSE](LICENSE).
