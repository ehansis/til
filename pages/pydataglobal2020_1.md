# PyData Global 2020, Episode 1/3

This year saw the first ever [PyData Global conference](https://global.pydata.org/), hosted in an online format.
The conference ran over 5 days, from Nov 11 to Nov 15 2020, as a mix of pre-recorded talks, live sessions,
text chat and a 2D interactive meeting space (see below!).
Big thanks to the conference team and [NumFocus](https://numfocus.org/) for organizing this great event! 👏🏻

There was so much good stuff to see and hear at the conference that I will split my notes over three posts.
* The first (this one here) will be about the conference format, data analysis methods and handy tools.
* The [second](pydataglobal2020_2.md) will be about ML model explainability and some advanced Pandas stuff.
* The [third](pydataglobal2020_3.md) post will feature data visualization topics.


## My thoughts on the conference format

These are exciting times for online conferences: induced by Covid-19, we are in a great phase of experimentation
for technologies, communication methods and organizing patterns. Many things are being tried out, of which
95% will go away and 5% will determine how online conferences are held in the years to come.
I'm curious to see which formats will prevail in the long run.

PyData Global, being a conference with attendees from all time zones, required some special arrangements.
Talks were pre-recorded, with each day's talks released early in the morning on [NumFocus Academy](https://academy.numfocus.org/).
Communication happened in a [Mattermost](https://mattermost.org/) forum system and in
[Gather](https://gather.town/). The latter looks like an old-school 2D RPG game, in which conference participants
walk around a virtual meeting venue. (Go try it out, there is a free demo!) 
When two avatars get close to each other, video and audio feeds automatically pop up.
So, in theory, this enables casual, serendipitous communication, almost like in meat space.

The asynchronous, pre-recorded talks worked great for me, because I could watch exactly what I wanted
and when, being able to pause, speed-up or skip.
I had attended [EuroPython 2020](europython2020.md) as online conference before, which had synchronous talks, i.e.
live-streamed sessions in video broadcasts. This didn't offer the same convenience as pre-recorded talks, but it meant that
many people were watching the same talk at the same time, which lead to some lively discussion in the conference forums.
This wasn't so much the case at PyData, because everybody watched at their own schedule.

There was a range of live events scheduled in Gather and Zoom, including watch parties for talks, Q&A panels and 
social events. In the end, though, I found communication among the conference goers not as lively as at EuroPython.


## Talk selection, part 1

### Pint + SQLAlchemy = Unit consistency and enforcement in your database

This was a virtual poster presentation by [Robin Wilson](http://www.rtwilson.com/). 
The core idea: In your [SQLAlchemy](https://www.sqlalchemy.org/) ORM model classes,
provide an interface of property getters/setters that do unit conversions using the [Pint](https://pint.readthedocs.io/en/stable/)
package. The actual attribute value, which is synced to the database, is hidden.

Example: You have a model attribute `length` that is accessed via getters/setters.
With the described setup, you can define your model to 
always store the length in meters to the database, via the hidden attribute `_length`. 
If a user wants to store a `length` of 3 feet or 17 km, your interface will do the conversion to meters behind the scenes. 
There is an example of how this can be implemented [on GitHub](https://github.com/robintw/sqlalchemy-units-example).


## Multi-Label Classification with Human Rights Data

One of the keynotes was given by Megan Price & Maria Gargiulo from the [Human Rights Data Analysis Group (HRDAG)](https://hrdag.org/).
This group does enormously important work, providing data analytics and statistics for human rights cases.
The website emphasizes that:

> Inaccurate statistics can damage the credibility of human rights claims—and that’s why we strive to ensure that statistics about human rights violations are generated with as much rigor and are as scientifically accurate as possible.

Consequentially, a part of the presentation focused on their data analytics workflow (this is what I'm focusing on here, there was
a nice presenatation on the labelling problem from the title, too).
In HRDAG, analytics tasks are set up as self-contained, self-documenting units of work.
Each task contains (in a pre-defined folder structure) all the input data, code and documentation required to run the whole analysis.
Chains of processing steps are laid down in Makefiles.
The workflow is described [in a blog post](https://hrdag.org/2016/06/14/the-task-is-a-quantum-of-workflow/) by Patrick Ball,
that I recommend for reading.

The blog post also prescribes that
> In HRDAG’s workflow, the only way we produce a result is by executing code. That means we don’t use interactive tools like spreadsheets or GUI-based statistics software (occasional exceptions are described below).

This very much resonates with the way I'm working at [Vebeto](https://www.vebeto.de/).
In fact, this quote puts into words a core principle that we have been following from the start.


### Modelling the extreme using quantile regression

[Massimiliano Ungheretti](https://www.linkedin.com/in/massimilianoungheretti/) gave an excellent presentation on quantile regression.
This method was new to me, but it sounds like it could be very useful.

Massimiliano's motivating example was the following: If I want to know what a really good price for my 
house would be, given its living area,
I would want to know something like the 90th percentile of prices for houses of my size. 
Just knowing the mean is not good enough.
So I need a model linking living area to 90th percentiles of prices.

The "usual" linear regression is an [Ordinary Least Squares](https://en.wikipedia.org/wiki/Ordinary_least_squares)
problem.
It estimates a model for the conditional **mean** of the distribution, using a quadratic penalty.
It does not tell you anything about the distribution of values.

L1 regression ("robust regression", using an L1 penalty) estimates a model for the conditional **median**.
[Quantile regression](https://en.wikipedia.org/wiki/Quantile_regression) is a generalization of this, 
estimating a model for a conditional **quantile** (or percentile).
It uses a "pinball loss function", which looks like a [tilted version](https://de.m.wikipedia.org/wiki/Datei:Pinball_Loss_Function.svg)
of the L1 loss function.
Using quantile regression, you could fit a linear model to your dataset of living area and house prices that
gives you the 90th percentile of the prices for a given area.

Applying quantile regression is a bit more difficult than OLS, both in the model fitting and in the model evaluation.
There is a Python implementation in the [statsmodels](https://www.statsmodels.org/stable/index.html) package.
The statsmodels docs have a [nice example](https://www.statsmodels.org/stable/index.html) on the use of quantile regression.


## Nifty tools

Here are some great tool tips, collected from various presentations:

* [pytest-plugins](https://github.com/man-group/pytest-plugins): A "goody-bag" of useful pytest plugins and fixtures
* [dtale](https://github.com/man-group/dtale): Simple visualization and inspection of Pandas DataFrames/Series.
* [tqdm](https://github.com/tqdm/tqdm): Progress bars for `for`-loops and for `pandas.apply`
* [isort](https://pycqa.github.io/isort/): Sort your imports!
* [loguru](https://github.com/Delgan/loguru): Very simple to use logging package, with colors.


(Disclaimer: I tried my very best to accurately represent the presentations. Let me know in case I got something wrong.)


<<< Go back to the [table of contents](../README.md) || Opinions are mine, not necessarily those of [Vebeto GmbH](https://www.vebeto.de)

--> If you would like to be notified of new posts, delete all the 'z's and drop me a line at til@ehzzzanszzzis.de