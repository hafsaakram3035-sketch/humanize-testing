"""Unit tests for the number module of humanize (Wajiha).

Functions covered: intcomma, ordinal, apnumber.
Test ids (IC-01, OR-10, AP-05 ...) match assignment_docs/notes_number.md.
"""
import csv
from pathlib import Path

import humanize
import pytest

DATA_DIR = Path(__file__).resolve().parents[2] / "test_data"


def load_csv(name):
    """Read (input, expected) pairs from a CSV file in test_data."""
    with open(DATA_DIR / name, newline="", encoding="utf-8") as f:
        return [(int(row["input"]), row["expected"]) for row in csv.DictReader(f)]


# =====================================================================
# intcomma
# =====================================================================
@pytest.mark.smoke
@pytest.mark.ecp
@pytest.mark.parametrize("value, expected", [
    pytest.param(12345, "12,345", id="IC-01"),
    pytest.param(-1000, "-1,000", id="IC-02"),
    pytest.param(0, "0", id="IC-03"),
])
def test_intcomma_ecp_integers(value, expected):
    assert humanize.intcomma(value) == expected


@pytest.mark.ecp
@pytest.mark.parametrize("value, expected", [
    pytest.param(1000.5, "1,000.5", id="IC-04"),
    pytest.param("1000", "1,000", id="IC-05"),
])
def test_intcomma_ecp_float_and_numeric_string(value, expected):
    assert humanize.intcomma(value) == expected


@pytest.mark.negative
@pytest.mark.parametrize("value, expected", [
    pytest.param("abc", "abc", id="IC-06"),
    pytest.param("", "", id="IC-07"),
])
def test_intcomma_negative_non_numeric_returned_unchanged(value, expected):
    assert humanize.intcomma(value) == expected


@pytest.mark.negative
def test_intcomma_negative_none_returns_none():  # IC-08
    assert humanize.intcomma(None) is None


@pytest.mark.ecp
def test_intcomma_ndigits_rounds_decimals():  # IC-09
    assert humanize.intcomma(1234.5678, 2) == "1,234.57"


@pytest.mark.smoke
@pytest.mark.boundary
@pytest.mark.parametrize("value, expected", [
    pytest.param(999, "999", id="IC-10"),
    pytest.param(1000, "1,000", id="IC-11"),
    pytest.param(1001, "1,001", id="IC-12"),
])
def test_intcomma_bva_around_one_thousand(value, expected):
    assert humanize.intcomma(value) == expected


@pytest.mark.boundary
@pytest.mark.parametrize("value, expected", [
    pytest.param(-999, "-999", id="IC-13"),
    pytest.param(-1000, "-1,000", id="IC-14"),
])
def test_intcomma_bva_negative_thousand(value, expected):
    assert humanize.intcomma(value) == expected


@pytest.mark.datadriven
@pytest.mark.parametrize("value, expected", load_csv("intcomma_data.csv"))
def test_intcomma_from_csv(value, expected):
    assert humanize.intcomma(value) == expected


# =====================================================================
# ordinal
# =====================================================================
@pytest.mark.smoke
@pytest.mark.ecp
@pytest.mark.parametrize("value, expected", [
    pytest.param(1, "1st", id="OR-01a"),
    pytest.param(2, "2nd", id="OR-01b"),
    pytest.param(3, "3rd", id="OR-01c"),
])
def test_ordinal_ecp_one_two_three(value, expected):
    assert humanize.ordinal(value) == expected


@pytest.mark.ecp
def test_ordinal_ecp_four_uses_th():  # OR-02
    assert humanize.ordinal(4) == "4th"


@pytest.mark.ecp
@pytest.mark.parametrize("value, expected", [
    pytest.param(21, "21st", id="OR-03a"),
    pytest.param(22, "22nd", id="OR-03b"),
    pytest.param(23, "23rd", id="OR-03c"),
])
def test_ordinal_ecp_above_twenty(value, expected):
    assert humanize.ordinal(value) == expected


@pytest.mark.ecp
@pytest.mark.parametrize("value, expected", [
    pytest.param(101, "101st", id="OR-04a"),
    pytest.param(111, "111th", id="OR-04b"),
])
def test_ordinal_ecp_large_numbers(value, expected):
    assert humanize.ordinal(value) == expected


@pytest.mark.ecp
@pytest.mark.parametrize("value, expected", [
    pytest.param(0, "0th", id="OR-05"),
    pytest.param("1", "1st", id="OR-06"),
])
def test_ordinal_ecp_zero_and_numeric_string(value, expected):
    assert humanize.ordinal(value) == expected


@pytest.mark.negative
def test_ordinal_negative_non_numeric_returned_unchanged():  # OR-07
    assert humanize.ordinal("abc") == "abc"


