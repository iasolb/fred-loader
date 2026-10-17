"""What a stranger sees on PyPI, pinned so it cannot quietly regress.

Read as text, not with tomllib: the suite runs on Python 3.10, which has none.
"""

from pathlib import Path

PYPROJECT = (Path(__file__).resolve().parent.parent / "pyproject.toml").read_text(
    encoding="utf-8"
)


def test_the_pypi_page_links_back_to_the_repo():
    assert "[project.urls]" in PYPROJECT
    assert 'Repository = "https://github.com/iasolb/fred-loader"' in PYPROJECT


def test_the_pypi_page_names_the_supported_pythons():
    for version in ("3.10", "3.11", "3.12"):
        assert f'"Programming Language :: Python :: {version}"' in PYPROJECT
