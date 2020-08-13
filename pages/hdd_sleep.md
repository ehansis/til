# REM Sleep and Hammock-Driven Develoment

Lately I read ["Why We Sleep" - The New Science of Sleep and Dreams](https://www.penguin.co.uk/books/295665/why-we-sleep/9780141983769.html) by Matthew Walker. 
This is a fascinating tour through the current state of affairs in sleep research with a few very interesting messages 
(above all: not sleeping enough is a quick and surefire way of wrecking your mental and physical health).
The chapter on sleep and memory reminded me of a Rich Hickey video called [Hammock-driven development](https://www.youtube.com/watch?v=f84n5oFoZBc) 
(transcript [here](https://github.com/matthiasn/talk-transcripts/blob/master/Hickey_Rich/HammockDrivenDev.md)).
This post is about the connection between these two (must-see/read!) pieces of media.


## Nightswimming

Sleep plays a fundamental role in forming and consolidating memory.
What follows is my very brief and simple description.
For a deeper introduction see any of the References listed at the end of this post.

When we sleep, we cycle through various sleep stages.
The main distinction is between REM (Rapid Eye Movement) and NREM (non-REM) sleep.
Commonly a distiction is made between four different NREM stages, labeled 1 through 4, with 1 describing the lightest and 4 the deepest sleep.
We cycle through these stages several times per night, going from REM through NREM 1, 2, 3 and 4, then back up the ladder to REM (or wakefulness).
Then, a new cycle begins, with each cycle taking about 90 minutes.
The proportion of time spent in each stage varies throughout the night, with more time spent in NREM sleep during the first half of the night
and more in REM during the second half.

NREM and REM sleep serve different purposes.
NREM sleep consolidates memories that are held in short-term memory and stores them in long-term memory, while freeing up capacity in short-term
memory for the next day's learning.
(All this has been shown experimentally, see the references below for some fascinating experiments.
For example, subjects fared much worse at learning new facts on the day after a single night of sleep deprivation.
Which tells you that cramming through the night for an exam is just the wrong thing to do.)

REM sleep is more involved in forming abstract knowledge and creating long-range connections between memories.
In sloppy terms, REM sleep lets your brain try out new and unexpected connections between memories, without the inhibition of "reasonable" thought that prevails during waking hours.
(Again there are lots of fascinating experiments on the topic. Also, as REM sleep is more pronounced during the second half of the night,
waking up early each morning hurts creativity and abstract thinking, as you starve your brain on REM sleep.)


## Finest worksong

Now back to Rich and software.
In the video, he talks about programming mainly consisting of problem solving.
Solving hard problems requires long times of uninterrupted thought.
He suggests the following procedure:

* State the problem as precisely as you can. Get the facts clear. Look at solutions to similar problems, figure out why they don't work in your particular case.
* Write all the information down.
* Think hard about all you have found out so far, in your hammock (hence, hammock-driven development), with your eyes closed, but without going to sleep!
  Also try to find holes in your solutions - things that won't work and tradeoffs.
* The brain can only think about 7 +- 2 things at once, your problem has many more variables. In your hammock you can pull all the different parts
  into conciousness again and again, in different combinations, to see the important connections.
* Then stop thinking about the problem and wait for the solution to come to you.


## Man on the moon

So where is the connection? Here is how I see it.

If you apply Rich's methodology, you prime your brain on the problem.
You make the problem's specifics as clear to your brain as you can and, by thinking hard and long in your hammock,
you make it clear to your brain that this is an important problem.

Now, as you go to sleep, REM sleep kindly takes on the task of creating new and (previously) unexpected connections 
between all the relevant knowledge, finding a novel solution that matches all the boundary conditions.
Probably (speculation on my part) the limit of "7 +- 2" doesn't apply like when awake, making it easier to solve
the problem "as a whole".

The [2009 Walker paper](https://walkerlab.berkeley.edu/reprints/Walker_NYAS_2009.pdf) cited below
describes a great experiment on this topic (on p. 184): 
Subjects were given a set of "number reduction tasks".
However, there was a shortcut that, if you found it, allowed you to finish each problem much more quickly.
The study participants did a first round of number crunching, then spent a break of varying duration either awake or asleep, followed by a second round.
A full night's sleep increased the chance of finding the shortcut to 60%, compared to 25% for any of the awake groups.
Interestingly, the insight was not immediate, the subjects didn't wake up with the shortcut present in their minds!
Instead, finding the shortcut took on average another 100 trials the next day.

To summarize: If you have a hard problem to solve, think about it as hard and as long as you can, trying to tease
out all the facts and boundary conditions that matter.
Then, sleep.
Your friend REM will do its thing, and maybe help you find that novel, creative solution.

For many people just taking your mind off a problem and doing something relaxing also seems to help with problem solving.
Having ideas in the shower is almost a cliche.
For me, cycling works very well - some of the hardest problems I have had to tackle solved themselves while cycling home from the office.
Yet, I can't offer you any scientific insights on showers and how they compare to REM sleep in terms of creativity.


## References

* [M. Walker. Why We Sleep - The New Science of Sleep and Dreams. Penguin Books, 2018](https://www.penguin.co.uk/books/295665/why-we-sleep/9780141983769.html)
* [M. Walker. The Role of Sleep in Cognition and Emotion. NYAS, 2009](https://walkerlab.berkeley.edu/reprints/Walker_NYAS_2009.pdf)
* [Diekelmann S, Born J. The memory function of sleep. Nat Rev Neurosci 11:114-126, 2010](https://www.researchgate.net/profile/Susanne_Diekelmann/publication/40834254_Diekelmann_S_Born_J_The_memory_function_of_sleep_Nat_Rev_Neurosci_11_114-126/links/0912f5032417709272000000.pdf)

(If you think this article is inaccurate or vastly simplified, please help me make it better!)
