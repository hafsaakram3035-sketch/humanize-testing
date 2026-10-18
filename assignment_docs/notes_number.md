\# Test Design Notes: number module (Wajiha)



Project: humanize (Python). Module: `number.py`

Functions: `intcomma`, `ordinal`, `apnumber`

Expected results below come from running the functions in our own environment

(see `explore\_output.txt`).



\## 1. intcomma



\### Equivalence Class Partitioning (ECP)



| ID | Input class | Input | Expected |

|---|---|---|---|

| IC-01 | Positive integer | 12345 | '12,345' |

| IC-02 | Negative integer | -1000 | '-1,000' |

| IC-03 | Zero | 0 | '0' |

| IC-04 | Float | 1000.5 | '1,000.5' |

| IC-05 | Numeric string | '1000' | '1,000' |

| IC-06 | Non-numeric string | 'abc' | 'abc' (returned unchanged) |

| IC-07 | Empty string | '' | '' |

| IC-08 | None | None | None |

| IC-09 | Rounding digits | (1234.5678, ndigits=2) | '1,234.57' |



\### Boundary Value Analysis (BVA)



| ID | Boundary | Input | Expected |

|---|---|---|---|

| IC-10 | Just below 1000 | 999 | '999' |

| IC-11 | Exactly 1000 | 1000 | '1,000' |

| IC-12 | Just above 1000 | 1001 | '1,001' |

| IC-13 | Negative, below limit | -999 | '-999' |

| IC-14 | Negative, at limit | -1000 | '-1,000' |



\## 2. ordinal



\### ECP



| ID | Input class | Input | Expected |

|---|---|---|---|

| OR-01 | Ends in 1, 2, 3 | 1, 2, 3 | '1st', '2nd', '3rd' |

| OR-02 | Ends in 4 to 9 | 4 | '4th' |

| OR-03 | Ends in 1, 2, 3 (above 20) | 21, 22, 23 | '21st', '22nd', '23rd' |

| OR-04 | Larger numbers | 101, 111 | '101st', '111th' |

| OR-05 | Zero | 0 | '0th' |

| OR-06 | Numeric string | '1' | '1st' |

| OR-07 | Non-numeric string | 'abc' | 'abc' |

| OR-08 | None | None | None |

| OR-09 | Negative number | -1 | '-1th' (looks wrong, see observations) |



\### BVA



| ID | Boundary | Input | Expected |

|---|---|---|---|

| OR-10 | Teens exception start | 10, 11 | '10th', '11th' |

| OR-11 | Inside teens | 12, 13 | '12th', '13th' |

| OR-12 | End of teens | 14 | '14th' |

| OR-13 | Lowest valid | 0, 1 | '0th', '1st' |

| OR-14 | 111 follows teens rule | 111 | '111th' |



\## 3. apnumber



\### ECP



| ID | Input class | Input | Expected |

|---|---|---|---|

| AP-01 | Single digit as word | 1, 5, 9 | 'one', 'five', 'nine' |

| AP-02 | Zero | 0 | 'zero' |

| AP-03 | Ten or more | 10, 11, 100 | '10', '11', '100' |

| AP-04 | Negative | -1 | '-1' |

| AP-05 | Numeric string | '4' | 'four' |

| AP-06 | Float | 4.5 | 'four' |

| AP-07 | Non-numeric string | 'abc' | 'abc' |

| AP-08 | None | None | None |



\### BVA



| ID | Boundary | Input | Expected |

|---|---|---|---|

| AP-09 | Just below zero | -1 | '-1' |

| AP-10 | Lowest word | 0 | 'zero' |

| AP-11 | First digit word | 1 | 'one' |

| AP-12 | Last word | 9 | 'nine' |

| AP-13 | First number as digits | 10 | '10' |



\## Observations (things that looked unusual)



\- `ordinal(-1)` returns '-1th', which is not a correct English ordinal.

\- Passing `None` to `intcomma`, `ordinal` and `apnumber` returns `None` itself (no error).

\- Non-numeric strings like 'abc' are returned unchanged, not rejected.

\- `apnumber(4.5)` returns 'four': the decimal part is dropped.

