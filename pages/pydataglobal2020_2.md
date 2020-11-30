# PyData Global 2020, Episode 2/3

This is part two of a series of posts on [PyData Global 2020](https://global.pydata.org/).

* [Part one](pydataglobal2020_1.md) is about the conference format, data analysis methods and handy tools.
* The second post (this one here) is about ML model explainability and some advanced Pandas stuff.
* The [third](pydataglobal2020_3.md) post will feature data visualization topics.


### Quickly deploying explainable AI dashboards, by Oege Dijk

"AI" is everywhere, and many practitioners worry about being able to explain how their models actually get to their results.
To help the explainability of AI models, Oege built an [explainer dashboard](https://github.com/oegedijk/explainerdashboard),
with which you can quickly and comprehensively analyze various aspects of a model.
It shows feature importances, model performance and individual predictions; it lets you play with 'what-if' scenarios in which
you change feature values and see the change in the outcome; it analyzes feature dependence and some more...
You can wrap many of the usual [scipy-learn](https://scikit-learn.org/stable/index.html) models to
instantly get your explainer dashboard.
See his [online demos](http://titanicexplainer.herokuapp.com/) for further details.

I could imaginge this being a very valuable tool for education purposes, or when you just start exploring
options for modelling a particular problem.


### Opening the Black Box, by Ben Fowler and Chelsey Kate Meise

This talk was mainly an introduction into [SHAP scores](https://github.com/slundberg/shap).
These can help you analyze how features impact the model output.
Check out the link for a more thorough explanation 🙃


### pandas.(to/from)\_sql is simple but not fast, by Uwe Korn

Uwe talked in great depth about the intricacies of storing and loading data to a SQL database, with [Pandas](https://pandas.pydata.org/).
If you are interested in the topic, have a look at [his slides](https://speakerdeck.com/xhochy/to-sql-is-simple-but-not-fast).

Here is what I took away: When you read data from SQL to a Pandas DataFrame, this happens via
a [SQLAlchemy](https://www.sqlalchemy.org/) connection.
SQLAlchemy reads data from the DB and converts them to lists of Python objects.
This is slow, because a lot of logic is involved in creating Python objects, much more than, for example,
working with the linear chunk of memory used in a NumPy array.
From this list of Python objects the DataFrame is created.
When writing to the database, more or less the inverse happens (DataFrame to Python objects to DB).

Much of the complexity in handling Python objects has to to with memory management.
The size (in memory) of the objects is not known in advance, so they cannot be handled in a simple format
like the NumPy array, in which each data object has a fixed number of bytes.
Instead, they have to be allocated one-by-one and managed in collections of memory pointers.
(This is a very rough description, obviously...)

This is where [Apache Arrow](https://arrow.apache.org/docs/index.html) comes in:

> Apache Arrow is a development platform for in-memory analytics. It contains a set of technologies that enable big data systems to process and move data fast. It specifies a standardized language-independent columnar memory format for flat and hierarchical data, organized for efficient analytic operations on modern hardware.

You can read quickly from a SQL database to Arrow, e.g. via [TurboDBC](https://turbodbc.readthedocs.io/en/latest/pages/advanced_usage.html#advanced-usage-arrow).
The Arrow memory forma requires far less memory management work than creating Python objects.
And, conversion from Arrow to Pandas is [built into Arrow](https://arrow.apache.org/docs/python/pandas.html), and it is fast!

If you don't want to go the Arrow route, there are other options for speeding up your Pandas to DB operations, in particular
when writing to the DB. See for example [here](https://naysan.ca/2020/05/09/pandas-to-postgresql-using-psycopg2-bulk-insert-performance-benchmark/) 
or [here](https://stackoverflow.com/questions/23103962/how-to-write-dataframe-to-postgres-table/47984180#47984180).



### What’s new in pandas?, by Joris Van den Bossche and Tom Augspurger

Joris and Tom gave a peek into the current Pandas development and upcoming features.
These included:

* Better integration of [numba](https://numba.pydata.org/), e.g. for custom rolling windows functions
* Dedicated [string datatype](https://pandas.pydata.org/pandas-docs/stable/user_guide/text.html#text-data-types), avaliable from version `1.0` onwards 
  (previously strings were stored as `object` datatype, the same as for other generic Python objects)
* (Upcoming) Use Apache Arrow memory layout under the hood for decreased storage, use Arrow string operations
* (Upcoming) Common missing value indicator: `pd.NA` instead of `None`, `NaN`, `NaT`
* (Upcoming/experimental) New nullable datataypes for `bool` and `int` (currently, writing a `NaN` value into an `int` column will cause the whole
  column to be cast to `float`)
* (Upcoming) New logic for boolean operations and comparisons containing `NA` values


(Disclaimer: I tried my very best to accurately represent the presentations. Let me know in case I got something wrong.)


<<< Go back to the [table of contents](../README.md) || Opinions are mine, not necessarily those of [Vebeto GmbH](https://www.vebeto.de)