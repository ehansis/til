# Meaningful string representations for large numbers in Python

If you asked me for the current population of Brazil, I could tell you that it is [212,481,856](https://www.worldometers.info/world-population/) people.
This is far more accurate than you probably needed to know (and it's already outdated when you read this).
It's probably more helpful if I told you that Brazil's population is 212,000,000 people.

When presenting large numbers to the readers of your analytics reports and dashboards, it usually helps to limit the precision.
The additional digits don't add meaningful information and may distract. The numbers are harder to comprehend.
Even worse, you may generate the impression that your data is very accurate, which it maybe isn't
(in the example shown above, the number is an estimate from a model).

Be kind to your readers, be realistic with respect to the accuracy of your data, and limit the precision of large numbers in your data displays.


## My number formatting function

Here's the Python function that I use to format large numbers as meaningful strings.
You can select the number of relevant digits to show, an optional thousands separator, and whether you want to force a leading sign.

**Note:** 
This is designed for integer output.
Don't expect this to format ``0.01561`` as ``0.016``, you will get ``0`` instead.
See also the examples below.

```python
def sround(f, digits=2, thousands_sep=None, signed=False):
    """Compute rounded string representations of numbers with a fixed number of significant digits

    Inspired by https://stackoverflow.com/a/3411731

    Args:
        f (float): number to format
        digits (int): number of digits to retain
        thousands_sep (str or None): thousands separator
        signed (bool): with or without leading sign (negative numbers always have a leading '-')

    Returns:
        str: formatted number
    """
    s = ("%" + ("+" if signed else "") + ".0f") % float(("%." + str(digits) + "g") % f)

    if thousands_sep is not None:
        if s[0] in ["+", "-"]:
            sign = s[0]
            s = s[1:]
        else:
            sign = ""

        # process the numbers in reverse to insert the thousands separator, then reverse result
        r = s[::-1]
        s = (
            sign
            + thousands_sep[::-1].join([r[i: i + 3] for i in range(0, len(s), 3)])[::-1]
        )

    return s
```


## Testing, testing!

What could possibly explain this function better than its unit test?
Here it is!

```python
class TestSround:
    def test_default(self):
        assert sround(0.01234) == "0"
        assert sround(1.234) == "1"
        assert sround(1.8) == "2"
        assert sround(1234678) == "1200000"

    def test_digits(self):
        assert sround(1234, digits=1) == "1000"
        assert sround(1234, digits=3) == "1230"
        assert sround(1234, digits=5) == "1234"
        assert sround(123456, digits=5) == "123460"

    def test_thousands_sep(self):
        assert sround(0.01234, thousands_sep=" ") == "0"
        assert sround(1.234, thousands_sep=" ") == "1"
        assert sround(123.456, thousands_sep=" ") == "120"
        assert sround(1234.56, thousands_sep=" ") == "1 200"
        assert sround(1234678, thousands_sep=" ") == "1 200 000"
        assert sround(12346789, thousands_sep=" ") == "12 000 000"
        assert sround(123456789, thousands_sep=" ") == "120 000 000"

        assert sround(1234678, thousands_sep="foo") == "1foo200foo000"

        assert sround(-10, thousands_sep=" ") == "-10"
        assert sround(-100, thousands_sep=" ") == "-100"
        assert sround(-1000, thousands_sep=" ") == "-1 000"
        assert sround(-10000, thousands_sep=" ") == "-10 000"
        assert sround(-119000, thousands_sep=" ") == "-120 000"
        assert sround(-1000000, thousands_sep=" ") == "-1 000 000"

        assert sround(+10, thousands_sep=" ") == "10"
        assert sround(+1000, thousands_sep=" ") == "1 000"

    def test_signed(self):
        assert sround(0.01234, signed=True) == "+0"
        assert sround(1.234, thousands_sep=" ", signed=True) == "+1"
        assert sround(123.456, signed=True) == "+120"
        assert sround(1234.56, thousands_sep=" ", signed=True) == "+1 200"
        assert sround(1234678, signed=True) == "+1200000"
        assert sround(+10000, thousands_sep=" ", signed=True) == "+10 000"

        assert sround(-0, signed=True) == "+0"
        assert sround(-0.0, signed=True) == "-0"
        assert sround(-0.01234, signed=True) == "-0"
        assert sround(-1.234, thousands_sep=" ", signed=True) == "-1"
        assert sround(-123.456, signed=True) == "-120"
        assert sround(-1234.56, thousands_sep=" ", signed=True) == "-1 200"
        assert (
            sround(-1234678, signed=True, digits=4, thousands_sep="yay!")
            == "-1yay!235yay!000"
        )
```




<<< Go back to the [table of contents](../README.md) || Opinions are mine, not necessarily those of [Vebeto GmbH](https://www.vebeto.de)