# Favourite VIM features, Episode 1

I have been using [vim](https://www.vim.org/) for many years now.
Still, I continue to find new features or re-discover forgotten ones.
Here are some of my relatively recent (re-)discovered favourites:

* ``zz``: Move current line to the middle of the screen. 
I often use this when stepping through search results (``/`` and ``n``), 
to view the context around the current search result.
Associated are ``zt`` and ``zb``, which move the current line to the 
top or bottom of the screen respectively.

* ``{`` and ``}`` to move one paragraph backwards/forward.
I used to know about and not use these, but I recently started to use
them a lot to jump around source code, when page up/down is too far
and moving by line is too slow.

* ``p`` in visual mode: This replaces the currently selected text with 
the contents of the default register.
A typical use case would be to paste something into a set of parentheses:
I could be tempted to go into the parentheses where I want to paste and
``di(P`` to change their content.
However, the delete replaces the content of the default register! 
So if I already have the text I want to paste in the
default register, it would be overwritten and the same text pasted back.
If, instead, I ``vi(`` to select the inside of the parentheses and then ``p``
in visual mode, I can paste the (previous) contents of the default register.
*After* pasting, I have the replaced text in the default register, so this
is also handy to swap text between to places.

* ``gv`` Repeat last visual selection. Saves quite a few keystrokes sometimes.

(If you have come this far: what about a round of [VimGolf](http://www.vimgolf.com/)?)





<<< Go back to the [table of contents](../README.md) || Opinions are mine, not necessarily those of [Vebeto GmbH](https://www.vebeto.de)

--> If you would like to be notified of new posts, delete all the 'z's and drop me a line at til@ehzzzanszzzis.de