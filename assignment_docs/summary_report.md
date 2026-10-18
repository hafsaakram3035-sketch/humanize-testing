\# Summary Report: Unit Test Automation for humanize



Group: Hafsa, Wajiha

Repository: \[paste the GitHub link here]



\## 1. Project

We tested the open-source Python library \*\*humanize\*\* (turns numbers, file sizes

and time differences into readable text). Tests are written with pytest.



\## 2. Setup (Task 1)

Python 3.12, Git, virtual environment, `pip install -e ".\[tests]"`.

The original humanize tests pass (384 passed, 15 skipped).

Setup video: `assignment\_docs/setup\_video.mp4`.



\## 3. Modules and functions tested (Task 2)

| Module | Functions | Tested by |

|---|---|---|

| number.py | intcomma, ordinal, apnumber | Wajiha |

| filesize.py | naturalsize | \[Hafsa] |

| time.py | naturaldelta | \[Hafsa] |



Test design: Equivalence Class Partitioning and Boundary Value Analysis.

Notes: `notes\_number.md`, `notes\_filesize.md`, `notes\_time.md`.



\## 4. Number of tests

| Person | Test functions | Test cases (with parametrize) |

|---|---|---|

| Wajiha | 33 | 120 |

| Hafsa | \[..] | \[..] |



Wajiha: intcomma 8, ordinal 10, apnumber 7, module level 7 test functions,

plus 1 Excel driven test function.



\## 5. Excel and CSV (Task 3)

Test cases are written in `test\_cases\_wajiha.xlsx` and `test\_cases\_hafsa.xlsx`.

Each row names a function and a CSV file in `test\_data/`. The tests read the

Excel sheet, then the CSV file, and run every data row (Wajiha: 5 test cases, 44 data rows).



\## 6. Configuration (Task 4)

\- Parallel run: pytest-xdist (`-n 2`)

\- Suites: one folder per module

\- Groups: markers smoke, ecp, boundary, negative, datadriven, excel, module

\- Parameterization: `@pytest.mark.parametrize`, CSV and Excel

\- Order: `conftest.py` (group order) and `@pytest.mark.order(n)` (single tests)

\- Run everything with `run\_tests.bat`, see `README.md`



\## 7. Results

\[Total tests, passed, failed. Add the result of run\_tests.bat groups.]

HTML report: `assignment\_docs/report.html`



\## 8. Findings (unusual behaviour in humanize)

\- `ordinal(-1)` returns "-1th", which is not correct English.

\- Passing None to intcomma, ordinal, apnumber and naturaldelta returns None.

\- Text like "abc" is returned unchanged by these functions.

\- `naturalsize("abc")` raises ValueError and `naturalsize(None)` raises TypeError.

\- `naturaldelta(119 seconds)` gives "a minute" (rounds down).

\- Our version of humanize has no `natural\_list` function, so we replaced it with `naturaldelta`.



\## 9. Task distribution

\[Write who did what, based on the commit history.]