@pytest.mark.negative
def test_ordinal_negative_none_returns_none():  # OR-08
    assert humanize.ordinal(None) is None


@pytest.mark.negative
def test_ordinal_negative_number_documents_current_behaviour():  # OR-09
    # Observation: the library gives "-1th", which is not correct English.
    assert humanize.ordinal(-1) == "-1th"


@pytest.mark.boundary
@pytest.mark.parametrize("value, expected", [
    pytest.param(10, "10th", id="OR-10a"),
    pytest.param(11, "11th", id="OR-10b"),
    pytest.param(12, "12th", id="OR-11a"),
    pytest.param(13, "13th", id="OR-11b"),
    pytest.param(14, "14th", id="OR-12"),
])
def test_ordinal_bva_teens(value, expected):
    assert humanize.ordinal(value) == expected


@pytest.mark.datadriven
@pytest.mark.parametrize("value, expected", load_csv("ordinal_data.csv"))
def test_ordinal_from_csv(value, expected):
    assert humanize.ordinal(value) == expected


# =====================================================================
# apnumber
# =====================================================================
@pytest.mark.smoke
@pytest.mark.ecp
@pytest.mark.parametrize("value, expected", [
    pytest.param(1, "one", id="AP-01a"),
    pytest.param(5, "five", id="AP-01b"),
    pytest.param(9, "nine", id="AP-01c"),
])
def test_apnumber_ecp_single_digit_as_word(value, expected):
    assert humanize.apnumber(value) == expected


@pytest.mark.ecp
def test_apnumber_ecp_zero_is_word():  # AP-02
    assert humanize.apnumber(0) == "zero"


@pytest.mark.ecp
@pytest.mark.parametrize("value, expected", [
    pytest.param(10, "10", id="AP-03a"),
    pytest.param(11, "11", id="AP-03b"),
    pytest.param(100, "100", id="AP-03c"),
])
def test_apnumber_ecp_ten_or_more_stays_digits(value, expected):
    assert humanize.apnumber(value) == expected


@pytest.mark.ecp
@pytest.mark.parametrize("value, expected", [
    pytest.param(-1, "-1", id="AP-04"),
    pytest.param("4", "four", id="AP-05"),
    pytest.param(4.5, "four", id="AP-06"),
])
def test_apnumber_ecp_negative_string_and_float(value, expected):
    assert humanize.apnumber(value) == expected


@pytest.mark.negative
def test_apnumber_negative_non_numeric_returned_unchanged():  # AP-07
    assert humanize.apnumber("abc") == "abc"


@pytest.mark.negative
def test_apnumber_negative_none_returns_none():  # AP-08
    assert humanize.apnumber(None) is None


@pytest.mark.boundary
@pytest.mark.parametrize("value, expected", [
    pytest.param(-1, "-1", id="AP-09"),
    pytest.param(0, "zero", id="AP-10"),
    pytest.param(1, "one", id="AP-11"),
    pytest.param(9, "nine", id="AP-12"),
    pytest.param(10, "10", id="AP-13"),
])
def test_apnumber_bva_edges(value, expected):
    assert humanize.apnumber(value) == expected


# =====================================================================
# module level tests (number.py as a whole)
# =====================================================================
@pytest.mark.module
def test_module_apnumber_zero_to_nine_are_words():
    words = [humanize.apnumber(i) for i in range(10)]
    assert words == ["zero", "one", "two", "three", "four",
                     "five", "six", "seven", "eight", "nine"]


@pytest.mark.module
def test_module_apnumber_ten_to_twenty_keep_digits():
    assert [humanize.apnumber(i) for i in range(10, 21)] == [str(i) for i in range(10, 21)]


@pytest.mark.module
def test_module_ordinal_always_has_valid_suffix():
    for n in range(1, 31):
        assert humanize.ordinal(n).endswith(("st", "nd", "rd", "th"))


@pytest.mark.module
def test_module_ordinal_starts_with_the_number():
    for n in range(0, 121):
        assert humanize.ordinal(n).startswith(str(n))


@pytest.mark.module
def test_module_intcomma_has_no_comma_below_1000():
    for n in range(0, 1000):
        assert "," not in humanize.intcomma(n)


@pytest.mark.module
def test_module_intcomma_round_trip_keeps_the_digits():
    for n in [0, 7, 999, 1000, 54321, 1234567, 10**9]:
        assert humanize.intcomma(n).replace(",", "") == str(n)


@pytest.mark.module
def test_module_functions_agree_on_small_numbers():
    # For 1 to 9, intcomma gives digits while apnumber gives words.
    for n in range(1, 10):
        assert humanize.intcomma(n) == str(n)
        assert humanize.apnumber(n) != str(n)