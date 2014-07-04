Yahoo Protocol Google Summer of Code Round-up
#############################################
:date: 2013-10-06 09:18
:author: Patrick Cloke
:tags: chat, GSoC, IM, instant messaging, Instantbird, Yahoo
:slug: yahoo-protocol-google-summer-of-code

I have to apologize to my student, `Quentin`_ (aka qheaden on IRC),
for taking so long to write this...but anyway: Google Summer of Code
2013 is over!  Quentin has done a great job working at implementing the
Yahoo Protocol for Instantbird (and Thunderbird) in JavaScript
(henceforth called "JS-Yahoo").  It's at the point where it has mostly
reached feature-parity with the libpurple plug-in.  Before `turning this
on as default`_ there are a few minor bugs that still need to be fixed,
but most of them have patches that just need another couple iterations.

Where do we go from here?
=========================

Once the last few bugs are fixed we'll enable Yahoo by default in the nightly
builds and, assuming we have no issues, it will be enabled by default in the
upcoming Instantbird 1.5. If there are no major issues in 1.5, we'll remove the
libpurple Yahoo implementation for Instantbird 1.next.

How do I try this now?!
=======================

You can already easily enable JS-Yahoo in `Instantbird nightly builds`_:

#. Type /about config in a conversation tab's textbox
#. Type "forcePurple" in the search box
#. Remove "prpl-yahoo" and "prpl-yahoojp" from this comma separated list
   of values (you can also remove prpl-jabber if you want to always use
   the JS-XMPP implementation from GSoC 2011! Note that this doesn't
   support `DNS SRV`_, however.)
#. Restart Instantbird!

You should now be using the JS-Yahoo protocol.  Hopefully you don't
notice anything different, but `PLEASE file bugs`_ if you see any
issues.

How come I can't use this in Thunderbird?!
==========================================

Because Instantbird and comm-central development don't happen in the same
Mercurial repository.  I'm working on `syncing the chat/ folder of these
repositories`_ currently and JS-Yahoo should be in Daily soon to be
included in the next Thunderbird release (i.e. Thunderbird 31).

The whole Instantbird community has been super happy with the progress
Quentin made and we hope that Quentin has learned a lot! Thanks for a
great summer qheaden and hopefully we'll see you around still!

.. _Quentin: http://phaseshiftsoftware.com/blog/
.. _turning this on as default: https://bugzilla.instantbird.org/show_bug.cgi?id=2135
.. _Instantbird nightly builds: http://nightly.instantbird.im/
.. _DNS SRV: https://bugzilla.mozilla.org/show_bug.cgi?id=14328
.. _PLEASE file bugs: https://bugzilla.instantbird.org/
.. _syncing the chat/ folder of these repositories: https://bugzilla.mozilla.org/show_bug.cgi?id=920801
