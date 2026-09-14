import pathlib
import sys

def _repo_root() -> pathlib.Path:
    # This test file lives under tests/. The repo root is one level up.
    return pathlib.Path(__file__).resolve().parents[1]

def test_classifier_declared_and_pytyped_marker_exists():
    root = _repo_root()

    # 1) The classifier is declared in pyproject.toml
    pyproject = root / "pyproject.toml"
    assert pyproject.exists(), f"pyproject.toml not found at {pyproject}"
    import tomllib  # Python 3.13+ includes tomllib
    with pyproject.open("rb") as f:
        data = tomllib.load(f)
    classifiers = data.get("project", {}).get("classifiers", [])
    assert "Typing :: Typed" in classifiers, (
        "Classifier 'Typing :: Typed' not found in [project] classifiers in pyproject.toml"
    )

    # 2) The py.typed marker is actually shipped
    pytyped_path = root / "src" / "fred_loader" / "py.typed"
    assert pytyped_path.exists(), (
        f"py.typed marker not found at {pytyped_path} - the package must ship typings"
    )
