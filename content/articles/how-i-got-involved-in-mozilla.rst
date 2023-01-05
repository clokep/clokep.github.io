How I Got Involved in Mozilla
#############################
:date: 2014-10-07 09:31
:author: Patrick Cloke
:tags: Mozilla

This is discussed very briefly on my `about page`_, but I figured it could use a
bit of a longer discussion. I generally consider myself to have joined the
Mozilla_ community in ~2006. I know that I was using Mozilla Firefox, Mozilla
Thunderbird, *and* Mozilla Sunbird way before that (probably since ~2004, which
is when I built my own computer). But I was just an enthusiast then, running
beta builds, then alpha and eventually nightly builds. (This was way back when
things were more dangerous to run: Minefield and Shredder.)

Anyway, back to 2006...I initially got involved in a more technical fashion by
writing extensions (or maybe it was GreaseMonkey_ scripts). I don't really have
anyway to prove this though -- I don't seem to have any of that code. (This was
before widespread distributed version control.) Anyway, let's just assume this
2006 date is correct.

My `first patch`_ was in 2008 to move a function from the `Provider for Google
Calendar`_ to the calendar core so that I could use it in Thundershows_: a
calendar provider for TV shows [#]_ [#]_. (As far as I know, I'm one of a
handful of people to actually implement a `calendar provider`_.) I found the
calendar project much easier to get involved in than other aspects of Mozilla
since it was so much smaller. (I also toyed_ with adding an entire new protocol
to Thunderbird, which `R Kent James`_ has `now done`_ successfully! [#]_ [#]_)

I then came across Instantbird_ in ~2008 (sometime in the Instantbird 0.1 era).
I thought this was great -- Mozilla was finally making an instant messaging
client! Well, I was kind of right...Instantbird is not an official Mozilla
project, but it was exactly what I wanted! The guys (mostly `Florian Quèze`_) in
the `#instantbird`_ IRC channel were awesome: kind, patient, helpful, and
welcoming. They were the ones that really introduced me into the Mozilla way of
doing things. I fixed my first bug for Instantbird in 2010_ and haven't stopped
since! I've since added `IRC support`_ via JavaScript (instead of libpurple) and
am now one of the lead developers. I've mentored Google Summer of Code students
twice (2013 and 2014), contribute to Thunderbird and am a peer of the `chat
code`_ shared between Instantbird and Thunderbird. (I do also occasionally
contribute to other projects. [#]_)

.. [#] This was my first project to really have other users, I had people filing
       bugs, asking for new features, etc. It was great! I even had someone
       (years later) tell me in `#instantbird`_ that they had loved
       Thundershows!
.. [#] My `second bug`_ dealt with the same set of code and had tests committed
       (by me) over 5 years after the initial patch. Oops!
.. [#] My work was based off of some experiments `Joshua Cranmer`_ did to add
       support for `web forums`_ to Thunderbird. After all this time, I still
       want that extension.
.. [#] Oh, also rkent did EXACTLY_ what I wanted years later: which is add
       Twitter to Thunderbird.
.. [#] But not Firefox. After seven years (and over 1800 commits), I've never
       fixed a bug in Firefox; although I have had code_ committed to
       ``mozilla-central``.

.. _about page: {filename}/pages/about.rst
.. _Mozilla: https://www.mozilla.org/
.. _GreaseMonkey: http://www.greasespot.net/
.. _first patch: https://bugzilla.mozilla.org/show_bug.cgi?id=468020
.. _Provider for Google Calendar: https://addons.mozilla.org/en-us/thunderbird/addon/provider-for-google-calendar/
.. _Thundershows: https://bitbucket.org/clokep/thundershows
.. _toyed: https://bitbucket.org/clokep/microblog-mailnews
.. _calendar provider: https://wiki.mozilla.org/Calendar:Creating_an_Extension#Provider_Extensions
.. _R Kent James: http://mesquilla.com/
.. _now done: https://bitbucket.org/rkentjames/skinkglue
.. _Instantbird: http://www.instantbird.com/
.. _Florian Quèze: http://blog.queze.net/
.. _#instantbird: irc://irc.mozilla.org/#instantbird
.. _2010: https://bugzilla.mozilla.org/show_bug.cgi?id=953935
.. _IRC support: https://bugzilla.mozilla.org/show_bug.cgi?id=953944
.. _Thunderbird: http://www.getthunderbird.com
.. _chat code: https://wiki.mozilla.org/Modules/Chat
.. _second bug: https://bugzilla.mozilla.org/show_bug.cgi?id=469477
.. _Joshua Cranmer: http://quetzalcoatal.blogspot.com/
.. _web forums: http://quetzalcoatal.blogspot.com/2010/01/developing-new-account-types-part-0.html
.. _EXACTLY: http://mesquilla.com/extensions/tweequilla/
.. _code: https://bugzilla.mozilla.org/show_bug.cgi?id=884319
