JavaScript IRC in Instantbird
#############################
:date: 2010-12-04 17:24
:author: Patrick Cloke
:tags: Instantbird, IRC, Mozilla, programming
:slug: javascript-irc-in-instantbird

I've been working on rewriting the IRC plugin for `Instantbird`_ since
the summer (sometime in August, I can't seem to find the exact date --
at least since Sept. 10th though).

Since `libpurple`_ (used in Pidgin, Adium, etc.) provides the IRC
protocol that we currently use, why do this?  One reason is to iron out
(and find) some of the bugs left in implementing protocols in JavaScript
and part of it is so I can learn to code better.  Unfortunately during
this semester I was not able to get as much done as I had hoped and
almost everything that had been done was finished in August/September

Some big milestones I've completed (with dates if I have them):

#. Connected to server via sockets in JavaScript
#. Generate a conversation that works as a raw connection to the server
   (i.e. as if you had opened a telnet connection to the server)
#. Parsing messages and automatic ponging when the server pings
#. Joining a channel (2010/12/04, i.e. today!)

There had been a bunch of small bugs I had been having in getting this
to work: one error, (which I found quickly) one of the other developers
(`Florian`_) was able to help me out with, was that I was not initiating
a **new** object.  And after learning a bit above observers I was able
to get the UI to respond.  I even threw in support for op/half-op/voice 
After today's work I was able to generate the following screenshot:

.. center::

    .. image:: {filename}/images/IRCworking2.png
        :target: {filename}/images/IRCworking2.png
        :alt: Example conversation using JavaScript IRC.
        :height: 297px
        :class: center

    An initial example of Instantbird communicating using JavaScript IRC.

This build would be almost fully usable by those who do very little on
IRC (i.e. if you just want to go and chat, it'd work well), but there's
a lot more work to be done.  The code can be viewed in the `Experiments
repository`_.  (Check it out, there's a 600+ line switch statement.)

.. _Instantbird: http://www.instantbird.com/
.. _libpurple: http://developer.pidgin.im/wiki/WhatIsLibpurple
.. _Florian: http://queze.net/
.. _Experiments repository: https://hg.instantbird.org/experiments/file/IRC-JavaScript/
