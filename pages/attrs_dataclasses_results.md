# Wrap your Python analytics results in a dataclass or attrs

When writing data queries or analysis functions, it is often necessary to pass back multiple result values.
As an example, let's assume that you write a query function for the average number of posts per day for a user, 
which passes back 

* the user's numerical ID,
* the user's nick name,
* the total number of posts by that user and
* the average number of posts per day.

## Your options

In Python, there are various ways you could implement that return value.
You could pass back a regular ``tuple``, a ``namedtuple``,  a ``dict``, a hand-written result class
or a special data class implemented with the [attrs](https://pypi.org/project/attrs/) package
or, since Python 3.7, a [dataclass](https://docs.python.org/3.7/library/dataclasses.html#dataclasses.dataclass).

All of these have their pros and cons, the ``attrs`` docs include [a nice write-up](https://www.attrs.org/en/stable/why.html) on that.
I want to advocate for ``attrs`` or ``dataclasses`` because:

* they reduce the probability of errors, compared to ``tuple``, ``namedtuple`` and ``dict``, by
  providing a clear description of the available data fields and how to access them;
* they allow for type annotation of the data fields;
* and they are much quicker to implement and offer more functionality than hand-coded classes. 

**Note:** To install ``attrs``, do ``pip install attrs``. The pip package ``attr`` without the 's' is a different package!
Nevertheless, after installing ``attrs`` you import it as ``attr``, without the 's'. 


## Example class

Using ``attrs``, the result object for the above query could look like this:

```python
import attr

@attr.s
class UserAveragePosts:
    user_id = attr.ib()  # type: int
    nick = attr.ib()  # type: str
    total_posts = attr.ib()  # type: int
    avg_posts_per_day = attr.ib()  # type: float
```

The query function instantiates a result object like this, for passing back the query results:
```python
r = UserAveragePosts(
    user_id=5,
    nick="Douglas",
    total_posts=42,
    avg_posts_per_day=0.21
)
```

## Type annotations

I'm not sure that the type annotations for the data fields work correctly under all circumstances. 
Yet, in PyCharm I get a warning when trying to instantiate with the wrong type.
So writing
```python
r = UserAveragePosts(
    user_id=5,
    nick="Douglas",
    total_posts="too many",
    avg_posts_per_day=0.21
)
```
gives me a warning ``expected type 'int', got 'str' instead`` for the ``total_posts`` field.


## Bonus 1: JSON serialization

A nice bonus of the ``attrs``-based result type is that it can very quickly be serialized to JSON.
This way, you can use the result class itself inside your code, and you can serialize the results as JSON
if you want to return them in a web API.

Serializing our example result ``r`` as JSON is as simple as
```python
import json
json.dumps(attr.asdict(r))
```

This gives you:
```json
{"user_id": 5, "nick": "Douglas", "total_posts": 42, "avg_posts_per_day": 0.21}
```

If you wanted to pass back the JSON data from a [Flask](https://flask.palletsprojects.com) app, you could build a simple endpoint like this:
```python
from flask import jsonify

@app.route('/avg_posts')
def average_posts():
    # r = ... query call ...
    return jsonify(attr.asdict(r))
```

The ``attr.asdict()`` function used for the serialization also works recursively. 
Let's define a nested result type for top-rated posts:
```python
from typing import List
import attr

@attr.s
class PostMetadata:
    id = attr.ib()  # type: int
    title = attr.ib()  # type: str
    rating = attr.ib(default=0)  # type: float


@attr.s
class TopRatedPosts:
    user_id = attr.ib()  # type:int
    posts = attr.ib()  # type: List[PostMetadata]
```

Then we can instantiate and serialize a nested object (note also the `default` argument used for ``rating``):
```python
r = TopRatedPosts(
    user_id=5,
    posts=[
        PostMetadata(id=3, title="Three incredible Python tricks", rating=9.9),
        PostMetadata(id=9, title="You will not believe this", rating=7.2),
        PostMetadata(id=2, title="Lorem Ipsum"),
    ]
)

print(json.dumps(attr.asdict(r), indent=4))
```

This gives us:
```json
{
    "user_id": 5,
    "posts": [
        {
            "id": 3,
            "title": "Three incredible Python tricks",
            "rating": 9.9
        },
        {
            "id": 9,
            "title": "You will not believe this",
            "rating": 7.2
        },
        {
            "id": 2,
            "title": "Lorem Ipsum",
            "rating": 0
        }
    ]
}
```


## Bonus 2: Derived attributes

In my work at [Vebeto](https://www.vebeto.de) I often have to format numerical query results as strings for showing them
in HTML or LaTeX documents.
Instead of scattering the formatting function calls throughout my code, this can be directly incorporated into the results objects.
To do this, I have implemented a small 'derived attribute' extension for ``attrs``, that automatically computes attribute values
based on other attributes.
For example, a string field ``rating_str`` would automatically be generated from the numerical field ``rating``.
This is the topic of a separate, future post.

In ``dataclass`` objects, it appears that something similar could be done using
[post-init processing](https://docs.python.org/3.7/library/dataclasses.html#post-init-processing).
I have not tried that myself, though.


<<< Go back to the [table of contents](../README.md) || Follow on [twitter](https://twitter.com/EberhardHansis)