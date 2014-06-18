Why Rewrite IRC into JavaScript? (vs. libpurple's vs. ChatZilla's)
##################################################################
:date: 2010-12-08 18:29
:author: Patrick Cloke
:tags: Instantbird, IRC, Mozilla, programming
:slug: why-rewrite-irc-into-javascript-vs-libpurples-vs-chatzillas

I had a request on IRC (from Mic) to write an in-depth blog post
about `IRC in JavaScript`_:

    "Maybe we could ask clokep if he'd like to write something about
    js-irc? Why it is done, what the advantages are once it's done, how
    he is working on it (going through the specs), putting the
    jsProtocol code to test and adding missing pieces?" -- `Mic`_

Wait a second, what is IRC?
===========================

I guess this is a good first question, I'll steal from `Wikipedia`_:

    Internet Relay Chat (IRC) is a form of real-time [...] chat [...] It
    is mainly designed for group communication [...] but also allows
    [...for...] private message as well as chat and data transfers.

Awesome, what's that really mean?  It's an instant messaging protocol
with an actual specification (i.e. it's not owned by some large, unnamed
company), with open-source libraries for clients and servers.  It's
usually used by more computer-oriented types of people and centers
around group conversation.  Personally most of what I use it for is
open-source software I use (I'm almost always in `#instantbird`_,
`#maildev`_, and `#songbird`_ on `Mozilla's IRC servers`_.)

Why it is done?  What advantages are there once this is done?
=============================================================

I touched upon this a little in my `last post`_.  In terms of
Instantbird: there's an idea of switching some / all of the protocols
(eventually) to be JavaScript protocols instead of the libpurple
versions (libpurple is written mostly in C and is cross-platform, but
recent gains in speed in JavaScript allow this advantage of libpurple to
not matter as much).  This would unfortunately mean we need to maintain
a lot more code, but it would allow us to integrate protocols in any way
that we see fit, instead of only using APIs / methods provided by
libpurple.  Hopefully this would allow us to `enhance our IRC
implementation`_ a bit.

Also, Instantbird (nightlies) currently have limited support for
generating a protocol plug-in in JavaScript.  A couple of "test"
protocols have be done, but nothing in "real" (in particular, none that
used a multi-user chat).  This would allow us to iron out `some`_
`bugs`_ in the implementation of JavaScript protocols.

*[Edit: Florian suggested another question that wasn't originally
covered, which some people more familiar with Mozilla code might be
wondering.]*

Why aren't you using the code from ChatZilla?
=============================================

This was a tough one.  Honestly when I first wanted a parsing
algorithm, I looked at the ChatZilla code, I used it.  Then rewrote it
in a fourth as many lines (`93`_ vs. `20`_).  Simply said, the code in
ChatZilla is *old*, it doesn't use many of the features available only
in newer versions of JavaScript.  To that point, the ChatZilla code
hasn't been updated in over a year!  The last check-in was: 2009-10-03,
below is a `quick summary`_ of the number of check-ins per year:

- 2010: 0
- 2009: 5
- 2008: 15
- 2007: 11
- 2006: 18

There's been a pretty steady decline in check-ins.  I could take this
code and attempt to whip it into shape and make huge sweeping changes
and commit them back to ChatZilla, but honestly it was easier to start
over for me.  Regardless of ease, I'm not sure it would work any:
especially since the ChatZilla code seems overly complicated and overly
specific (since it wasn't really built as a library as far as I can
see), especially since all the code is meant to deal only with IRC.  The
Instantbird code needs to be protocol agnostic to a degree, while is why
it interfaces to purplexpcom.

A quick example of this is: ChatZilla uses a CIRCUser object, but for
Instantbird I need to create either an imIContact or a
purpleIAccountBuddy (depending on the situation).  It's possible that's
can be abstracted and code shared -- but I'm not sure it would be worth
the effort.  After all this, I should probably look more into the
ChatZilla code, perhaps more of it could be used.

(If someone familiar with the ChatZilla code base -- I don't know
who/if there's a maintainer -- is interested in talking with me, please
get in contact here or on #instantbird.  It's possible we could align
some of what I've been working on, but I'm not sure how much could be
shared besides the parsing algorithm).

*[End edit]*

What are the specific advantages for an end-user?
=================================================

In terms of the IRC protocol itself, there shouldn't be any, my goal
is for it to be a drop in replacement for the libpurple implementation
with automatic account migration, etc. For end-users we can hopefully
solve `a few annoying IRC UI issues`_.

What about for developers?  Anything cool there?
================================================

Well, I'm hoping to be able to test this replacement via an extension
that replaces the libpurple IRC to dogfood it before eventual inclusion
in Instantbird.  I'm not sure if that counts as "cool." though.  If
nothing else there will be an example of how to write a protocol in
JavaScript (using sockets).  So hopefully other people can make some
other cool protocols off of that example.  You might wonder what else we
have planned for JavaScript protocols; there are plans to make at least
a Twitter protocol.

How is this being done?
=======================

