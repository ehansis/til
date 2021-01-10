# Indexing with floats in pandas or xarray is tricky!

## What's the matter?

Let's imagine that we are working with a time series `s` of characters, 
indexed with `t` in steps of 0.1 seconds:
```python
import pandas as pd
import numpy as np

t = np.arange(0, 1, 0.1)
s = pd.Series(data=list("abcdefghij"), index=t)

print(s)
```

This is what `s` looks like when printed:
```
0.0    a
0.1    b
0.2    c
0.3    d
0.4    e
0.5    f
0.6    g
0.7    h
0.8    i
0.9    j
dtype: object
```

So far, so simple. Now I want to know the value at `t = 0.6`:
```python
print(s.loc[0.6])
```

But, oh no, I get a
```
KeyError: 0.6
```

What happened? Let's look more closely at the time index value that we wanted to look up:
```python
print(t[6])
```
```
0.6000000000000001
```

So, for some reason (probably a very good reason, but I haven't researched it)
the construction of our time index `t` with `np.arange` resulted in a value
that is just a tiny bit larger than `0.6`.
That's why our lookup fails - these two floats are not equal.

This demonstrates the main point of this article: If you use floats in index-based lookups,
you are up for some interesting problems and surprises whenever you use
lookups that require strict equality.
The string representations of floats (e.g. what you see in the `print(s)` output above)
may be rounded, so you can't rely on those.


## What to do?

### First option: Use precise values
We could use the precise value for the lookup, if possible: `print(s.loc[t[6]])` works and correctly
prints a `g`.

### Use slices

We can also index using slices:
```
print(s.loc[0.6: 0.8])
```
works and prints 
```
0.6    g
0.7    h
0.8    i
dtype: object
```

Slices have their own gotchas though. The [pandas docs](https://pandas.pydata.org/pandas-docs/stable/user_guide/indexing.html) note that
> Note that contrary to usual Python slices, both the start and the stop are included, when present in the index! See [Slicing with labels](https://pandas.pydata.org/pandas-docs/stable/user_guide/indexing.html#indexing-slicing-with-labels) and [Endpoints are inclusive](https://pandas.pydata.org/pandas-docs/stable/user_guide/advanced.html#advanced-endpoints-are-inclusive).

Then, there are [rules](https://pandas.pydata.org/pandas-docs/stable/user_guide/indexing.html#indexing-slicing-with-labels) on slicing with non-existent labels:
> When using .loc with slices, if both the start and the stop labels are present in the index, then elements located between the two (including them) are returned: [...]
> 
> If at least one of the two is absent, but the index is sorted, and can be compared against start and stop labels, then slicing will still work as expected, by selecting labels which rank between the two: [...]
> 
> However, if at least one of the two is absent and the index is not sorted, an error will be raised (since doing otherwise would be computationally expensive, as well as potentially ambiguous for mixed type indexes).

In the example above, the label `0.6` is absent (in the sense of strict equality), but our index is sorted and can be compared against the labels, so everything between `0.6` and `0.8` (inclusive!)
is returned. Note, that `0.8` happens to be included exactly in the index and is included in the output.

Can we look up a single value this way? Not easily:
```python
print(s.loc[0.6: 0.6])
```
will yield an empty Series. Our index contains `0.6000000000000001`, so there are no values
between `0.6` and `0.6`. What would work is something like `s.loc[0.599: 0.601].iloc[0]`.

Also, the following may come as a surprise:
```python
print(s.loc[0.4: 0.6])
```
yields
```
0.4    e
0.5    f
dtype: object
```
Why do we get `0.8` included in `s.loc[0.6: 0.8]` but not `0.6` in `s.loc[0.4: 0.6]`?
Well, our index contains a value slightly larger than `0.6`, so that element is not 
between `0.4` and `0.6`.

To summarize: You can use slices for inexact lookups, to get values inside a certain range.
But, you have to know exactly what you are doing, or you may be surprised by the results
around the edges of the lookup.

What I like to do is make the inclusion (or exclusion) of the endpoints explicit, by adding
a bit of slack to the lookup that is smaller than the increment between the index values:
```python
print(s.loc[0.59: 0.81])
```
Of course, this requires that you know the (minimum) increment across the index.


### Use nearest-neighbor lookups

Another option is to explicitly use nearest-neighbor lookups.
In pandas there are various methods for implementing this, using `argsort`, interpolation 
from `scipy`, ... If you do a [search in StackOverflow](https://stackoverflow.com/search?q=pandas+nearest-neighbor) you can get plenty of inspiration.


## The same in xarray

In pandas, float-based lookups might be rarely necessary (at least, I can't remember ever having
needed them). They might arise if you are dealing with lots of time-series data with float timestamps.
However, in typical xarray use cases they occur all the time: xarray is often used to process
geospatial raster data on longitude/latitude grids that are represented as float numbers.
Selecting grid cells or subsets by coordinate necessarily requires you to do float-based lookups.
And the intricacies of float representation mean that you cannot be sure of the precise coordinate
values after file I/O, resampling or other operations on the grid.

The xarray package has built-in support for [nearest-neighbor lookups](http://xarray.pydata.org/en/stable/indexing.html#nearest-neighbor-lookups).
Let's define a test array `a`:
```python
import xarray as xr

a = xr.DataArray(data=range(10), coords=[("t", t)])
print(a)
```
which prints as
```
<xarray.DataArray (t: 10)>
array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
Coordinates:
  * t        (t) float64 0.0 0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9
```

Straight float-based selection has the same issues as in pandas: both `a.sel(t=0.6)` and the 
equivalent `a.loc[dict(t=0.6)]` result in a `KeyError: 0.6`.

However, we can say
```python
print(a.sel(t=0.6, method='nearest'))
```
which prints
```
<xarray.DataArray ()>
array(6)
Coordinates:
    t        float64 0.6
```

Nearest-neighbor-based lookup is _not_ available for `.loc[]` though, 
which also means that you cannot do assignment with nearest-neighbor indexing 
(the [xarray docs](http://xarray.pydata.org/en/stable/indexing.html#assigning-values-with-indexing) say "Do not try to assign values when using any of the indexing methods `isel` or `sel`".)
This is reasonable - assignment with nearest-neighbor lookups could result in weird
behaviour, e.g., when you assign two different values that map to the same array element
after nearest-neighbor matching.

Slicing in xarray works similar to pandas.
With `.loc[]` and slices we can also do assignment:
```python
a.loc[dict(t=slice(0.59, 0.81))] = 17
print(a)
```
which results in
```
<xarray.DataArray (t: 10)>
array([ 0,  1,  2,  3,  4,  5, 17, 17, 17,  9])
Coordinates:
  * t        (t) float64 0.0 0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9
```
Note that I dis-ambiguated the start/end coordinates of my slice as recommended above, 
by adding a bit of slack.

(Note: This was tested with xarray version 0.16.2 and pandas version 1.1.5.)

<<< Go back to the [table of contents](../README.md) || Opinions are mine, not necessarily those of [Vebeto GmbH](https://www.vebeto.de)