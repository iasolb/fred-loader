"""Printed output must never crash a stream that is not UTF-8.

A Windows script whose stdout is piped or redirected writes cp1252. The pull
loop printed check marks and arrows there and raised UnicodeEncodeError inside
pull_all after the data had already arrived, so a successful pull read as a
crash (2026-10-17). Each test runs its call under a strict cp1252 stdout,
which is what that script sees. The swap happens inside the test body because
pytest re-installs its own capture stream after fixture setup.

Offline: the client is faked by patching ``fred_loader.utils.Fred``.
"""
from __future__ import annotations

import io
from contextlib import contextmanager, redirect_stdout
from unittest.mock import MagicMock, patch

import pandas as pd

import fred_loader.utils as utils
from fred_loader.load import pull_fred
from fred_loader.utils import Config, available


class _Cp1252Out:
    def __init__(self):
        self.raw = io.BytesIO()
        self.stream = io.TextIOWrapper(
            self.raw, encoding="cp1252", errors="strict", newline="\n"
        )

    def text(self) -> str:
        self.stream.flush()
        return self.raw.getvalue().decode("cp1252")


@contextmanager
def cp1252_stdout():
    out = _Cp1252Out()
    with redirect_stdout(out.stream):
        yield out


def test_say_degrades_a_character_the_stream_cannot_encode():
    with cp1252_stdout() as out:
        utils._say("before ✓ after")
    assert out.text() == "before ? after\n"


def test_a_pull_with_a_failure_prints_cleanly_to_cp1252(tmp_path):
    def _get(series_id, observation_start=None):
        if series_id == "BAD_ID":
            raise RuntimeError("upstream said → no")
        return pd.Series(
            [1.0, 2.0, 3.0],
            index=pd.DatetimeIndex(pd.date_range("2020-01-01", periods=3, freq="MS")),
        )

    mock_fred = MagicMock()
    mock_fred.get_series.side_effect = _get
    cfg = Config(
        filename="enc.csv",
        output_path=tmp_path,
        start="2020-01-01",
        series={"GOOD_ID": ("Good Series", "M"), "BAD_ID": ("Bad Series", "M")},
    )

    with patch("fred_loader.utils.Fred", return_value=mock_fred), \
         patch("fred_loader.utils.time.sleep"), \
         cp1252_stdout() as out:
        df = pull_fred(cfg, apply_scores=False)

    assert list(df.columns) == ["Good Series"]
    text = out.text()
    assert "ok   Good Series" in text
    assert "FAIL Bad Series" in text
    assert "upstream said ? no" in text
    assert "Saved -> " in text


def test_available_prints_cleanly_to_cp1252():
    with cp1252_stdout() as out:
        available()
    assert "TOTAL" in out.text()
