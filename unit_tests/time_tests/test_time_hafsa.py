"""Unit tests for the time module of humanize (Hafsa).

Function covered: naturaldelta.
Test ids (ND-01a, ND-09c ...) match assignment_docs/notes_time.md.
Note: the folder is called time_tests so it does not clash with Python's own time module.
"""
import csv
from datetime import timedelta
from pathlib import Path

import humanize
import pytest

DATA_DIR = Path(__file__).resolve().parents[2] / "test_data"


def load_csv(name):
    """Read (input, expected) pairs from a CSV file in test_data."""
    with open(DATA_DIR / name, newline="", encoding="utf-8") as f:
        return [(int(row["input"]), row["expected"]) for row in csv.DictReader(f)]


def secs(n):
    return timedelta(seconds=n)


def days(n):
    return timedelta(days=n)


# =====================================================================
# naturaldelta
# =====================================================================
@pytest.mark.smoke
@pytest.mark.ecp
@pytest.mark.parametrize("value, expected", [
    pytest.param(secs(0), "a moment", id="ND-01a"),
    pytest.param(secs(1), "a second", id="ND-01b"),
    pytest.param(secs(2), "2 seconds", id="ND-01c"),
    pytest.param(secs(30), "30 seconds", id="ND-01d"),
    pytest.param(secs(60), "a minute", id="ND-02a"),
    pytest.param(secs(90), "a minute", id="ND-02b"),
    pytest.param(secs(120), "2 minutes", id="ND-02c"),
    pytest.param(secs(3600), "an hour", id="ND-02d"),
    pytest.param(secs(7200), "2 hours", id="ND-02e"),
])
def test_naturaldelta_ecp_seconds_minutes_hours(value, expected):
    assert humanize.naturaldelta(value) == expected


@pytest.mark.ecp
@pytest.mark.parametrize("value, expected", [
    pytest.param(days(1), "a day", id="ND-03a"),
    pytest.param(days(2), "2 days", id="ND-03b"),
    pytest.param(days(7), "7 days", id="ND-03c"),
    pytest.param(days(31), "a month", id="ND-03d"),
    pytest.param(days(60), "a month", id="ND-03e"),
    pytest.param(days(365), "a year", id="ND-03f"),
    pytest.param(days(730), "2 years", id="ND-03g"),
    pytest.param(days(1825), "5 years", id="ND-03h"),
])
def test_naturaldelta_ecp_days_months_years(value, expected):
    assert humanize.naturaldelta(value) == expected


@pytest.mark.ecp
@pytest.mark.parametrize("value, expected", [
    pytest.param(60, "a minute", id="ND-04a"),
    pytest.param(3600, "an hour", id="ND-04b"),
    pytest.param(1.5, "a second", id="ND-04c"),
    pytest.param("60", "a minute", id="ND-04d"),
])
def test_naturaldelta_ecp_plain_number_and_numeric_text(value, expected):
    assert humanize.naturaldelta(value) == expected


@pytest.mark.negative
def test_naturaldelta_negative_text_returned_unchanged():  # ND-05
    assert humanize.naturaldelta("abc") == "abc"


@pytest.mark.negative
def test_naturaldelta_negative_none_returns_none():  # ND-06
    assert humanize.naturaldelta(None) is None


@pytest.mark.smoke
@pytest.mark.boundary
@pytest.mark.parametrize("value, expected", [
    pytest.param(secs(59), "59 seconds", id="ND-09a"),
    pytest.param(secs(60), "a minute", id="ND-09b"),
    pytest.param(secs(119), "a minute", id="ND-09c"),
    pytest.param(secs(120), "2 minutes", id="ND-09d"),
    pytest.param(secs(3599), "59 minutes", id="ND-09e"),
    pytest.param(secs(3600), "an hour", id="ND-09f"),
    pytest.param(secs(86399), "23 hours", id="ND-09g"),
    pytest.param(secs(86400), "a day", id="ND-09h"),
])
def test_naturaldelta_bva_short_unit_edges(value, expected):
    assert humanize.naturaldelta(value) == expected


@pytest.mark.boundary
@pytest.mark.parametrize("value, expected", [
    pytest.param(days(29), "29 days", id="ND-10a"),
    pytest.param(days(30), "30 days", id="ND-10b"),
    pytest.param(days(31), "a month", id="ND-10c"),
    pytest.param(days(364), "11 months", id="ND-10d"),
    pytest.param(days(365), "a year", id="ND-10e"),
    pytest.param(days(366), "1 year, 1 day", id="ND-10f"),
])
def test_naturaldelta_bva_long_unit_edges(value, expected):
    assert humanize.naturaldelta(value) == expected


@pytest.mark.ecp
@pytest.mark.parametrize("value, months, expected", [
    pytest.param(days(30), False, "30 days", id="ND-07a"),
    pytest.param(days(60), False, "60 days", id="ND-07b"),
    pytest.param(days(60), True, "a month", id="ND-07c"),
])
def test_naturaldelta_months_option(value, months, expected):
    assert humanize.naturaldelta(value, months=months) == expected


@pytest.mark.negative
def test_naturaldelta_negative_unsupported_minimum_unit_raises_error():  # ND-08
    with pytest.raises(ValueError):
        humanize.naturaldelta(secs(90), minimum_unit="minutes")


@pytest.mark.datadriven
@pytest.mark.parametrize("value, expected", load_csv("naturaldelta_data.csv"))
def test_naturaldelta_from_csv(value, expected):
    assert humanize.naturaldelta(value) == expected


# =====================================================================
# module level tests (time.py as a whole)
# =====================================================================
@pytest.mark.module
def test_module_zero_is_a_moment():
    assert humanize.naturaldelta(secs(0)) == "a moment"


@pytest.mark.module
def test_module_seconds_below_a_minute_use_the_seconds_unit():
    for s in range(2, 60):
        assert humanize.naturaldelta(secs(s)) == f"{s} seconds"


@pytest.mark.module
def test_module_minutes_two_to_fifty_nine():
    for m in range(2, 60):
        assert humanize.naturaldelta(timedelta(minutes=m)) == f"{m} minutes"


@pytest.mark.module
def test_module_hours_two_to_twenty_three():
    for h in range(2, 24):
        assert humanize.naturaldelta(timedelta(hours=h)) == f"{h} hours"


@pytest.mark.module
def test_module_seconds_and_timedelta_give_same_answer():
    for s in [0, 1, 59, 60, 3600, 86400]:
        assert humanize.naturaldelta(s) == humanize.naturaldelta(secs(s))


@pytest.mark.module
def test_module_result_is_always_text():
    for s in [0, 1, 59, 60, 3599, 3600, 86399, 86400, 2592000, 31536000]:
        assert isinstance(humanize.naturaldelta(secs(s)), str)