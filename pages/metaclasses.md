# Mysterious Metaclasses

The Python `metaclass` concept may be unknown or mysterious to you - at least it was and still is to me.
I'm not going to try and explain metaclasses here, because I would probably get the details wrong and 
[other people](https://duckduckgo.com/?q=Python+metaclass) have done a better job doing that.


## Why???

What I want to offer you first is my (current) understanding of what metaclasses are good for:
By applying a metaclass to some base class, you can intercept the construction of derived classes from the base class
and influence the construction of the derived class. 

For example, using a metaclass you could define constraints that all classes derived from
your base class have to meet, without knowing about or touching the derived classes.
This is the example shown in James's video (see below).

Another application would be to perform some kind of task for each class that is being derived from your base class.
For example, I'm using this in my code to perform an automatic 'registration' of classes (see belower).


## Go watch a video

The incomparable [James Powell](https://talks.dutc.io/) has given a talk 
entitled ["So you want to be a Python expert"](https://www.youtube.com/watch?v=cKPlPJyQrt4) at PyData 2017. 
In it, he talks about several Python "expert" topics, and metaclasses are one of them (starting around minute 21:00).
The rest of the talk is well worth your time, too, if you want to learn about "dunder" methods, decorators, generators and context managers.


## Automatic class registration

In my own programming endeavours, I have used metaclasses only rarely.
However, here's an example of where I found them quite useful:

I am defining 'filter' classes that perform some filtering task on data (the details don't matter here).
All filter classes derive from a common base class `FilterBase`.
However, I would like to have a registry of all the filters that I wrote, i.e., of all classes derived from `FilterBase`.
This is where the metaclass `FilterRegistration` comes in:

```python
filter_registry = {}


class FilterRegistration(type):
    def __init__(cls, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if cls.__name__ != 'FilterBase':
            filter_registry[cls.__name__] = cls


class FilterBase(metaclass=FilterRegistration):
    # base class code goes here...
    pass
```

By applying `FilterRegistration` as a metaclass to `FilterBase`, the `FilterRegistration.__init__` method
is called upon construction of each derived class.
In it, the derived class is added to a (global) dictionary `filter_registry`, keyed by the class name,
unless it is the base class itself.

Now I can define a derived filter class like this:
```python
class MyFilter(FilterBase):
    # class code goes here
    pass
```

This class is automatically added to the filter registry, which looks like this if `print`ed: 
```
{'MyFilter': <class '__main__.MyFilter'>}
```

So I can happily go about coding all my filters, never having to worry about filling the filter registry again.
