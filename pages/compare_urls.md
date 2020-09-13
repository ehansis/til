# Comparing URLs for Equality in Python Unit Tests

When you are writing unit tests for a web app, you sometimes need to compare URLs for equality.
For example, if you show links on a page and want to check them in a unit test, you could parse
out the links from the respective HTML elements and compare them to their expected values.
However, if your links include query strings and encoded arguments, things can get tricky.
The following two links are functionally equivalent, because ordering of arguments in query strings doesn't matter
and `%20` encodes a space:
```
https://foo.bar/app?user=me&password=sec%20ret&page=3
https://foo.bar/app?page=3&user=me&password=sec ret
```
Also, differently encoded URLs should be considered equal, like the following two:
```
https://foo.bar/posts/My+first+post
https://foo.bar/posts/My%20first%20post
```

Simple string comparison won't work. 
But, as so often, StackOverflow has you covered!


## Thank you, twneale!

[This answer](https://stackoverflow.com/a/9468284/13649423) by [twneale](https://stackoverflow.com/users/120991/twneale) on SO
includes a very handy piece of code for URL comparison.
Here it is (the Python 3 part only, slightly reformatted, 
licensed as [CC-BY-SA 3.0](https://creativecommons.org/licenses/by-sa/3.0/)):
```python
from urllib.parse import urlparse, parse_qsl, unquote_plus


class Url(object):
    """A url object that can be compared with other url objects
    without regard to the vagaries of encoding, escaping, and ordering
    of parameters in query strings."""

    def __init__(self, url):
        parts = urlparse(url)
        _query = frozenset(parse_qsl(parts.query))
        _path = unquote_plus(parts.path)
        parts = parts._replace(query=_query, path=_path)
        self.parts = parts

    def __eq__(self, other):
        return self.parts == other.parts

    def __hash__(self):
        return hash(self.parts)
```


It is used as follows:
```python
u1 = Url("https://foo.bar/app?user=me&password=sec%20ret&page=3")
u2 = Url("https://foo.bar/app?page=3&user=me&password=sec ret")
print(u1 == u2)

u1 = Url("https://foo.bar/posts/My+first+post")
u2 = Url("https://foo.bar/posts/My%20first%20post")
print(u1 == u2)
```
Running this prints `True` two times.


## Breaking down

Let's break down the `Url` class a bit, because there are some interesting things to learn here.

Upon instantiation, the `__init__` function first runs the provided `url` through `urlparse` ([docs](https://docs.python.org/3/library/urllib.parse.html#urllib.parse.urlparse)).
This returns `parts`, which is a named tuple.
Here is the result of `parts` for the first example URL `u1` used above:
```text
ParseResult(scheme='https', netloc='foo.bar', path='/app', params='', query='user=me&password=sec%20ret&page=3', fragment='')
```
So this breaks down the URL into its constituent parts (surprise, surprise!).

Next, the `query` part of the parsing result is passed through `parse_qsl` ([docs](https://docs.python.org/3/library/urllib.parse.html#urllib.parse.parse_qsl)).
This breaks down the query string into a list of key-value tuples, the result being
```text
[('user', 'me'), ('password', 'sec ret'), ('page', '3')]
```
This includes decoding of percent-encoded sequences into unicode characters (the space in `sec ret`).
Converting this list of tuples to a `frozenset` ([docs](https://docs.python.org/3/library/stdtypes.html?highlight=frozenset#frozenset)) 
returns something that is unchangeable and hashable and in which the order of items doesn't matter.
This means that two URLs with the same key-value query args (after decoding) but in different order will produce the same `frozenset`.

The `path` component of the URL is passed through `unquote_plus` ([docs](https://docs.python.org/3/library/urllib.parse.html#urllib.parse.unquote_plus)), which 
decodes percent-encoded characters and also converts pluses to spaces.
This is necessary for our second example shown above, to test that `My+first+post` and `My%20first%20post` are the same.

Finally, a new `parts` named tuple is built by injecting our `frozenset` version of the query string and the decoded `path`.
Note that `namedtuple._replace` looks like a protected member (and my IDE flags it as such) but it isn't really 
[intended to be one](https://softwareengineering.stackexchange.com/questions/315348/why-is-the-replace-method-of-python-namedtuple-classes-protected)
and calling it is fine.

So, what we end up with, is the URL parsed into its constituents, with encoding differences removed from the path
and differences in order and encoding removed from the query string. Very handy.

Finally, the `__eq__` function tells Python to compare `Url` objects by comparing the `parts`, and hash them
by hashing the `parts`.