Well I said up above IRC has a specification, right?  Well, yes. 
There's the `original specification`_, this was superseded by `four`_
`different`_ `specification`_ `documents`_.  Of which we only really
care about one: `the client protocol`_.  So we have this updated
specification (try reading it, it's rather painful), which is good. 
It's relatively straightforward set of commands and responses/errors. 
It's a bit more confusing than that though since there are a couple of
extensions, etc.  This is summarized below:

* [STRIKEOUT:RFC 1459]

    * Extended with `[STRIKEOUT:DCC specification ("direct client-to-client")]`_

        * Replaced with [STRIKEOUT:`CTCP ("client-to-client protocol")`_]

            * `Draft for a formalized CTCP`_

        * (Apparently some people are working on a `DCC2`_)

    * Officially replaced with RFCs 2810, 2811, 2812, 2813

A lot of this is being done by reading the specifications and finding
the proper responses, etc.  I've also used `Wireshark`_ a bit to see how
libpurple sends IRC commands (in particular, in what order it sends them
in).  A lot of my development is happening on live IRC servers, which
isn't really best practice, but I'm mostly sending commands by hand to
see the responses since a bunch of non-standard responses and extensions
have developed beyond the above.  I have been using `beware irc`_ to run
a daemon on my own machine, however.

So how far along are you?
=========================

I've started implementing RFC 2812 and have a variety of commands done
(the login sequence occurs automatically, the server connection is kept
alive, messages can be sent to a channel and are parsed when received, a
lot of the initial server information is displayed but unparsed).  But
there's a lot more to do!  As my last post outlined, I recently was able
to successfully get a chat to work in Instantbird from a silly bug I had
been having.

It's rather slow going since I'll start to implement something from
the IRC side, and then realize the `Instantbird layer`_ (the jsProtocol
module) is missing a component I need.  One of the major parts of
working on this is extending the Instantbird layer to contain the proper
functions and objects needed to implement chats via JavaScript.  This is
usually the slowest going part of my code, since it involves interfacing
with Instantbird / `purplexpcom`_.  Luckily Florian, the main developer
of Instantbird, has been a big help with this (as have other
participants of #instantbird -- in particular I know Mic helped track
down a few syntax type bugs).

What's next?
============

Now that have the basics of chat working, I need to start handling the
QUIT, PART and JOIN commands for when other users enter & leave chat
rooms.  Once these are complete it should be quite usable, although the
entire preference system still doesn't exist, including notifying the UI
of what options are available.  In addition, I need to look into doing
SSL sockets.

Once the protocol plug-in is done, we plan to abstract sections of it
that will be useful for other protocols (in particular the socket
connection aspects).

Where can I see this stuff...?
==============================

My work is kept in the "`experiments`_\ " repository on Instantbird's
`Mercurial`_ repository.  There's also a variety of bugs open (they're
listed above, I'm not going to re-list them), although not a ton is
happening in them.

How can I help?!
================

Well you can of course feel free to download the code and hack on it,
let me know (via IRC or any of the bugs most likely) if you have a patch
you'd like me to apply.  Or if you just found something that doesn't
work you can feel free to let me know, although I probably just haven't
gotten around to fixing it yet.

Also, if you've ever found something annoying / broken in the IRC
implementation in Instantbird / libpurple please let us know (through
any of the above contact sources).

Hopefully that's a bit of a better explanation of why we're spending
time to rewrite the IRC protocol implementation into JavaScript -- we
definitely think it's worth it and can lead to a bunch of new unique
protocol plug-ins for Instantbird.

.. _IRC in JavaScript: https://bugzilla.instantbird.org/show_bug.cgi?id=507
.. _Mic: http://log.bezut.info/instantbird/101208/#m54
.. _Wikipedia: http://en.wikipedia.org/wiki/IRC
.. _#instantbird: irc://irc.mozilla.org/#instantbird
.. _#maildev: irc://irc.mozilla.org/#maildev
.. _#songbird: irc://irc.mozilla.org/#songbird
.. _Mozilla's IRC servers: http://irc.mozilla.org/
.. _last post: {filename}/content/javascript-irc-in-instantbird.rst
.. _enhance our IRC implementation: https://bugzilla.instantbird.org/showdependencytree.cgi?id=507&maxdepth=2&hide_resolved=1
.. _some: https://bugzilla.instantbird.org/show_bug.cgi?id=519
.. _bugs: https://bugzilla.instantbird.org/show_bug.cgi?id=118
.. _93: http://hg.mozilla.org/chatzilla/file/tip/js/lib/irc.js#l1250
.. _20: https://hg.instantbird.org/experiments/file/IRC-JavaScript/components/ircProtocol.js#l208
.. _quick summary: http://hg.mozilla.org/chatzilla/log/tip/js/lib/irc.js
.. _a few annoying IRC UI issues: https://bugzilla.instantbird.org/showdependencytree.cgi?id=574&maxdepth=1&hide_resolved=1
.. _original specification: http://tools.ietf.org/html/rfc1459
.. _four: http://tools.ietf.org/html/rfc2810
.. _different: http://tools.ietf.org/html/rfc2811
.. _specification: http://tools.ietf.org/html/rfc2812
.. _documents: http://tools.ietf.org/html/rfc2813
.. _the client protocol: http://tools.ietf.org/html/rfc2812
.. _`[STRIKEOUT:DCC specification ("direct client-to-client")]`: http://www.irchelp.org/irchelp/rfc/dccspec.html
.. _CTCP ("client-to-client protocol"): http://www.irchelp.org/irchelp/rfc/dccspec.html
.. _Draft for a formalized CTCP: http://www.invlogic.com/irc/ctcp.html
.. _DCC2: http://www.dcc2.org/
.. _Wireshark: http://www.wireshark.org/download.html
.. _beware irc: http://ircd.bircd.org/
.. _Instantbird layer: http://hg.instantbird.org/instantbird/file/tip/purple/purplexpcom/src/jsProtoHelper.jsm
.. _purplexpcom: http://hg.instantbird.org/instantbird/file/tip/purple/purplexpcom/public/
.. _experiments: https://hg.instantbird.org/experiments/file/IRC-JavaScript/
.. _Mercurial: http://mercurial.selenic.com/
