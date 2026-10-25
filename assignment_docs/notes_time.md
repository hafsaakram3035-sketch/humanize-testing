\# Test Design Notes: filesize module (Hafsa)



Project: humanize (Python). Module: `filesize.py`

Function: `naturalsize`

Expected results below come from running the function in our own environment

(see `explore\_output.txt`).



\## naturalsize



\### Equivalence Class Partitioning (ECP)



| ID | Input class | Input | Expected |

|---|---|---|---|

| NS-01 | Bytes (below 1000) | 0, 1, 2, 999 | '0 Bytes', '1 Byte', '2 Bytes', '999 Bytes' |

| NS-02 | Kilobytes | 1500 | '1.5 kB' |

| NS-03 | Megabytes | 1000000, 1500000 | '1.0 MB', '1.5 MB' |

| NS-04 | Bigger units | 10\*\*9, 10\*\*12, 10\*\*15 | '1.0 GB', '1.0 TB', '1.0 PB' |

| NS-05 | Negative numbers | -1, -999, -1000, -1500000 | '-1 Byte', '-999 Bytes', '-1.0 kB', '-1.5 MB' |

| NS-06 | Numeric string | '1000', '1500' | '1.0 kB', '1.5 kB' |

| NS-07 | Float | 1500.5 | '1.5 kB' |

| NS-08 | Non-numeric string | 'abc' | ValueError |

| NS-09 | None | None | TypeError |

| NS-15 | gnu=True option | 999, 1000, 1024, 1048576 | '999B', '1000B', '1.0K', '1.0M' |

| NS-16 | format option | 1500 with '%.0f' and '%.2f' | '2 kB', '1.50 kB' |



\### Boundary Value Analysis (BVA)



| ID | Boundary | Input | Expected |

|---|---|---|---|

| NS-10 | One byte versus more | 1, 2 | '1 Byte', '2 Bytes' |

| NS-11 | Around 1000 | 999, 1000, 1001 | '999 Bytes', '1.0 kB', '1.0 kB' |

| NS-12 | Around one million | 999999, 1000000 | '1000.0 kB', '1.0 MB' |

| NS-13 | Binary, around 1024 | 1023, 1024, 1025 (binary=True) | '1023 Bytes', '1.0 KiB', '1.0 KiB' |

| NS-14 | Binary, around 1 MiB | 1048575, 1048576 (binary=True) | '1024.0 KiB', '1.0 MiB' |



\## Observations (things that looked unusual)



\- 1 gives '1 Byte' (singular) but 2 gives '2 Bytes'.

\- By default the function counts in 1000s (kB), so 1024 gives '1.0 kB'. With binary=True it counts in 1024s (KiB).

\- Rounding quirk: 999999 gives '1000.0 kB' instead of '1.0 MB' (and 1048575 with binary=True gives '1024.0 KiB').

\- 'abc' raises ValueError and None raises TypeError, with no friendly message.

\- gnu=True removes the space and 1000 gives '1000B' (not '1.0K').

