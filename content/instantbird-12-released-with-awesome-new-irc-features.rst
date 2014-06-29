Instantbird 1.2 Released (with awesome new IRC features)!
#########################################################
:date: 2012-08-08 17:08
:author: Patrick Cloke
:tags: Instantbird, IRC
:slug: instantbird-12-released-with-awesome-new-irc-features

If you haven't seen the announcement...\ `Instantbird 1.2 has been
released`_!  It's got a ton of great new features that I'm excited for:
`better tab complete`_, a marker showing the last viewed messages,
support for Bonjour and more.  But the most exciting bits to me are our
JavaScript implementations of `XMPP`_ (used for `Facebook Chat`_ and
`GTalk`_, so far) and `IRC`_!

Why am I so excited for them? Mostly because they're extendable! 
(Well...and I guess because I wrote most of the IRC code.) I've
`written`_ a bit about this before for IRC...but it will let add-ons do
whatever they want to the IRC protocol.  You should check out the
implementations (links above), they're very hackable.  Hopefully we can
remove libpurple XMPP and fully switch to Instantbird's XMPP for the
next release, once a few `Mozilla bugs`_ are fixed.

Did I also mention that these implementations (including the raw XMPP
and Twitter, which Instantbird has supported since 1.0) are going to be
included in `Thunderbird`_\ 15, as part of it's new `chat feature`_? 
Florian has done a great job of integrating our chat code there and it
gives quite a different user experience than Instantbird, so don't be
worried about Instantbird going away!

Now of course, we always think of the future here (after all,
releasing itself isn't really exciting when most of the features have
been in nightly builds...forever), so we started making a list of some
of the stuff we'd like to implement in future Instantbirds, you can
check it out `here`_. Some of them are very exciting, feel free to grab
one and work on it.

.. _Instantbird 1.2 has been released: http://blog.instantbird.org/2012/08/instantbird-1-2-released/
.. _better tab complete: http://blog.instantbird.org/2012/08/tab-completion-in-instantbird-1-2/
.. _XMPP: http://lxr.instantbird.org/instantbird/source/chat/protocols/xmpp/
.. _Facebook Chat: http://lxr.instantbird.org/instantbird/source/chat/protocols/facebook/
.. _GTalk: http://lxr.instantbird.org/instantbird/source/chat/protocols/gtalk/
.. _IRC: http://lxr.instantbird.org/instantbird/source/chat/protocols/irc/
.. _written: {filename}/irc-auto-performs.rst
.. _Mozilla bugs: https://bugzilla.mozilla.org/show_bug.cgi?id=14328
.. _Thunderbird: http://www.mozilla.org/en-US/thunderbird/
.. _chat feature: https://wiki.mozilla.org/Modules/Chat
.. _here: https://etherpad.mozilla.org/ib-1-3
