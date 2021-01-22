# Fiddly Fonts and Ubiquitous Browsers

(The first half of this post is somewhat technical. You can safely skip ahead to "Know your Browser", if you wish.)


## Dude, where's my font?

When rendering a web page, a web browser tries to throw something onto the screen as quickly as possible.
This means that it will start rendering before all assets like images, style sheets or font files have been downloaded.
Depending on your browser, you might see an "unfinished" version of the page first that changes into the final, fully formatted version sometime later.
This effect has sometimes been dubbed [FOUT - Flash of Unstyled Text](https://www.paulirish.com/2009/fighting-the-font-face-fout/).

When visiting a webpage, it might be considered an insignificant annoyance if the correct fonts appear belatedly.
The annoyance becomes major, though, when you (ab)use the browser to generate data visualizations, as I like to do:
I like to code my graphs to be viewed in the browser and, if I need a standalone file like a PDF or PNG,
to render them with [Selenium](https://www.selenium.dev/) or some other headless automated browser.

My favourite graphing solution, [Altair](https://altair-viz.github.io/) in conjunction with 
[Vega-Embed](https://github.com/vega/vega-embed), draws charts in a [HTML Canvas](https://www.w3schools.com/html/html5_canvas.asp).
If these graphs are drawn before the fonts for the chart are available to the browser,
I either get default fonts (tends to happen in Firefox) or no fonts at all (tends to happen in Chrome).
Contrary to a regular web page, the charts are **not** being redrawn once the fonts are available!
In an interactive browser session I can hit Reload to get the charts right.
When building "hardcopies" of charts in a headless browser, I cannot, so I randomly end up with broken, unlabeled charts 
once in a while.


## Fix FOUT

That's not acceptable, obviously. Searching the web, you can find numerous suggestions on how to alleviate the issue.
If you really want to dig into the issue, I recommend the [comprehensive font loading guide](https://www.zachleat.com/web/comprehensive-webfonts/)
by Zach Leatherman. What follows is from my own experiments:


### Use a `preload` tag

You could add something like the following to your `<head>` section:
```
<link rel="preload" href="fonts/myfont.otf" as="font" type="font/opentype" crossorigin>
```
To cite from the [MDN Web Docs](https://developer.mozilla.org/en-US/docs/Web/HTML/Preloading_content):
> The preload value of the `<link>` element's `rel` attribute lets you declare fetch requests in the HTML's `<head>`, specifying resources that your page will need very soon, which you want to start loading early in the page lifecycle, before browsers' main rendering machinery kicks in. This ensures they are available earlier and are less likely to block the page's render, improving performance.
 
In theory, telling the browser to load font files early might make them available in time for the chart rendering.
In practice... it didn't reliably help with my chart rendering issues.


### Use the font at the start of the body

Several people recommended adding an html tag that explicitly uses the font, at the very start of the `<body>`
(e.g. in a `<div>` with size zero or an otherwise invisible `<span>`).
The idea is that this causes the browser to load and apply the font.
This didn't seem to work at all for me.


### Base64-encode your fonts 

Instead of loading font files in CSS from a URL like this
```css 
@font-face {
    font-family: "MyFancyFont";
    font-style: normal;
    font-weight: bold;
    src: url("/assets/fancybold.otf") format("opentype");
}
```
you can embed the font data right into the `@font-face` by using a base64-encoded [data URI](https://en.wikipedia.org/wiki/Data_URI_scheme).
So your `@font-face` might look like this:
```css
@font-face {
  font-family: "MyFancyFont";
  font-style: normal;
  font-weight: bold;
  src: url(data:font/opentype;base64,T1RUTwA...);
}
```
The part starting with `T1RUTwA...` is a very long string (shown truncated here) that contains the font file's data in base64 encoding.

If you have Python at hand, the following snippet loads and base64-encodes a file, and copies the resulting string to your clipboard
(if you have `pyperclip`) installed:
```python
import base64
import pyperclip
s = base64.b64encode(open("<file name>", "rb").read())
pyperclip.copy(str(s))
```

This actually helped me get fonts right in desktop browsers (Firefox, Safari and Chrome), and in Selenium/Chromium-based headless rendering.
But Firefox on iOS refused to show the font in the charts, and Safari on iOS only showed it on reload ... a partial success.

**Note:** This will reduce rendering performance, so this is probably not a good choice for your average high-traffic website.
See also [Zach's thoughts](https://www.zachleat.com/web/web-font-data-uris/) on the topic.


### Check if fonts are ready

There is a `document.fonts` property that can, according to [the docs](https://developer.mozilla.org/en-US/docs/Web/API/Document/fonts),
be used to defer javascript commands until fonts are loaded:
```javascript
document.fonts.ready.then(function() {
  // Any operation that needs to be done only after all the fonts
  // have finished loading can go here.
});
```

I stick the `vega-embed` code, that renders the Altair charts, into the callback.
This, in conjunction with base64-encoding of the fonts, seems to work most of the time.
Yet, since this error occurs only randomly, I'm not 100% sure yet, and Firefox on iOS still refuses to show my fonts.
The search continues...


## Know your Browser

If you have skipped the technical stuff, you can safely _stop skipping now_.

### Browsers are taking over the world!

What's the bigger point here?
Your web browser is the portal through which you satisfy a large part of your digital information needs.
Even if you think that you are using a native desktop app, you may actually be looking at
a web page displayed with the [Chromium](https://www.chromium.org/Home) rendering engine, disguised
as a desktop app by virtue of the [Electron](https://www.electronjs.org/) framework.
Here are a few examples of Electron "desktop" apps, i.e. special websites shown in a special browser window posing as native apps:

* Slack
* Skype
* WhatsApp Desktop
* Visual Studio Code
* Evernote
* Microsoft Teams
* Todoist
* Twist
* ... and the list goes on and on.

So even if you are not working in your browser, you may actually still be working in a browser.


### Browsers are very complicated!

While becoming ubiquitous, browsers also have become very complicated.
The foray into font rendering above is just a tiny hint at all the complications that can befall a modern web developer.
CSS can also be very complicated, as can be JavaScript and any of the other web technologies.

That's from the web developer perspective.
Under the hood, browsers are astonishingly complicated, too!
There is the very nice [Life of a Pixel](https://www.youtube.com/watch?v=PwYxv-43iM4) video that romps through the
Chrome rendering architecture in 25 minutes and shows all the things that have to happen for you to actually
see the cat video.

So why am I writing this? With browsers being such an important piece of software, and web technologies becoming
so wide-spread, it's not a bad idea, as a technically minded person, to have a basic understanding of the fundamental building blocks.
Even if you are not building software or websites yourself, you may be running projects with people who do.
And you are certainly using web technologies all the time.
The [Life of a Pixel](https://www.youtube.com/watch?v=PwYxv-43iM4) video is a good starting point, as it touches on
all the major building blocks.
From there you can branch out into the topics you find most interesting, and pick the rabbit hole of your choice.

Happy browsing everyone!


<<< Go back to the [table of contents](../README.md) || Opinions are mine, not necessarily those of [Vebeto GmbH](https://www.vebeto.de)

--> If you would like to be notified of new posts, delete all the **z**s and drop me a line at **til@ehzzzanszzzis.de**