# Summary Report: Unit Test Automation for humanize

Group: Hafsa, Wajiha
Repository: https://github.com/hafsaakram3035-sketch/humanize-testing

## 1. Project
We tested the open-source Python library **humanize** (it turns numbers,
file sizes and time differences into readable text). Tests are written with pytest.

## 2. Setup (Task 1)
Python 3.12, Git, a virtual environment, and `pip install -e ".[tests]"`.
The original humanize tests pass (384 passed, 15 skipped) on both our laptops.
Setup video: `assignment_docs/setup_video.mp4`.

## 3. Modules and functions tested (Task 2)

| Module | Functions | Tested by | Notes file |
|---|---|---|---|
| number.py | intcomma, ordinal, apnumber | Wajiha | notes_number.md |
| filesize.py | naturalsize | Hafsa | notes_filesize.md |
| time.py | naturaldelta | Hafsa | notes_time.md |

Test design: Equivalence Class Partitioning (ECP) and Boundary Value Analysis (BVA).
Note: our humanize version has no `natural_list` function, so we used `naturaldelta` instead.

## 4. Number of tests

| Person | Test functions | Test cases (with parametrize) |
|---|---|---|
| Wajiha | 33 | 120 |
| Hafsa | 35 | 136 |
| **Total** | **68** | **256** |

Wajiha: intcomma 8, ordinal 10, apnumber 7, module level 7, plus 1 Excel driven function.
Hafsa: naturalsize 10 and filesize module level 7, naturaldelta 10 and time module level 6,
plus 2 Excel driven functions.

## 5. Excel and CSV (Task 3)

| File | Test cases | Data rows |
|---|---|---|
| test_cases_wajiha.xlsx | 5 (TC-X01 to TC-X05) | 44 |
| test_cases_hafsa.xlsx | 4 (TC-H01 to TC-H04) | 23 |

There are 11 CSV files in `test_data/`. Each Excel row names a function and a CSV
file. The tests read the Excel sheet, then the CSV file, and run every data row.

## 6. Configuration (Task 4)

- Parallel run: pytest-xdist (`-n 2`)
- Suites: one folder per module (number, filesize, time_tests)
- Groups: markers smoke, ecp, boundary, negative, datadriven, excel, module
- Parameterization: `@pytest.mark.parametrize`, CSV and Excel
- Order: `conftest.py` sets the group order, `@pytest.mark.order(n)` sets single tests
- Everything runs with `run_tests.bat` (modes: all, parallel, groups, suites, report); see `README.md`

## 7. Results

- `pytest unit_tests -q`: 256 passed
- Groups: smoke 40, ecp/boundary/negative 88, datadriven 108, module 20
- Suites: number 120, filesize 63, time_tests 73
- HTML report: `assignment_docs/report.html`

## 8. Findings (unusual behaviour in humanize)

- `ordinal(-1)` returns '-1th', which is not correct English.
- Passing None to intcomma, ordinal, apnumber and naturaldelta returns None itself.
- Text like 'abc' is returned unchanged by intcomma, ordinal, apnumber and naturaldelta.
- `naturalsize('abc')` raises ValueError and `naturalsize(None)` raises TypeError.
- `naturalsize(999999)` returns '1000.0 kB' instead of '1.0 MB' (rounding quirk).
- `naturalsize(1)` gives '1 Byte' but `naturalsize(2)` gives '2 Bytes'.
- By default naturalsize counts in 1000s (kB); binary=True counts in 1024s (KiB).
- `naturaldelta` rounds down: 119 seconds gives 'a minute'.
- 31 days is the first value that gives 'a month'; 30 days stays '30 days'.
- Negative timedeltas were not tested because results differ between humanize versions.

## 9. Task distribution

- Wajiha: setup and setup video, number module notes and tests, Excel sheet and CSV data
  for the number module, configuration (conftest, run_tests.bat, README, requirements),
  final HTML report and this summary. Commits: 17
- Hafsa: setup on her laptop, filesize and time notes and tests, her Excel sheet and CSV
  data, and checking the configuration on her modules. Commits: 14 (13 under the name
  Hafsa and 1 under her GitHub account name).