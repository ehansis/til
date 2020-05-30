# Tooling for this page

Here is an interesting piece of data (that I just now made up): 
53% of programmers who use Markdown for a blog-like site 
write their own tooling for managing the content.
No wonder then that this repo [includes](../tocgen.py) ``tocgen.py``, 
my small (but sure to be growing) collection of helper functions for this site.

Currently, the script does three things:

* For the table of contents, it pulls the title of each linked page from the 
  respective Markdown file and sets it as link text.
* Appends a link back to the table of contents to each sub-page.
* It searches for all links (internal and external) and checks if they are alive.

Writing this took an hour, maybe, but I project the total time savings over
the lifetime of this site to be orders of magnitude larger (by expert judgement).
More importantly so, it helps me catch and avoid mistakes.

Regarding the last point: I think that improved quality is a generally undervalued benefit
of automation. More on that later.




<<< Go back to the [table of contents](../README.md) || Follow on [twitter](https://twitter.com/EberhardHansis)