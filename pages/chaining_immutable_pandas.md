# Chaining Immutable Pandas


## (Im)mutability

In many programming languages you have the choice of using either mutable or immutable objects.

Mutable objects can be changed in-place.
For example, a list in Python is mutable.
I can create a list and change its data:
```python
a = []
a.append(32)
a.clear()
```

Tuples, on the other hand are immutable.
Once I create a tuple, I cannot change it:
```python
t = ("foo", "bar")
```
I can access its contents, e.g. doing
```python
print(t[1])
```
But changing it causes an error:
```python
t[1] = 17
```
```
TypeError: 'tuple' object does not support item assignment
```


# Optional mutability

In [Pandas](https://pandas.pydata.org/), the main objects for managing data are Series (a single column of data)
and DataFrames (multiple columns).
For most operations in Pandas, you have the option to either use them in a mutable or in an immutable way.
For example, we can set an Index in-place (i.e. treat the DataFrame as a mutable object):
```python
import pandas as pd

df = pd.DataFrame([[1, 2, 3], [4, 5, 6]])
df.set_index(pd.Index(["a", "b"]), inplace=True)
print(df)
```
```
   0  1  2
a  1  2  3
b  4  5  6
```

Alternatively, we can treat the DataFrame as an immutable object and not use the `inplace=True` option.
Then, `set_index()` returns a new copy of the DataFrame with the Index set.
The original DataFrame stays unchanged:
```python
df = pd.DataFrame([[1, 2, 3], [4, 5, 6]])
df_with_index = df.set_index(pd.Index(["a", "b"]))
print(df)
print()
print(df_with_index)
```
```
   0  1  2
0  1  2  3
1  4  5  6

   0  1  2
a  1  2  3
b  4  5  6
```

Note that, if you confuse the mutable with the immutable usage, you might get unexpected results.
Using the mutable operation like  
```python
df2 = df.set_index(pd.Index(["a", "b"]), inplace=True)
```
will result in `df2` being `None`, since the immutable operation doesn't return anything.
Similarly, doing
```python
df.set_index(pd.Index(["a", "b"]))
```
without the `inplace=True` and without assigning the method output to a new variable will cause nothing to happen,
since `df` stays unchanged and the method output, the new DataFrame with the index set, is thrown away.


## Should I mutate or should I not?

If you need a simple rule of thumb: _Avoid mutable operations whenever possible._ The only good reason I can think of
for preferring mutable operations is, if your data is so large that you cannot afford copies of it being made.
On the contrary, there are a bunch of good reasons for using immutable operations:

### Readability

If I compare reading
```
df = df.set_index('some_column', drop=False)
```
to reading
```
df.set_index('some_column', inplace=True, drop=False)
```
I find the first version easier to comprehend. There is an assignment, I know where things go, and
I don't have to hunt for an `inplace=True` parameter somewhere in the function call.

### Functional style

[Functional programming](https://en.wikipedia.org/wiki/Functional_programming), or programming in a functional style
in a general-purpose language like Python, has some nice advantages.
Code written in a functional style can be much easier to test, comprehend and compose.

Ideally you write only pure functions, i.e. ones that always return the same result when called with the same arguments
and cannot be affected by mutable state or side effects.
Mutating the state of an input object would be an undesirable side effect, so use immutable operations only.

### Method chaining

Many of the DataFrame and Series methods can be chained, for conciseness and readability.
For example, compare this
```python
df = pd.DataFrame([[1, 2, 3], [4, 5, 6]], columns=['A', 'B', 'C'])
df.set_index(pd.Index(["a", "b"]), inplace=True)
df['D'] = [17, 42]
df = df.sort_values(by='B')
df.describe()
```
with this
```python
(
    pd.DataFrame([[1, 2, 3], [4, 5, 6]], columns=['A', 'B', 'C'])
    .set_index(pd.Index(["a", "b"]))
    .assign(D=[17, 42])
    .sort_values(by='B')
    .describe()
)
```
(The parentheses save me from having to append backslashes for line continuation).

Sure, the chained style is not always the right way to go. For instance, it can make debugging harder.
But, with mutable operations you couldn't even use it if you wanted to.

Note that for some immutable operations in Pandas there are special commands, like the `assign` used here
to append a column.

### Immutable surprises

Sometimes mutability can cause surprising behaviour (and surprises are bad).
Consider the following script:
```python
import pandas as pd

sales = pd.DataFrame([
    dict(item='Quinoa', unit_price=3.99, quantity=5, position=0),
    dict(item='Kale', unit_price=1.49, quantity=3, position=1),
    dict(item='Kombucha', unit_price=5.49, quantity=1, position=2),
])
sales.set_index('position', inplace=True)
print("\nSales:\n", sales)

totals = sales
totals.set_index('item', inplace=True)
totals = totals['unit_price'] * totals['quantity']
print("\nTotals:\n", totals)
```

The first `print` shows us the `sales` data, indexed by the `position` on the bill:
```
Sales:
               item  unit_price  quantity
position                                
0           Quinoa        3.99         5
1             Kale        1.49         3
2         Kombucha        5.49         1
```

The second `print` shows the total revenue per item:
```
Totals:
 item
Quinoa      19.95
Kale         4.47
Kombucha     5.49
```

**Question:** If we printed `sales` again, what would be its index?

**Answer:** Not `position`, as you might have expected:
```
          unit_price  quantity
item                          
Quinoa          3.99         5
Kale            1.49         3
Kombucha        5.49         1
```

The line `totals = sales` bound `totals` to the same DataFrame as `sales`, and the following
in-place operation `totals.set_index('item', inplace=True)` changed that DataFrame.
The `position` information from the index is now lost forever!
If we had used immutable operations everywhere, this particular problem could not have occurred.
