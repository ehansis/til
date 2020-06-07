# Getting Complex
... and understanding Simple along the way.

## Go watch this talk

This post is based on an, in internet-terms ancient, talk by Rich Hickey, 
entitled ["Simple Made Easy"](https://www.infoq.com/presentations/Simple-Made-Easy/).
If you deal in any way with software or other complex systems and haven't seen the talk yet, I recommend
that you do so (right after you finished reading this post).


## What Complex means

I'm not going to try and summarize the talk.
Instead, I want to focus on my main take-away: the meaning of the word "complex".

Complex means entangled, braided, intertwined. 
You take several strands of thought and "complect" them with each other.
Understanding the whole construct becomes challenging, because you have to keep multiple things in your head
at the same time and evaluate their interactions.
Since our brain can only think about a limited number of facts at the same time (7?), understanding
complex systems is very difficult and you are bound to make mistakes.

"Simple", on the other hand, derives from "simplex", a single strand.
If things are simple, they are not entangled or intertwined with something else.


## Complexity in software

Simplicity (i.e. the absence of complexity) is probably the most important factor in designing robust systems.
Here are a few examples where complexity may arise:


### Not so DRY

(I heard this example elsewhere but don't remember the source, sorry.) Imagine you are refactoring
a big code base. You discover a bit of functionality, applying colors for formatting error messages,
that has been re-implemented several times in different parts of the system, e.g. in the database backend,
in the user interface and in administrative tools.
You might be tempted to unify that in one spot, in a library of utility functions, and replace the respective code
in the whole code base by calls to your new function.
That's great, right? It follows the [DRY principle](https://de.wikipedia.org/wiki/Don%E2%80%99t_repeat_yourself) (don't repeat yourself)!

However, now you have complected parts of the system - database backend, user interface and admin tools - that
maybe were not complected before and never should have been!
This can cause all kinds of headaches in the long run, like the inability to split apart the code of these
three constituents, added complexity when wanting to change the functionality for just one part of the system or
simply making the code harder to understand.

Of course, often times it is very valuable to stay DRY.
But it is precisely this notion of complexity - tying things together that should be separate - that has to 
be considered carefully.


### State

As a second example, pointed out in Rich's talk, consider [state](https://en.wikipedia.org/wiki/State_(computer_science)).
Loosely defined, a program's state remembers past events or user interactions.
For example, if you click the ``B`` button in the toolbar of your document editor, you put it into a state where all text is set in bold face.

State is inherently complex.
If the behavior of your code depends on its internal state, you complect all past interactions with what is happening right now.
Debugging becomes infinitely harder in stateful systems, because in order to find an issue, you have to precisely
regenerate the state it was in when the problem occurred.
Avoiding state wherever possible promotes simplicity.


### Shiny new toys

A third example for inadvertent complexity comes from external dependencies and tools.
The larger the toolset that you use in your system, the more complex it becomes.

Yes, I can very quickly build a website in [Wordpress](https://wordpress.com/), and I can even host it myself if I want to.
But I have now complected the task of putting some text in front of you with a giant hairball of PHP and configuration
that I don't really care to understand.

Or, consider the Python plotting package [Altair](https://altair-viz.github.io/).
I love its syntax, it let's me create beautiful, highly customized graphs.
But for exporting them to SVG or PDF, I need to run the visualization, which ends up being rendered with JavaScript,
through a headless browser.
I understand that this is inherent to the design of Altair, being a wrapper around [Vega-Lite](https://vega.github.io/vega-lite/docs/).
And usually it works beautifully.
But I just hate the thought that I am dependent on [Selenium](https://www.selenium.dev/selenium/docs/api/py/)
and [ChromeDriver](https://chromedriver.chromium.org/) or [GeckoDriver](https://firefox-source-docs.mozilla.org/testing/geckodriver/)
just to save my charts.
(Don't get me wrong here: Altair is great and I very much recommend it. It's just the feeling of complexity that annoys me.)


## KISS (Keep it simple, stupid!)

I find this notion of complexity very helpful when considering design choices.
The problems you work on are complex enough in and of themselves.
Avoid inadvertent complexity from design and technology choices, spend your effort on problem complexity instead.

What I have left out here is the difference between 'easy' and 'simple', which I leave to Rich to discuss.
Now it's time to go watch [the talk](https://www.infoq.com/presentations/Simple-Made-Easy/)!


