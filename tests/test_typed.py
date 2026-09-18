import pathlib
import sys


def _classifier_declared(pyproject: pathlib.Path, classifier: str) -> bool:
    """Is this classifier declared in pyproject.toml?

    `tomllib` IS STDLIB ONLY FROM 3.11 and this package supports >=3.10, so a
    bare `import tomllib` failed COLLECTION on the oldest Python it claims to
    support. Measured on CI 2026-09-17: 3.11 green, 3.10 red with
    `ModuleNotFoundError: No module named 'tomllib'`, and because the publish
    job is gated on the tests, the release never ran at all. The old comment
    here said "Python 3.13+ includes tomllib", which is true and not the point:
    what matters is the OLDEST version supported, not the newest.

    On 3.10 this asserts against the file TEXT rather than skipping. A skipped
    test here would read as green while asserting nothing.
    """
    if sys.version_info >= (3, 11):
        import tomllib

        with pyproject.open("rb") as fh:
            data = tomllib.load(fh)
        return classifier in data.get("project", {}).get("classifiers", [])
    return classifier in pyproject.read_text(encoding="utf-8")


def _repo_root() -> pathlib.Path:
    # This test file lives under tests/. The repo root is one level up.
    return pathlib.Path(__file__).resolve().parents[1]

def test_classifier_declared_and_pytyped_marker_exists():
    root = _repo_root()

    # 1) The classifier is declared in pyproject.toml
    pyproject = root / "pyproject.toml"
    assert pyproject.exists(), f"pyproject.toml not found at {pyproject}"
    assert _classifier_declared(pyproject, "Typing :: Typed"), (
        "Classifier 'Typing :: Typed' not found in [project] classifiers in pyproject.toml"
    )

    # 2) The py.typed marker is actually shipped
    pytyped_path = root / "src" / "fred_loader" / "py.typed"
    assert pytyped_path.exists(), (
        f"py.typed marker not found at {pytyped_path} - the package must ship typings"
    )
