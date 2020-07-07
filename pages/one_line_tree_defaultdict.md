# def tree(): return defaultdict(tree)

... one-line tree structure in Python!

Now you can do something like
```python
from collections import defaultdict

def tree(): return defaultdict(tree)

food = tree()
food["healty"]["fruit"]["apple"] = 3
food["nasty"]["burgers"]["cheeseburger"] = 8
```

(This has been written about by many others before, 
see e.g. [here](https://gist.github.com/hrldcpr/2012250) for a longer explanation. 
I like it that there are so many simple things to discover in Python!)