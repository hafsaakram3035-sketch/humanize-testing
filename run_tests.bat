@echo off
REM Usage: run_tests.bat [all|parallel|groups|suites|report]
set MODE=%1
if "%MODE%"=="" set MODE=all

if /i "%MODE%"=="all" goto all
if /i "%MODE%"=="parallel" goto parallel
if /i "%MODE%"=="groups" goto groups
if /i "%MODE%"=="suites" goto suites
if /i "%MODE%"=="report" goto report
echo Unknown mode "%MODE%". Use: all, parallel, groups, suites or report.
goto end

:all
echo === ALL TESTS, one by one, in group order ===
python -m pytest unit_tests -v
goto end

:parallel
echo === ALL TESTS, 2 workers at the same time ===
python -m pytest unit_tests -n 2 -q
goto end

:groups
echo === GROUP 1: smoke ===
python -m pytest unit_tests -m "smoke" -n 2 -q
echo === GROUP 2: ecp, boundary, negative ===
python -m pytest unit_tests -m "(ecp or boundary or negative) and not smoke" -n 2 -q
echo === GROUP 3: data driven, CSV and Excel ===
python -m pytest unit_tests -m "datadriven" -n 2 -q
echo === GROUP 4: module level ===
python -m pytest unit_tests -m "module" -n 2 -q
goto end

:suites
echo === SUITE: number ===
python -m pytest unit_tests\number -n 2 -q
echo === SUITE: filesize ===
python -m pytest unit_tests\filesize -n 2 -q
echo === SUITE: time ===
python -m pytest unit_tests\time_tests -n 2 -q
goto end

:report
echo === ALL TESTS in parallel, with an HTML report ===
python -m pytest unit_tests -n 2 --html=assignment_docs\report.html --self-contained-html
goto end

:end