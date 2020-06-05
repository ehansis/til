# Quick derived attributes in Python attrs classes

In a [previous post](attrs_dataclasses_results.md) I described how I use the Python ``attrs`` package
to wrap analytics results. 
At the end I mentioned derived attributes, and this is what I want to describe here.


## What I want

One of my primary uses for the derived attributes is string formatting of numerical results.
Let's use the same example class as in the [previous post](attrs_dataclasses_results.md):
```python
import attr

@attr.s
class UserAveragePosts:
    user_id = attr.ib()  # type: int
    nick = attr.ib()  # type: str
    total_posts = attr.ib()  # type: int
    avg_posts_per_day = attr.ib()  # type: float
```

For showing those data in a web interface, I want nice string representations of ``total_posts``
and ``avg_posts_per_day``.
The former I want with a narrow non-breaking space (unicode ``U+202F``) as thousands separator,
the latter as float with 1 decimal digit and a comma as decimal separator (German style!).

<<< Go back to the [table of contents](../README.md) || Follow on [twitter](https://twitter.com/EberhardHansis)