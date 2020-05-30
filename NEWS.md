1.0.1 2020-05-30 Lady Elaine
============================

There have been a few usuablity improvements here, with the help of updated `trepan3k` and `x-python` and `xdis` releases.

Stack operands are now shown for instruciton and we colorize trace output.

New commands:

* `set logtrace` sets logger level on vm tracing
* `next` (step over)
* `finish` (step out)

There are some bugs in `set logtrace`, and `finish`. However, as in the last release, these are minor compared to the improvements. So release again rather than wait.


1.0.0 2020-04-20 One-oh!
========================

I gotta say it that the interaction between this and x-python is pretty cool, and the possibiilities for which direction to go in on both projects are numerous and vast.

How did I get here? Well, I was pouring over trace logs to find bugs in x-python, and then realized, hey, I've written a debugger already for Python that could help here.

So here it is.  I can die now and my life is complete.

Although commands like `next`, `finish` and breakpoints, aren't there yet, rather than sit on it this, I thought I'd release. This is very usuable as is - release early and often!
