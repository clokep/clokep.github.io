The so-called IRC "specifications"
##################################
:date: 2011-03-08 21:20
:author: Patrick Cloke
:tags: Instantbird, IRC, programming, specifications
:slug: so-called-irc-specifications

.. contents::

In a `previous post`_ I had briefly gone over the "history of IRC" as
I know it.  I'm going to expand on this a bit as I've come to understand
it a bit more while reading through documentation.  (Hopefully it won't
sound too much like a rant, as it is all driving me crazy!)

IRC Specifications
==================

So there's the original specification (`RFC 1459`_) in May 1993; this
was expanded and replaced by four different specifications (`RFC 2810`_,
`2811`_, `2812`_, `2813`_) in April 2000.  Seems pretty straightforward,
right?

DCC/CTCP
========

Well, kind of...there's also the DCC/CTCP specifications, which is a
separate protocol embedded/hidden within the IRC protocol (e.g. they're
sent as IRC messages and parsed specially by clients, the server sees
them as normal messages).  DCC/CTCP is used to send files as well as
other particular messages (ACTION commands for roleplaying, SED for
encrypting conversations, VERSION to get client information, etc.). 
Anyway, this get's a bit more complicated -- it starts with the `DCC
specification`_.  This was replaced/updated by the `CTCP specification`_
(which fully includes the DCC specification) in 1994.  An `"updated"
CTCP specification`_ was released in February 1997.  There's also a
`CTCP/2 specification`_ from October 1998, which was meant to
reformulate a lot of the previous three versions.  And *finally*,
there's the DCC2 specification (two parts: `connection negotiation`_ and
`file transfers`_) from April 2004.

But wait!  I lied...that's not really the end of DCC/CTCP, there's
also a bunch of extensions to it: `Turbo DCC`_, `XDCC (eXtended DCC)`_
in 1993, `DCC Whiteboard`_, and a few other variations of this: RDCC
(Reverse DCC), SDD (Secure DCC), DCC Voice, etc.  Wikipedia has a `good
summary`_.

Something else to note about the whole DCC/CTCP mess...parts of it
just *don't* have any documentation.  There's *none*\ at all for SED (at
least that I've found, I'd love to be proved wrong) and very little
(really just a mention) for DCC Voice.

So, we're about halfway through now.  There's a bunch of extensions to
the IRC protocol specifications that add new commands to the actual
protocol.

Authentication
==============

Originally IRC had no authentication ability except the PASS command,
which very few servers seem to use, a variety of mechanisms have
replaced this, including `SASL authentication`_ (both PLAIN and BLOWFISH
methods, although BLOWFISH isn't documented); and SASL itself is covered
by at least `four`_ `RFCs`_ `in this`_ `situation`_.  There also seems
to be a method called "Auth" which I haven't been able to pin down, as
well as Ident (which is a more general protocol authentication method I
haven't looked into yet).

Extension Support
=================

This includes a few that generally add a way by which servers are able
to tell their clients exactly what a server supports.  The first of
these was RPL\_ISUPPORT, which was defined as a `draft specification`_
in January 2004, and `updated`_ in January of 2005.

A similar concept was defined as `IRC Capabilities`_ in March 2005.

Protocol Extensions
===================

IRCX, a Microsoft extension to IRC used (at one point) for some of
it's instant messaging products `exists as a draft`_ from June 1998.

There's also:

-  The `MONITOR`_ command.
-  `User mode +g`_.
-  `Services compatibility modes`_.
-  `Account-notify client capability`_.
-  `Target change for messages`_.

Services
========

To fill in some of the missing features of IRC, services were created
(Wikipedia has a good `summary`_ again).  This commonly includes
ChanServ, NickServ, OperServ, and MemoServ.  Not too hard, but different
server packages include different services (or even the same services
that behave differently), one of more common ones is `Anope`_, however
(plus they have awesome documentation, so they get a link).

There was an attempt to standardize how to interact with services
called IRC+, which included three specifications: `conference control
protocol`_, `identity protocol`_ and `subscriptions protocol`_.  I don't
believe this are supported widely (if at all).

IRC URL Scheme
==============

Finally this brings us to the IRC URL scheme of which there are a few
versions.  A draft from August 1996 defines the original `irc: URL
scheme`_.  This was updated/replaced by `another draft`_ which defines
irc: and ircs: URL schemes.

As of right now that's all that I've found...an awful lot.  Plus it's
not all compatible with each other (and sometimes out right contradicts
each other).  Often newer specifications say not to support older
specifications, but who knows what servers/clients you'll end up talking
to!  It's difficult to know what's used in practice, especially since
there's an awful lot of `IRC servers`_ out there.  Anyway, if someone
does know of another specification, etc. that I missed please let me
know!

.. _previous post: {filename}/why-rewrite-irc-into-javascript-vs-libpurples-vs-chatzillas.rst
.. _RFC 1459: http://tools.ietf.org/html/rfc1459
.. _RFC 2810: http://tools.ietf.org/html/rfc2810
.. _2811: http://tools.ietf.org/html/rfc2811
.. _2812: http://tools.ietf.org/html/rfc2812
.. _2813: http://tools.ietf.org/html/rfc2813
.. _DCC specification: http://www.irchelp.org/irchelp/rfc/dccspec.html
.. _CTCP specification: http://www.irchelp.org/irchelp/rfc/ctcpspec.html
.. _"updated" CTCP specification: http://www.invlogic.com/irc/ctcp.html
.. _CTCP/2 specification: http://www.invlogic.com/irc/ctcp2_intro.html
.. _connection negotiation: http://tools.ietf.org/html/draft-smith-irc-dcc2-negotiation-00
.. _file transfers: http://www.dcc2.org/files/dcc2/draft-smith-irc-dcc2-files-00.txt
.. _Turbo DCC: http://www.visualirc.net/tech-tdcc.php
.. _XDCC (eXtended DCC): http://xa.bi/files/irc/xdcc.3.3.0b.irc
.. _DCC Whiteboard: http://www.visualirc.net/tech-wboard.php
.. _good summary: http://en.wikipedia.org/wiki/Direct_Client-to-Client
.. _SASL authentication: http://hg.atheme.org/atheme/atheme/raw-file/tip/doc/SASL
.. _four: http://tools.ietf.org/html/rfc2222
.. _RFCs: http://tools.ietf.org/html/rfc4422
.. _in this: http://tools.ietf.org/html/rfc2595
.. _situation: http://tools.ietf.org/html/rfc4616
.. _draft specification: http://tools.ietf.org/html/draft-brocklesby-irc-isupport-03
.. _updated: http://tools.ietf.org/html/draft-hardy-irc-isupport-00
.. _IRC Capabilities: http://tools.ietf.org/html/draft-mitchell-irc-capabilities-01
.. _exists as a draft: http://tools.ietf.org/html/draft-pfenning-irc-extensions-04
.. _MONITOR: http://hg.atheme.org/charybdis/charybdis/raw-file/tip/doc/monitor.txt
.. _User mode +g: http://hg.atheme.org/charybdis/charybdis/raw-file/tip/doc/modeg.txt
.. _Services compatibility modes: http://hg.atheme.org/charybdis/charybdis/raw-file/tip/doc/services.txt
.. _Account-notify client capability: http://hg.atheme.org/charybdis/charybdis/raw-file/tip/doc/account-notify.txt
.. _Target change for messages: http://hg.atheme.org/charybdis/charybdis/raw-file/tip/doc/tgchange.txt
.. _summary: http://en.wikipedia.org/wiki/Internet_Relay_Chat_services
.. _Anope: http://www.anope.org/docgen/1.8/en_us/
.. _conference control protocol: http://www.irc-plus.org/specs/confctrl-draft.html
.. _identity protocol: http://www.irc-plus.org/specs/identity-draft.html
.. _subscriptions protocol: http://www.irc-plus.org/specs/subscriptions-draft.html
.. _`irc: URL scheme`: http://tools.ietf.org/html/draft-mirashi-url-irc-01
.. _another draft: http://tools.ietf.org/html/draft-butcher-irc-url-04
.. _IRC servers: http://en.wikipedia.org/wiki/Comparison_of_IRC_daemons
