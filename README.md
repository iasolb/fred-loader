# FRED_Loader

A Python wrapper around the Federal Reserve FRED API that abstracts away
series IDs, resampling rules, and macro scoring behind a clean,
human-readable interface. Installs as `fred-loader`, for anyone who pulls
macroeconomic data into pandas.

## Install

```bash
pip install fred-loader
```

Or from a checkout of this repository: `pip install -e .`.

## Quickstart

```python
from fred_loader import Config, pull_fred

cfg = Config(filename="fred_master.csv", output_path="./data")
df = pull_fred(cfg)
```

Cherry-pick series categories:

```python
from fred_loader import INFLATION, LABOR, RATES, Config, pull_fred

cfg = Config(
    filename="policy_inputs.csv",
    output_path="./data",
    series={**INFLATION, **LABOR, **RATES},
)
df = pull_fred(cfg)
```

## Learning it

Worked notebooks live in
[research-kit/notebooks](https://github.com/iasolb/research-kit/tree/main/notebooks),
alongside `census-loader` and `otter`, because the examples worth reading use
this library with the others rather than on its own.

`01-get-set-up` assumes you have seen pandas once and gets you from nothing to
a chart of something true. `03-two-sources-one-question` puts FRED and Census
data in one model and deals with the fact that they disagree about time.

They replaced a demo notebook that showed the library working. These show a
piece of work, and the library happens to be how it gets done.

## Project structure

```
src/fred_loader/
  __init__.py       # public API re-exports
  utils.py          # Config
  load.py           # pull_fred entry point
  series.py         # series catalog: categories and subcategories
  macro_scores.py   # scoring layer: score, available_scores
  py.typed          # PEP 561: ships the inline annotations to type checkers
```
