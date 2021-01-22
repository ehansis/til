# CORS, Tainted Canvases and getDataURL

A while ago I implemented a data animation on top of a map background.
The map was drawn with [Leaflet.js](https://leafletjs.com/) using tiles from [Maptiler](https://www.maptiler.com/),
the data with [d3.js](https://d3js.org/) (this is irrelevant for the following discussion, just for completeness).

I wanted to store the animation as a video, so I tried two different approaches:
1. rendering the animation in the browser and recording it with a `MediaRecorder`, following [this example](https://bl.ocks.org/veltman/ff864215009174bc5d164ec3533125c2), or
2. drawing the animation frame-by-frame into a `canvas`, retrieving the frames via `canvas.toDataURL('image/png')` and sending
them to my server for movie encoding with [ffmpeg](https://ffmpeg.org/).

Both approaches work (and have their own advantages and disadvantages), but for both there was the same
initial obstacle:


## Tiles tainted my canvas

When I drew only the data to the canvas, I could get the image content or video fine.
However, once I added the map, I got either blank output with no error message (from the `MediaRecorder`)
or a `canvas.toDataURL() Security Error` when retrieving the canvas content with `canvas.toDataURL`.

As it turns out, this issue arises from [CORS](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS) security policies.
Quoting from the [MDN web docs](https://developer.mozilla.org/en-US/docs/Web/HTML/CORS_enabled_image):

> Because the pixels in a canvas's bitmap can come from a variety of sources, including images or videos retrieved from other hosts, it's inevitable that security problems may arise.
>
> As soon as you draw into a canvas any data that was loaded from another origin without CORS approval, the canvas becomes tainted. A tainted canvas is one which is no longer considered secure, and any attempts to retrieve image data back from the canvas will cause an exception to be thrown.
     
So once I added the map tiles from the tile provider, the canvas became 'tainted' and I was no longer allowed to record
it or retrieve its content as an image.

The rationale behind this policy, as I understand it, is the following:
I could write JavaScript code that loads images from locally accessible sources of images and videos.
Without the security policy, I could record or retrieve the image data from the browser and send it someplace else.
However, drawing that content, which is from a different origin than my web application, marks the canvas as tainted and forbids
recording or image data retrieval.


## What to do?

The source of the image or video data can allow Cross-Origin access, as described [here](https://developer.mozilla.org/en-US/docs/Web/HTML/CORS_enabled_image).
There is also a [question on StackOverflow](https://stackoverflow.com/questions/25753754) with some more 
information and suggestions for solutions.

In my case, the easiest solution was to proxy the map tile requests through my own webserver.
This way the page containing the JavaScript code and the tile URL had the same origin and canvas recording/retrieval was allowed.




<<< Go back to the [table of contents](../README.md) || Opinions are mine, not necessarily those of [Vebeto GmbH](https://www.vebeto.de)

--> If you would like to be notified of new posts, delete all the 'z's and drop me a line at til@ehzzzanszzzis.de