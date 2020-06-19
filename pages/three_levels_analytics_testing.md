# Three Levels of Testing in Data Analytics

Software engineers have long known that automated testing is an indispensable tool for building good software.
Among the most famous testing approaches is [TDD - Test Driven Development](https://en.wikipedia.org/wiki/Test-driven_development),
which involves short cycles of writing tests _first_ and then the features that make the tests pass.

Data analytics people (Data Engineers, Data Scientists, Data Analysts, or whatever else you care to call yourself)
also write software, in a sense.
They use full-featured programming languages, script languages or GUI-based tools to define data flows,
analysis processes and visualization.
However, I often get the impression that testing is not so much of a priority in the data analytics world.

Is that OK? Well, if you only ever work on your own little toy problems and if nobody makes decisions
based on your analytics, not even you, it probably is.
But as soon as your work might influence business decisions, policy, science or something else of importance,
I want to claim that doing data analytics without automated testing is reckless and unprofessional.

``rant start``
Granted, if you work with some [colorful](https://www.qlik.com) [pointy-clicky](https://www.tableau.com) [tool](https://powerbi.microsoft.com/)
or even a [spreadsheet](https://products.office.com/excel), your technology choice makes it very hard to implement proper testing.
Such tools also tend to hide the complexity of your analysis, raising the risk for [mistakes](http://www.eusprig.org/horror-stories.htm).
Pairing this with the fact that version control and true collaborative work are close to impossible with these tools
(anybody up for merging changes from the 'workbooks' of three colleagues into one?) makes me wonder
why such tools are used at all for important data anlytics work in professional environments.
``rant end``


## Not quite TDD

Personally, I try to follow TDD when I can, but TDD doesn't seem to be a good fit for exploratory data work.
I often don't know exactly where I'm going with the analysis when I start it, so applying TDD is hard.

Also, I find it hard to strike a balance between maintaining the fun of data analysis and being diligent with testing.
Ideally, I should test all parts of my code for all possible combinations of input data and all edge and corner cases.
Even if that was possible, it's not what I could get myself (or probably any other data person) to do.

So what I want to outline here are three levels of testing that I apply in my analytics workflows.
I mainly code in Python, so I will reference tools and methods from the Python ecosystem.
The ideas themselves can probably also be implemented in any other (code-based, mousing-free) toolset.


## Level 1: assert

The good old ``assert`` statement is very simple and effective for adding a bit of testing to your code.
An ``assert`` statment checks that a certain condition is met. If not, it raises an exception (which usually stops the application).

Let's consider a simple example: You are analyzing sales data and want to know the revenue share of your product categories.
So you might have code like this:
```python
category_revenue = sales.groupby('category')['price'].sum()
category_share = category_revenue / category_revenue.sum()
```

This is quite straightforward, and you will probably get the desired result.
But if you want to be a bit more certain about your calculations, you could add an ``assert`` statement like this:
```python
assert abs(category_share.sum() - 1) < 1.0e-6, "Inconsistent category share"
```

This tests that the revenue shares of the different product categories actually add up to 1 (leaving a bit of wiggle room for round-off errors).
If this condition is not met, it prints the error message ``"Inconsistent category share"`` and stops execution.

I like to use ``assert`` statments whenever I know that something non-trivial should be true in the code.
Some other examples:

* Check that numbers are non-negative or non-zero, when they are supposed to always be
* Check that the number of rows and columns in tables match the expected values (e.g. the number of lines in an input file)
* Check that there are no NaN values where there should not be any


## Level 2: unit test

For more complex computations, implement unit tests.
I find this especially valuable for data transformations, numerical models or queries that can be separated out as functions.
For parts of the ETL pipeline I find this much harder to do - see Level 3 on that topic.

Unit tests are at the heart of 'classical' software testing.
You write a test that pipes synthetic inputs into your function and checks if the output is as expected.
You can find an example of a unit test in my recent post on [string representation of large numbers](sround.md).

Writing unit tests takes some discipline, especially if your are more in the exploratory mode and want to 
get some exciting analytics done.
But it hugely pays off in the long run.
Actually, I don't need to sing the praise of unit testing here, plenty of smart folks 
have [done that before me](https://duckduckgo.com/?q=why+should+i+do+unit+testing&ia=web).

Unit testing is also useful for checking your data visualizations, e.g. querying a data display from your web tool,
parsing the chart SVG and checking if what's in there actually matches your input data.
(Try doing that with Ex*el charts...)


## Level 3: consistency checks

It's very hard to prepare your code for any possible data that might be thrown at it.
But often you can define consistency checks on your input data, your intermediate results and your outputs, that give you a better
idea of how well things are going.

I got into writing checks after learning about the [TDDA - Test Driven Data Analytics](http://www.tdda.info) library
by Nicholas J. Radcliffe of [Stochastic Solutions](http://stochasticsolutions.com/).
I'm going to provide a brief glimpse into the 'constraints generation and verification' portion of that library.
Go check out the documentation and tutorials on [tdda.info](http://www.tdda.info) to learn more, I highly recommend it.

Imagine that your are analyzing a dataset about portrait paintings.
You scrape the data from [Wikidata](https://www.wikidata.org) and dump them into a Pandas DataFrame called ``df``.
You would like to know if the scraping worked.
But you also want check further runs of your pipeline that may result in different data, 
so you can't simply check against reference values.

With TDDA, you can automatically discover, and later verify, constraints on your data:

```python
from tdda.constraints.pd.constraints import discover_df
constraints = discover_df(df).to_json()
```

This yields constraints in JSON:
```json
{
    "fields": {
        "name": {
            "type": "string",
            "min_length": 17,
            "max_length": 65,
            "max_nulls": 0
        },
        "creator": {
            "type": "string",
            "min_length": 23,
            "max_length": 113,
            "max_nulls": 0,
        },
        "width": {
            "type": "real",
            "min": 0.24,
            "max": 2.076,
            "sign": "positive",
            "max_nulls": 0
        },
        "height": {
            "type": "real",
            "min": 0.28,
            "max": 1.83,
            "sign": "positive",
            "max_nulls": 0
        },
        "inception": {
            "type": "integer",
            "min": 1421,
            "max": 2019,
        }
    }
}
```

In this (partially fabricated) example, ``name`` is the painting name, which must not be empty (``"max_nulls": 0``)
and whose string length is between 17 and 65.
The constraints on the painting's ``creator`` are similar.
The painting dimensions ``width`` and ``height`` have numerical constraints.
The year of ``inception`` must be integer, within certain bounds, but may actually be empty if it is not known.
Note: TDDA detects those constraints from example data, automatically! Even if you need to modify them afterwards, TDDA provides an excellent starting point.

Now on any future pipeline run you can load those constraints and verify your data against them:
```python
from tdda.constraints.pd.constraints import verify_df, detect_df

# check if data meets constraints
result = verify_df(df, 'constraints_01.json')
print(str(result))

# determine failed constraint checks, write them to a file
detect_df(df, 'constraints_01.json', outpath='failures_02.csv', output_fields=[], per_constraint=True)
```

If your input data change, the constraints will sometimes complain about 'valid' data that fall outside
the prescribed ranges.
Then you will have to adapt the constraints after inspecting the data.
This might be a minor inconvenience, but you will get to actually check the data in question instead
of blindly piping everything through your analytics process.

I have built ELT pretty long and complicated ETL pipelines, in which each processing step was
followed by such a consistency check.
Often, I enrich my test tasks in the pipeline with additional consistency checks that fall outside
the domain of TDDA (e.g., checking that data is consistent between related objects).



