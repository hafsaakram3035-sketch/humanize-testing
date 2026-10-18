**# humanize-testing**



**Unit test automation for the Python library \*\*humanize\*\***

**(source: https://github.com/jmoiron/humanize).**

**Tests are written with \*\*pytest\*\*.**



**Group members: Hafsa, Wajiha**



**## Setup (Windows)**



**```**

**python -m venv venv**

**venv\\Scripts\\activate**

**pip install -e ".\[tests]"**

**pip install -r requirements.txt**

**```**



**Check the setup: `pytest tests -q` (runs the original humanize tests).**



**## Project structure**



**- `src/` and `tests/`: original humanize source and its own tests**

**- `unit\_tests/`: our automated unit tests (one folder per module = one suite)**

&#x20; **- `number/` (intcomma, ordinal, apnumber)**

&#x20; **- `filesize/` (naturalsize)**

&#x20; **- `time\_tests/` (naturaldelta)**

**- `test\_data/`: CSV files with test data**

**- `assignment\_docs/`: setup video, test design notes (ECP and BVA), Excel test cases, reports**

**- `pytest.ini`: markers (groups) and settings**

**- `conftest.py`: sets the order in which groups run**

**- `run\_tests.bat`: ready-made run commands**



**## Test groups (markers)**



**| Marker | Meaning |**

**|---|---|**

**| smoke | quick basic checks |**

**| ecp | equivalence class partitioning tests |**

**| boundary | boundary value analysis tests |**

**| negative | invalid input tests |**

**| datadriven | tests that read CSV and Excel data |**

**| excel | tests driven by the Excel sheet |**

**| module | module level tests |**



**## How to run**



**```**

**run\_tests.bat all        (all tests, one by one, in group order)**

**run\_tests.bat parallel   (all tests, 2 workers at the same time)**

**run\_tests.bat groups     (groups one after another, each in parallel)**

**run\_tests.bat suites     (each module folder one after another)**

**run\_tests.bat report     (parallel run and HTML report)**

**```**



**Single commands:**



**```**

**pytest unit\_tests                      (everything)**

**pytest unit\_tests -n 2                 (parallel)**

**pytest unit\_tests\\number               (one suite)**

**pytest -m smoke                        (one group)**

**pytest -m "ecp or boundary"            (two groups)**

**pytest unit\_tests -k intcomma          (tests of one function)**

**```**



**## Execution order**



**1. Groups run in this order: smoke, ecp, boundary, negative, datadriven, module**

&#x20;  **(set in `conftest.py`).**

**2. Some tests have an explicit position with `@pytest.mark.order(n)`.**



**## Data driven tests**



**- Test data is in CSV files in `test\_data/`.**

**- Test cases are described in Excel sheets in `assignment\_docs/`**

&#x20; **(`test\_cases\_wajiha.xlsx`). Each row names a function and a CSV file.**

**- Parameterization uses `@pytest.mark.parametrize`.**

