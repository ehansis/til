# Caching expensive function calls with the diskcache Python package

Caching is useful in many applications: Your web app needs to run fairly expensive database queries
to serve a page. Your numerical model computes certain results several times because they are needed
in different parts of the code.
Your data dashboard re-computes results anew each time the dashboard is opened.
In all these situations, performance can be greatly increased by caching the results of a function call
and making them instantly available for a repeat call with the same function arguments.


## Cache competitors

Here are a few options for implementing a cache (by no means an exhaustive selection):


### lru_cache

The very simplest cache is built right into the Python standard library: `functools.lru_cache` ([docs](https://docs.python.org/3/library/functools.html#functools.lru_cache)).
This stores the N last recently used (hence, LRU) results of a function call in a dictionary, in memory.
Using it is as simple as this:
```python
from functools import lru_cache

@lru_cache
def expensive_function(foo, bar):
    do_very_expensive_query(foo)
    do_expensive_computation(bar)
```

Calls to `expensive_function` are cached and repeated calls with the same arguments `foo` and `bar` are retrieved from the cache.
Note that the function arguments need to be hashable, since they are used as dictionary keys!


### dogpile.cache

`dogpile.cache` ([docs](https://github.com/sqlalchemy/dogpile.cache)) is a widely-used and mature cache package.
However, I personally found the API a bit too complicated and also experienced some unexplained deadlock issues
in multithreaded applications.


### redis

There are various implementations of using [redis](https://redis.io/) as a cache in Python, for example [python-redis-cache](https://github.com/taylorhakes/python-redis-cache).
I don't have experience with those, but they all require you to set up and manage a redis instance.


### DiskCache

The package I have liked best so far, for general-purpose use, is [DiskCache](http://www.grantjenks.com/docs/diskcache/).
This is a disk-based cache, so, unlike `functools.lru_cache`, you can easily handle many gigabytes of cached data
if you have a moderately large and fast disk.

The page claims the following benefits:

    Pure-Python
    Fully Documented
    Benchmark comparisons (alternatives, Django cache backends)
    100% test coverage
    Hours of stress testing
    Performance matters
    Django compatible API
    Thread-safe and process-safe
    Supports multiple eviction policies (LRU and LFU included)
    Keys support “tag” metadata and eviction
    Developed on Python 3.8
    Tested on CPython 3.5, 3.6, 3.7, 3.8
    Tested on Linux, Mac OS X, and Windows
    Tested using Travis CI and AppVeyor CI
    
The 'Thread-safe and process-safe' part are very important for web apps and other multi-process applications.
I haven't had any issues using diskcache in heavily parallelized environments so far.

There is a good [tutorial](http://www.grantjenks.com/docs/diskcache/tutorial.html) on how to get started setting up a cache.
Once you have done so, you can `get` and `set` single items by a key.

What I use most, though, is the `memoize` decorator which, like `functools.lru_cache`, caches function arguments and results.
Here is an example, copied from the above-mentioned tutorial:
```python
from diskcache import FanoutCache

cache = FanoutCache()

@cache.memoize(typed=True, expire=1, tag='fib')
def fibonacci(number):
    if number == 0:
        return 0
    elif number == 1:
        return 1
    else:
        return fibonacci(number - 1) + fibonacci(number - 2)
```

Without caching, the recursive calls to `fibonacci` would cause the function to be called over and over again.
With the `cache.memoize` deocorator, the result is cached for each `number` argument and the function is therefore
only called once for each `number`


## Cache be gone!

Once you have implemented a cache, you have gotten yourself a new problem, though: You need to think long and hard
about when the cache needs to be cleared or single results evicted.
Cached results may become outdated if, for example, data changes in your database.
If the arguments to your query function stay the same, the cache won't know about the changed data and retrieve an outdated result.
This can lead to some very confusing errors.
But, how to solve that depends very much on your specific application...