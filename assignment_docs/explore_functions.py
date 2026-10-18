"""Run each humanize function with sample inputs and print the real output.
Use this to decide the expected results for our ECP and BVA notes."""
import datetime
import humanize


def show(func, *args, **kwargs):
    label = func.__name__ + str(args) + (str(kwargs) if kwargs else "")
    try:
        result = repr(func(*args, **kwargs))
    except Exception as e:
        result = f"ERROR {type(e).__name__}: {e}"
    print(f"{label:55} -> {result}")


print("=== intcomma ===")
for v in [0, 1, 999, 1000, 1001, 12345, -999, -1000, 1000.5, "1000", "abc", "", None]:
    show(humanize.intcomma, v)
show(humanize.intcomma, 1234.5678, 2)

print("\n=== ordinal ===")
for v in [0, 1, 2, 3, 4, 10, 11, 12, 13, 14, 21, 22, 23, 101, 111, -1, "1", "abc", None]:
    show(humanize.ordinal, v)

print("\n=== apnumber ===")
for v in [-1, 0, 1, 5, 9, 10, 11, 100, "4", 4.5, "abc", None]:
    show(humanize.apnumber, v)

print("\n=== naturalsize ===")
for v in [0, 1, 2, 999, 1000, 1001, 1500, 1000000, 10**9, -1000, "1000", "abc", None]:
    show(humanize.naturalsize, v)
show(humanize.naturalsize, 1023, binary=True)
show(humanize.naturalsize, 1024, binary=True)
show(humanize.naturalsize, 1000, gnu=True)
show(humanize.naturalsize, 1024, gnu=True)
show(humanize.naturalsize, 1500, format="%.2f")

print("\n=== naturaldelta ===")
for s in [0, 1, 2, 59, 60, 61, 119, 120, 3599, 3600, 7200, 86399]:
    show(humanize.naturaldelta, datetime.timedelta(seconds=s))
for d in [2, 29, 30, 365, 366, 730]:
    show(humanize.naturaldelta, datetime.timedelta(days=d))
show(humanize.naturaldelta, datetime.timedelta(days=30), months=False)
show(humanize.naturaldelta, 60)
show(humanize.naturaldelta, "abc")
show(humanize.naturaldelta, None)