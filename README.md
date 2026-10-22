# fred-loader
Readable names for FRED economic data series, returned as pandas DataFrames.

[![PyPI version](https://img.shields.io/pypi/v/fred-loader)](https://pypi.org/project/fred-loader/)
[![Python versions](https://img.shields.io/pypi/pyversions/fred-loader)](https://pypi.org/project/fred-loader/)
[![MIT License](https://img.shields.io/pypi/l/fred-loader)](https://opensource.org/licenses/MIT)
[![Tests](https://github.com/iasolb/fred-loader/actions/workflows/tests.yml/badge.svg)](https://github.com/iasolb/fred-loader/actions/workflows/tests.yml)

## Features

- Retrieve multiple FRED series in a single pull and align to a common frequency
- Optional macro scoring layer that derives scores and indicators
- Built in catalog of categories and subcategories for easy discovery
- Simple API surface: pull_fred, Config, and exported series
- Output a single CSV per run for reproducibility
- Typed interfaces and helpful error messages

## Installation

```
pip install fred-loader
```

### API key

```
export FRED_API_KEY=YOUR_API_KEY
```

Alternatively, place a .env file in the project root with the line:

```
FRED_API_KEY=YOUR_API_KEY
```

## Quick start
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

## Usage
- The library exposes a catalog of categories and subcategories via module exports.
- Central entry point is pull_fred(config, apply_scores=False) which returns a pandas DataFrame.
- The Config object controls the output path, start date, resampling rule, and which series to include.
- The internal catalog (ALL_SERIES, CATEGORIES, SUBCATEGORIES) can be browsed via available(), search(), and info() helpers.

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

## Documentation

Worked notebooks are available at https://github.com/iasolb/research-kit/tree/main/notebooks.

## Contributing

```
pip install -e ".[dev]"
pytest
```

## License

https://github.com/iasolb/fred-loader/blob/main/LICENSE
