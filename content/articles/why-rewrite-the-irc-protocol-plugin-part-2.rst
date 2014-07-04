Why rewrite the IRC protocol plugin? (Part 2)
#############################################
:date: 2011-04-30 13:01
:author: Patrick Cloke
:tags: Instantbird, IRC
:slug: why-rewrite-irc-protocol-plugin-part-2

I `previously wrote about`_ why I'm rewriting the libpurple IRC
implementation into a JavaScript implementation for Instantbird.  This
is kind of a follow up, but more focused on what I hope to accomplish
feature wise for IRC in Instantbird.  A good overview to look at is the
`dependencies of bug 507`_ (implement IRC in JavaScript) -- you'll want
to look to the left of bug 507, these are the bugs that depend on 507
(as opposed to blocking 507).

My overall hope is to make Instantbird the easiest and simplest IRC
client to use.  I've found that most IRC clients tend to depend a great
deal on commands and essentially being a very thin GUI layer on top of
the protocol.  I don't really see the reason for this, we should attempt
to hide the protocol as much as possible from the users.  This means
fitting the IRC command responses into the GUI wherever possible and
possibly "losing" some features compared to other IRC clients, although
I think that's a matter of perspective.  (For example, there's often an
IRC command to list all the channels available, I *do not* think this
should be implemented as a text command, but it should be available via
the join chat GUI).

Now some more specific plans:

-  Support for IRC services would be pretty awesome, I'm not sure
   whether this would be part of the main protocol or as an extension,
   but it should be able to handle NickServ mostly autonomously
   (possibly even automatically registering the nick, etc.).  MemoServ
   could be implemented as a message service once there is UI for that
   in Instantbird.  I'm not sure how ChanServ could be handled in the
   UI, but I'll think more about this.  See `bug 720`_ for more info. 
   (And yes, there are multiple versions of IRC services, but we can
   attempt to support a subset and otherwise just leave it up to the
   user.  Ideally servers would have supported this stuff...but that's
   not how IRC works.)
-  The UI should be more responsive to the modes of the user and to the
   channel.  For example, if the user does not have permission to edit
   the topic, it should not be editable in the UI (`bug 318`_).  Also,
   if a user is a (half-)operator, there should be UI to have cause
   other users to be given (h)op (`bug 597`_).  In terms of channel
   modes, there could be UI to show the channel is invite only or that
   it's a hidden channel.

There's some not as user visible improvements I'd like to make:

-  Supporting more authentication methods in IRC (`bug 719`_).

There's also a few "bugs" in the libpurple implementation that this
will fix:

-  The /msg command doesn't show outgoing messages (`bug 188`_).  I
   believe this is actually already fixed.
-  IRC channels should automatically rejoin on reconnect (`bug 385`_).
-  Chats with other users should show whether they are available or not
   (`bug 613`_).

These are just some ideas and it's a long ways off for feature parity
with libpurple even.  (Although since Instantbird doesn't support all
the features of Pidgin, feature-parity in this case doesn't include
things like DCC transfer, etc. until Instantbird itself supports those.)

Right now, the code is mostly usable (and I'm finally catching any
exceptions that are thrown so the code shouldn't crash anymore), and
works fine.  The one issue I'm having is sometimes I'm unable to
reconnect when the connection is lost, but I think I've finally fixed
that issue and reconnection should happen automatically!

One last quick note, if you happen to have the `repository`_ checked
out, you'll want to update on the default branch from now on as I've
merged the separate branches together under subfolders.

.. _previously wrote about: {filename}/articles/why-rewrite-irc-into-javascript-vs-libpurples-vs-chatzillas.rst
.. _dependencies of bug 507: https://bugzilla.instantbird.org/showdependencygraph.cgi?id=507&display=web&rankdir=LR
.. _bug 720: https://bugzilla.instantbird.org/show_bug.cgi?id=720
.. _bug 318: https://bugzilla.instantbird.org/show_bug.cgi?id=318
.. _bug 597: https://bugzilla.instantbird.org/show_bug.cgi?id=597
.. _bug 719: https://bugzilla.instantbird.org/show_bug.cgi?id=719
.. _bug 188: https://bugzilla.instantbird.org/show_bug.cgi?id=188
.. _bug 385: https://bugzilla.instantbird.org/show_bug.cgi?id=385
.. _bug 613: https://bugzilla.instantbird.org/show_bug.cgi?id=613
.. _repository: https://hg.instantbird.org/experiments
