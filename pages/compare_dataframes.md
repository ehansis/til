# Real-life-compatible comparison of Pandas DataFrames in Python unit tests

... sounds easy, right? Often, the `pandas.DataFrame.equals` function does the job.
According to [the docs](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.equals.html),
this function

> [...] allows two Series or DataFrames to be compared against each other to see if they have the same shape and elements. NaNs in the same location are considered equal. The column headers do not need to have the same type, but the elements within the columns must be the same dtype.

So if you have two DataFrames and want to know if they are really, truly equal, and don't want to know anything else, this is fine.
However, when writing unit tests, you might desire two other things:

1) For floating point values, testing for (strict, bit-wise) equality is often not practical, because tiny differences in value might
   still count as 'equal' in the sense of your test. Often, two floats computed with the same logic but with different code, 
   are not bitwise equal due to round-off errors.
   The `pytest` test package has a handy solution for this: comparing like `assert a == pytest.approx(b)` allows for tiny
   differences to still evaluate as true assertion.
   
2) When the DataFrames are _not_ equal, it is very handy to get some information on how they differ, so that you can hunt down bugs
   or refine your test code. The pandas-internal function gives you `True` or `False`, and nothing else.


## Help yourself, please

Here is a little helper function that I use when comparing DataFrames in `pytest` unit tests.
It uses approximate comparison for `float` values and strict comparison otherwise.
Also, if the DataFrames are unequal, it tells you a bit about where they differ.
The index and column order doesn't have to be equal between the DataFrames.

```python
import math
import pytest

def compare_dataframes(a, b):
    assert len(a) == len(b), f"Different number of rows, {len(a)} vs. {len(b)}"
    assert len(a.columns) == len(b.columns), f"Different number of columns, {len(a.columns)} vs. {len(b.columns)}"
    for idx, row in a.iterrows():
        for col, val in row.items():
            other = b.loc[idx, col]
            if isinstance(val, float):
                if math.isnan(val):
                    assert math.isnan(other)
                else:
                    assert val == pytest.approx(
                        other
                    ), f"Values do not match: {val:f} and {other:f}, in {str(idx)} {str(col)}"
            else:
                assert (
                    val == other
                ), f"Values do not match: {str(val)} and {str(other)}, in {str(idx)} {str(col)}"
```

Enjoy, and go test!

<<< Go back to the [table of contents](../README.md) || Opinions are mine, not necessarily those of [Vebeto GmbH](https://www.vebeto.de)