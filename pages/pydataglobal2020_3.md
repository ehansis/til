# PyData Global 2020, Episode 3/3

This is part three of a series of posts on [PyData Global 2020](https://global.pydata.org/).

* [Part one](pydataglobal2020_1.md) is about the conference format, data analysis methods and handy tools.
* [Part two](pydataglobal2020_2.md) is about ML model explainability, and some advanced Pandas stuff.
* The third post (this one here) features data visualization topics.


## Rapidly emulating professional visualizations from New York Times in Python using Altair, by Shantam Raj

[Altair](https://altair-viz.github.io/) is a fantastic Python package that wraps the [Vega-Lite](https://vega.github.io/vega-lite/) grammar of graphics.
This is currently my go-to package for highly customized and complex plots with a 'predictable' API (i.e., not like matplotlib).
Shantam has a nice [gallery](https://armsp.github.io/covidviz/) of Altair plots, in which he re-creates professional data visualizations
from various new outlets in Altair.
The site includes all the plotting code.
For beginners in Altair, these projects might be a bit hard to follow at times, because not every single step is explained in detail.
Yet they are a good resource to study advanced chart composition and styling options in Altair.



## Panel: Dashboards for PyData, Tutorial by James A. Bednar

When I was regularly building 'business intelligence' dashboards (which I don't do anymore, thank goodness), 
I was always searching for good Python libraries to do the job.
R has had [Shiny](https://shiny.rstudio.com/) for a long time, but Python didn't have a real competitor.
(Back then, I settled on building in Python+JavaScript, heavily leaning on [dc.js](https://dc-js.github.io/dc.js/)
and [crossfilter](https://github.com/crossfilter/crossfilter), in case you were interested.)

Now, it seems like [Panel](https://panel.holoviz.org/) is establishing itself as a viable dashboard solution in Python.
Go read about all of its features on the website, and check out the [getting-started guide](https://panel.holoviz.org/getting_started/index.html)
to see how quickly you can get off the ground.
Simply calling `pn.interact` on a plotting function introspects the function signature,
finds variables that it can automatically create interaction widgets for (sliders, ...)
and re-plots on parameter changes.
If you need more control, you can build your dashboard manually from `panel.widgets` and bind them to display functions with `panel.bind`.

Panel also is very flexible in how you use it, being able to work with all the major plotting packages 
(Matplotlib, Bokeh, Plotly, Altair) and either in a Jupyter notebook or served as a standalone app.

If I had a use for this, I'd try out Panel in an instant. Luckily, I don't! ;-)



## Scalable cross-filtering dashboards with Panel, HoloViews and hvPlot, by Philipp Rudiger and James A. Bednar

This talk was about advanced visualization topics for use with Panel (see the previous section).
Crossfiltering is also known as 'linked brushing': you have several charts showing the same data, with the
possibility of highlighting/selecting data (brushing). With linked brushing, a selection in one plot is also
visible in the others, enabling you to discover relationships between datapoints.
Here's a simple [example](https://altair-viz.github.io/gallery/scatter_linked_brush.html) of scatter plots
with linked brushing, built with Altair.

In Panel dashboards, linked brushing can be achieved using [HoloViews](https://holoviews.org/).
The talk also demoed [hvPlot](https://hvplot.holoviz.org/), which provides an alternate plotting interface
for Pandas, Dask, XArray, GeoPandas and a range of other data analytics packages,
for building interactive [Bokeh](https://docs.bokeh.org/en/latest/) plots.

Quite honestly, I'm somewhat confused about how these packages fit together and how they are best used.
It's great to see so much activity in the data visualization space, though.



(Disclaimer: I tried my very best to accurately represent the presentations. Let me know in case I got something wrong.)



<<< Go back to the [table of contents](../README.md) || Opinions are mine, not necessarily those of [Vebeto GmbH](https://www.vebeto.de)

--> If you would like to be notified of new posts, delete all the 'z's and drop me a line at til@ehzzzanszzzis.de