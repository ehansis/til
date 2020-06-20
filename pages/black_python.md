# Just make it black: stop worrying about Python code formatting

[Black](https://github.com/psf/black) is a tool that calls itself 'the uncompromising Python code formatter',
and it really lives up to this promise.

Black formats your code according to strict rules, while making sure that the code's behaviour doesn't change.
Since I discovered it, I have hardly spent any time manually formatting my code.
Black saves you a lot of time, makes your code more readable and enforces a consistent syle within your development team.

Here is some random example code (from a [Code Kata](http://codekata.com/) exercise) before Black:
```python
import re

def get_cols():
    with open("weather.dat") as f:
            first_line = f.readline()

    matches=re.finditer(r' +\S+', first_line)

    return {m.group().strip(): {'start': m.start(), 'num': m.end() - m.start()} for m in matches}
```

Here it is after:
```python
import re


def get_cols():
    with open("weather.dat") as f:
        first_line = f.readline()

    matches = re.finditer(r" +\S+", first_line)

    return {
        m.group().strip(): {"start": m.start(), "num": m.end() - m.start()}
        for m in matches
    }
```

Some things that happened are:
* Quotes normalized to all double quotes
* Long lines broken up
* Correct spaces around operators
* Normalized number of empty lines before functions
* Normalized indentation

I added a keyboard shortcut in my IDE (``Cmd+Ctrl+B``, if you wanted to know) for
running Black on the current source file.
I run it every time I have finished a block of code or a specific change. 
Running it has become so much of a habit that I often catch myself hitting ``Cmd+Ctrl+B`` in TeX, Markdown or JavaScript.
Still, I opt for running it manually instead of automatically on saving, because automatic reformatting of code might, 
for example, interfere with debugging sessions.

I find it tremendously liberating that I am practically unable to format the code manually.
This way, I can completely focus on the content.
This might sound trivial, but try it for a while and I hope that you become as attached (addicted?) to it as I am.




<<< Go back to the [table of contents](../README.md) || Follow on [twitter](https://twitter.com/EberhardHansis) || Opinions are mine, not necessarily those of [Vebeto GmbH](https://www.vebeto.de)