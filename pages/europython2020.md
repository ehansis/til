# My Picks from EuroPython 2020

The [EuroPython 2020 conference](https://ep2020.europython.eu/) took place as an online-only event on Jul 23 and 24 this year.
Big thanks to all the organizers for setting up such an engaging and (almost) flawless online conference!
Here is a selection of talks and other news that I found interesting, along with my notes.

The talks will be uploaded to YouTube once they are cut and prepared. I assume you will
find them in the [EuroPython YouTube channel](https://www.youtube.com/user/PythonItalia) in a few weeks.

(Bonus at the end of this post: Guido van Rossum's predictions for Python package managers!)


##  Elias Mistler: How to write multi-paradigm code 

* Well-prepared and interesting talk, slides are [here](https://github.com/eliasmistler/europython2020-multi-paradigm-sudoku/blob/master/multi-paradigm%20slides.pdf).
* Recommendation: implement functionality in pure functions, reference those in in a shallow wrapper/wiring class.
* Try to use immutable data structures. This also enables method chaining. If needed, use a mix of mutable/immutable processing with a switch, like Pandas does it.

Python packages to try out:
* [toolz](https://pypi.org/project/toolz/): utility functions for iterators, functions, and dictionaries. 
  This includes `thread_last` ([docs](https://toolz.readthedocs.io/en/latest/api.html?highlight=thread#toolz.functoolz.thread_last))
  for piping values through a sequence of functions.
* [schema](https://pypi.org/project/schema/): Definition and validation of Python data structures.


##  Ruud van der Ham: Attractive GUIs with PySimpleGUI  

* [PySimpleGUI](https://pypi.org/project/PySimpleGUI/) looks really nice, and simple!


##  Eyal Trabelsi: Elegant Exception Handling 

* Many of basic and advanced ideas about exception handling.
* `assert` not recommended in general: wrong exception type, might be compiled away
* `@typechecked` decorator from `pytypes`: type-check function inputs at runtime
* Slides are [here](https://ep2020.europython.eu/media/conference/slides/5PDef3W-elegant-exception-handling.html)

Python packages to try out:
* [returns](https://returns.readthedocs.io/en/latest/index.html): exception handling for functional programming


##  Sangarshanan Veeraraghavan: Interactive Mapmaking with Python 

* Nice overview of packages and approaches
* [Kepler](https://github.com/keplergl/kepler.gl/tree/master/bindings/kepler.gl-jupyter) (by MapBox) - this one was new to me, looks very polished
* Altair, Bokeh, Plotly - regular plotting libs that also can be used for maps
* [Geopatra](https://github.com/Sangarshanan/geopatra) - wrapper around other libs, written by the presenter


##  Ivana Kellyerova: How to Avoid Becoming a 10x Engineer 

This was probably the most memorable talk of the conference, but I wouldn't be able to summarize it here.
Go watch the video later!

(Important takeaway: BS = Balsamico Sauce)


## Other learnings

* A `retry` decorator comes in handy, e.g. when doing network requests. There
  are various implementations out there, like [this one](https://github.com/invl/retry) or the one from the `tenacity` package.
* Don’t use lambda functions in list comprehensions. The lambda function would be re-defined in each loop! Use def instead.
* Use `assign` to create new columns in Pandas, this enables method chaining.
* Simple `raise` statement re-raises the caught exception in an except block (had forgotten about that one...)


## Guido van Rossum's Keynote

* This was 45 minutes of Q&A with Guido, very interesting.
* Static type checking is probably not going to be part of the interpreter. Statically typed Python is sometimes less powerful than full dynamic Python, so it would have to be possible to turn off static type checking where needed. It’s better to leave that outside the interpreter and use it when desired.
* Integrating `mypy` into the standard library would slow down their development, as the standard library only moves slowly.
* Advice to young programmers: "Have fun at work but let yourself still be distracted by other things besides work."

And, finally, Guido's prediction on Python package management:

> "Only pip and conda will survive. Avoid pipenv or poetry, they aren't enough mainstream. The multiple config files will eventually converge."

I have been relying on Conda for a long time, but recently thought about switching to one of the "new" options.
Reading this comment means that I will stay with Conda at least for a bit longer.




<<< Go back to the [table of contents](../README.md) || Opinions are mine, not necessarily those of [Vebeto GmbH](https://www.vebeto.de)