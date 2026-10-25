"""Unit tests for the filesize module of humanize (Hafsa).

Function covered: naturalsize.
Test ids (NS-01a, NS-11b ...) match assignment_docs/notes_filesize.md.
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
# naturalsize
# =====================================================================
@pytest.mark.smoke
@pytest.mark.ecp
@pytest.mark.parametrize("value, expected", [
    pytest.param(0, "0 Bytes", id="NS-01a"),
    pytest.param(1, "1 Byte", id="NS-01b"),
    pytest.param(2, "2 Bytes", id="NS-01c"),
    pytest.param(999, "999 Bytes", id="NS-01d"),
])
def test_naturalsize_ecp_bytes_range(value, expected):
    assert humanize.naturalsize(value) == expected


@pytest.mark.ecp
@pytest.mark.parametrize("value, expected", [
    pytest.param(1500, "1.5 kB", id="NS-02"),
    pytest.param(1000000, "1.0 MB", id="NS-03a"),
    pytest.param(1500000, "1.5 MB", id="NS-03b"),
    pytest.param(10**9, "1.0 GB", id="NS-04a"),
    pytest.param(10**12, "1.0 TB", id="NS-04b"),
    pytest.param(10**15, "1.0 PB", id="NS-04c"),
])
def test_naturalsize_ecp_larger_units(value, expected):
    assert humanize.naturalsize(value) == expected


@pytest.mark.ecp
@pytest.mark.parametrize("value, expected", [
    pytest.param(-1, "-1 Byte", id="NS-05a"),
    pytest.param(-999, "-999 Bytes", id="NS-05b"),
    pytest.param(-1000, "-1.0 kB", id="NS-05c"),
    pytest.param(-1500000, "-1.5 MB", id="NS-05d"),
])
def test_naturalsize_ecp_negative_values(value, expected):
    assert humanize.naturalsize(value) == expected


@pytest.mark.ecp
@pytest.mark.parametrize("value, expected", [
    pytest.param("1000", "1.0 kB", id="NS-06a"),
    pytest.param("1500", "1.5 kB", id="NS-06b"),
    pytest.param(1500.5, "1.5 kB", id="NS-07"),
])
def test_naturalsize_ecp_string_and_float_input(value, expected):
    assert humanize.naturalsize(value) == expected


@pytest.mark.negative
def test_naturalsize_negative_invalid_text_raises_value_error():  # NS-08
    with pytest.raises(ValueError):
        humanize.naturalsize("abc")


@pytest.mark.negative
def test_naturalsize_negative_none_raises_type_error():  # NS-09
    with pytest.raises(TypeError):
        humanize.naturalsize(None)


@pytest.mark.smoke
@pytest.mark.boundary
@pytest.mark.parametrize("value, expected", [
    pytest.param(1, "1 Byte", id="NS-10a"),
    pytest.param(2, "2 Bytes", id="NS-10b"),
    pytest.param(999, "999 Bytes", id="NS-11a"),
    pytest.param(1000, "1.0 kB", id="NS-11b"),
    pytest.param(1001, "1.0 kB", id="NS-11c"),
    pytest.param(999999, "1000.0 kB", id="NS-12a"),
    pytest.param(1000000, "1.0 MB", id="NS-12b"),
])
def test_naturalsize_bva_decimal_unit_edges(value, expected):
    assert humanize.naturalsize(value) == expected


@pytest.mark.boundary
@pytest.mark.parametrize("value, expected", [
    pytest.param(1023, "1023 Bytes", id="NS-13a"),
    pytest.param(1024, "1.0 KiB", id="NS-13b"),
    pytest.param(1025, "1.0 KiB", id="NS-13c"),
    pytest.param(1048575, "1024.0 KiB", id="NS-14a"),
    pytest.param(1048576, "1.0 MiB", id="NS-14b"),
])
def test_naturalsize_bva_binary_unit_edges(value, expected):
    assert humanize.naturalsize(value, binary=True) == expected


@pytest.mark.ecp
@pytest.mark.parametrize("value, options, expected", [
    pytest.param(999, {"gnu": True}, "999B", id="NS-15a"),
    pytest.param(1000, {"gnu": True}, "1000B", id="NS-15b"),
    pytest.param(1024, {"gnu": True}, "1.0K", id="NS-15c"),
    pytest.param(1048576, {"gnu": True}, "1.0M", id="NS-15d"),
    pytest.param(1500, {"format": "%.0f"}, "2 kB", id="NS-16a"),
    pytest.param(1500, {"format": "%.2f"}, "1.50 kB", id="NS-16b"),
])
def test_naturalsize_options_gnu_and_format(value, options, expected):
    assert humanize.naturalsize(value, **options) == expected


@pytest.mark.datadriven
@pytest.mark.parametrize("value, expected", load_csv("naturalsize_data.csv"))
def test_naturalsize_from_csv(value, expected):
    assert humanize.naturalsize(value) == expected


# =====================================================================
# module level tests (filesize.py as a whole)
# =====================================================================
@pytest.mark.module
def test_module_decimal_unit_names_grow_with_size():
    units = ["kB", "MB", "GB", "TB", "PB"]
    for power, unit in zip(range(1, 6), units):
        assert humanize.naturalsize(1000 ** power).endswith(unit)


@pytest.mark.module
def test_module_binary_unit_names_grow_with_size():
    units = ["KiB", "MiB", "GiB", "TiB"]
    for power, unit in zip(range(1, 5), units):
        assert humanize.naturalsize(1024 ** power, binary=True).endswith(unit)


@pytest.mark.module
def test_module_decimal_and_binary_agree_below_1000():
    for n in range(0, 1000):
        assert humanize.naturalsize(n) == humanize.naturalsize(n, binary=True)


@pytest.mark.module
def test_module_negative_mirrors_positive():
    for n in [1, 999, 1000, 1500, 10**6]:
        assert humanize.naturalsize(-n) == "-" + humanize.naturalsize(n)


@pytest.mark.module
def test_module_gnu_style_has_no_space():
    for n in [1000, 1024, 10**6]:
        assert " " not in humanize.naturalsize(n, gnu=True)


@pytest.mark.module
def test_module_text_and_number_input_give_same_result():
    for n in [0, 1, 999, 1000, 1500, 10**6]:
        assert humanize.naturalsize(str(n)) == humanize.naturalsize(n)


@pytest.mark.module
def test_module_result_is_always_text():
    for n in [0, 1, 999, 1000, 10**6, 10**12]:
        assert isinstance(humanize.naturalsize(n), str)