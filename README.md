# fred-loader

Readable names for FRED economic data series, returned as pandas objects.

[![PyPI version](https://img.shields.io/pypi/v/fred-loader)](https://pypi.org/project/fred-loader/)
[![Supported Python versions](https://img.shields.io/pypi/pyversions/fred-loader)](https://pypi.org/project/fred-loader/)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/iasolb/fred-loader/blob/main/LICENSE)
[![Tests](https://github.com/iasolb/fred-loader/actions/workflows/tests.yml/badge.svg)](https://github.com/iasolb/fred-loader/actions/workflows/tests.yml)

## Features

- Pull FRED series using a built-in catalog of readable series names and categories.
- Resample series to a shared pandas frequency and return the data as a pandas DataFrame.
- Save pulled data to CSV and optionally add macro scores.
- Browse and search the catalog by category, series ID, or readable name.

## Installation

```bash
pip install fred-loader
```

The FRED API requires an API key. Obtain one from the [FRED API key page](https://fred.stlouisfed.org/docs/api/api_key.html) and set it in the `FRED_API_KEY` environment variable. The package also loads environment variables from a `.env` file through `python-dotenv`; add this line to that file:

```text
FRED_API_KEY=your_api_key
```

## Quick start

```python
from fred_loader import Config, pull_fred

cfg = Config(filename="fred_master.csv", output_path="./data")
df = pull_fred(cfg)
```

`pull_fred` returns a DataFrame and writes the same data to `./data/fred_master.csv`.

## Usage

### Select series

Pass a selection of built-in category dictionaries to `Config` to pull a subset of the catalog:

```python
from fred_loader import INFLATION, LABOR, RATES, Config, pull_fred

cfg = Config(
    filename="policy_inputs.csv",
    output_path="./data",
    series={**INFLATION, **LABOR, **RATES},
)
df = pull_fred(cfg)
```

The `series` argument also accepts a FRED series ID, a category or subcategory name, a list or tuple of those values, or a custom dictionary mapping FRED IDs to `(friendly_name, native_frequency)` tuples. With `series=None`, the full built-in catalog is used.

### Configure pulls

`Config` accepts `filename` and `output_path`, along with optional pull settings:

- `start` sets the first observation date and defaults to `"1990-01-01"`.
- `resample_rule` sets the pandas resampling frequency and defaults to `"W-FRI"`.
- `mean_freqs` specifies native-frequency codes to average during resampling and defaults to `{"D"}`. Other series use the last observation in each period.
- `pi_star` and `u_star` set the inflation target and natural rate of unemployment used by the scoring layer. They default to `2.0` and `4.0`.

`pull_fred(config, apply_scores=False)` saves the output CSV under `output_path` and returns a DataFrame indexed by date. Set `apply_scores=True` to apply the scoring layer before saving and returning the DataFrame.

### Apply macro scores

The scoring functions are available independently for an existing DataFrame:

```python
from fred_loader import available_scores, list_scored_columns, score

scored = score(df)
preview = available_scores(df)
catalog = list_scored_columns()
```

`score` adds scores whose input columns are present in the DataFrame. `available_scores` reports which scores can be computed, and `list_scored_columns` returns the full score-column catalog grouped by category. The `score` function accepts `pi_star`, `u_star`, and `copy` keyword-only parameters.

### Browse the catalog

Use `available` to print the categories or the series in a category or subcategory. Use `search` to find series by ID or readable name, and `info` to print details for a series:

```python
from fred_loader import available, info, search

available()
search("inflation")
info("CPIAUCSL")
```

### Notebooks

Worked examples are available in the [research-kit notebooks](https://github.com/iasolb/research-kit/tree/main/notebooks). The `01-get-set-up` notebook demonstrates setup and plotting. The `03-two-sources-one-question` notebook combines FRED and Census data and handles differences in their time frequencies.

### Project structure

```text
src/fred_loader/
  __init__.py       # public API re-exports
  utils.py          # Config and catalog discovery
  load.py           # pull_fred entry point
  series.py         # series catalog: categories and subcategories
  macro_scores.py   # scoring layer: score, available_scores
  py.typed          # inline type annotations for type checkers
```

## Contributing

Install the development dependencies and run the test suite from the repository root:

```bash
pip install -e ".[dev]"
pytest
```

## License

This project is licensed under the MIT License. See the [LICENSE file](https://github.com/iasolb/fred-loader/blob/main/LICENSE).
