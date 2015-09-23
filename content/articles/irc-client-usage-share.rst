IRC Client Usage Share on moznet
################################
:date: 2015-09-23 17:07
:author: Patrick Cloke
:tags: Mozilla, Thunderbird, Instantbird, IRC

.. contents::

Background
==========

The usage share of IRC clients has always been something I'm interested in. This
is partially to see how many people are using `Instantbird`_ or `Mozilla
Thunderbird`_ for IRC (as I've written much of the IRC code for those clients).
`Usage share of browsers`_ is quite a researched topic, but I've never come
across this data for IRC. Most [#]_ IRC clients implement a part of the `CTCP`_
protocol which allows a client to query another client for their version.
Thinking of this as a `user agent`_ is probably a good analogue. I don't think
this would imply that there is much of an issue with `user agent spoofing`_, as
there would be for web browser statistics since (as far as I know), no one uses
the version response to do capability negotiation. It also is not used by
servers.

Technical Bits
==============

So how'd we do this? I wrote an `extension`_ for Instantbird which handled both
the backend and the display of the results. I think that this really showcases
the extensibility of Instantbird and the effort we've put into ensuring their
are generic APIs available for developers. In particular this uses the `IRC
handler API`_ and the `add panel API`_ (added by `one of our GSoC students`_ a
couple of years ago.)

Anyway, at the actual protocol level, I simply send a ``CTCP VERSION`` query to
each user I know of on the IRC network (based on who is in the same channels as
me) and then record the responses. I tried to be nice to the network here and
rate-limited myself to 1 query per second. No one complained after ~100 queries
and I didn't seem to have any ``fakelag`` issues. I then dumped the results and
made a pretty(-ish) plot of this. (If you're a network administrator reading
this and think this is insane, I'd be very curious to hear a better way to do
this!)

Results
=======

In order to get some results I hooked my client up to `moznet`_ on July 23rd,
2015 and let it run on many channels (pretty much anything with more than 20
users) for a few hours [#]_. I was in Europe and started early in the morning
and let it run through the evening, so it should encompass some "normal" usage
by Mozillians. I would expect a bit of skew in these results toward
Mozilla-esque IRC clients (Instantbird, Thunderbird and `ChatZilla`_).

Of course these numbers are just a single sampling and I have no idea how much
variance there is day-to-day or over time, but I found the (un-scientific)
results to be interesting!

Responses
'''''''''

The first thing I noticed is the large amount of information some version
responses gave (in no particular order):

* ``KVIrc 4.3.1 svn-6313 'Aria' 20120701 - build 2013-02-14 17:47:33 UTC - Windows 7 Ultimate (x64) Service Pack 1 (Build 7601)``
* ``xchat 2.8.8 Linux 3.17.4-1-ARCH [x86_64/2.90GHz/SMP]``
* ``HexChat 2.10.1 [x64] / Windows 7 SP1 [4.09GHz]``

I don't understand the rationale behind sharing a user's operating system and
CPU speed. Most clients responded with a simple ``<software> <version number>``,
although quite a few also include a URL.

Client Summary
''''''''''''''

Initially I visualized the data by plotting it two serparate ways: first by
showing the count of each version response and then grouping by "client family".
The first plot had too many columns to reasonably show in this post: thus I've
only included a plot of the client families [#]_. There are two plots, the first
shows a subset of the data by cutting the tail (arbitrarily including families
with at least 10 users).

.. note::

    A "client family" is counting all versions of the same client together. This
    was calculated by taking the text up to the first whitespace or digit and
    converting to lowercase:

    .. code-block:: javascript

        family = version.split(/[\s\d]/)[0].toLowerCase()

.. raw:: html

    <style type="text/css">
        #family-all-count, #family-count {
          width: 100%;
          height: 300px;
        }
    </style>

    <script type="text/javascript" src="/js/flotr2.min.js"></script>
    <script type="text/javascript">
        function createPlot(aId, aTitle, aData) {
          // Put the data in order from biggest to smallest.
          var data = []
          for (var d of aData.entries())
            data.push(d);
          data.sort(function(a, b) a[1] < b[1]);

          // Re-arrange the data to be plotted into two arrays: one is a set of points
          // of x-index to value, the other is x-index to label.
          var labels = [];
          for (var i = 0; i < data.length; i++) {
            // Sometimes the labels are stupid long.
            labels[i] = [i, (data[i][0] || "undefined").slice(0, 25)];
            data[i] = [i, data[i][1]];
          }

          var options = {
            title: aTitle,
            HtmlText: false,
            bars: {
              show: true,
              shadowSize: 0,
              barWidth: 0.5
            },
            mouse: {
              track: true,
              relative: true
            },
            xaxis: {
              ticks: labels,
              labelsAngle: 90
            },
            yaxis: {
              min: 0,
              autoscaleMargin: 1,
              title: "Count",
              titleAngle: 90
            }
          };

          var plot = document.getElementById(aId);
          Flotr.draw(plot, [data], options);
        }

        document.addEventListener("DOMContentLoaded", function() {
            var families = new Map([["instantbird", 21], ["thunderbird", 39], ["xchat", 77], ["colloquy", 33], ["limechat", 61], ["irssi", 204], ["irccloud", 520], ["znc", 161], ["icedove", 3], ["chatzilla", 59], ["bip-", 11], ["hexchat", 61], ["mozbot", 3], ["miranda", 6], ["mirc", 31], ["textual", 44], ["weechat", 76], ["kvirc", 6], ["purple", 70], ["x-chat", 8], ["xchat-wdk", 1], ["dircproxy", 1], ["konversation", 12], ["quassel", 69], ["linkinus", 3], ["\x02erc\x02", 6], ["leroooooy", 1], ["elitebnc", 1], ["fu,", 1], ["anope-", 1], [">", 2], ["telepathy-idle", 3], ["rcirc", 3], ["mrgiggles:", 1], ["ircii", 1], ["http://www.mibbit.com", 4], ["shout", 7], ["yaaic", 2], ["karen", 1], ["", 3], ["sceners", 1], ["uberscript", 1], ["tiarra:", 3], ["snak", 1], ["wuunyan", 1], ["adiirc", 1], ["n/a", 1], ["pircbotx", 3], ["none", 1], ["yes", 1], ["nettalk", 1], ["riece/", 1], ["unknown", 1], ["version", 1], ["circ", 3], ["request", 1], ["forrest,", 1], ["trillian", 1], ["\x03", 2], ["smuxi-frontend-gnome", 1], ["some", 1], ["\x02\x03", 1], ["oh", 1], ["\u201Cnever", 1], ["this", 1], ["nochat", 1], ["wee", 1], ["foadirc", 1], ["smuxi-server", 1], ["aperture", 1], ["internet", 1], ["supybot", 1], ["ejabberd", 2], ["dxirc", 1], ["ircle", 1], ["infobot", 1], ["exovenom", 1], ["nsa-irc", 1]]);

            // Count the totals, used in reporting not actually displayed.
            var total = 0;
            for (var family of families.entries())
                total += family[1];

            // Update the plots.
            createPlot("family-all-count",
                       "All Families (Total: " + total + ")", families);

            // Remove all families that have less than 10 hits.
            for (var family of families.entries()) {
                if (family[1] < 10) {
                    families.delete(family[0])
                    total -= family[1];
                }
            }

            createPlot("family-count",
                       "Families with at Least 10 Users (Total: " + total + ")",
                       families);
        });
    </script>

    <div id="family-count"></div>
    <div id="family-all-count"></div>

Points of Note
''''''''''''''

I have to admit that I was fairly shocked by the number of IRCCloud users as I
found it pretty unusable when messing with it. I suspect it being an 'easy'
bouncer draws many people to it. The bouncer-like software (IRCCloud, ZNC, bip)
represents almost half of the users surveyed (692 / 1549 ≈ 45%)!

I'm surprised so many people are using ``purple`` as their IRC client, as the
support there is really barebones. (It makes sense if you're already using
Pidgin and don't want another client.) I think we've made a significant amount
of improvements in Instantbird's IRC support to make it simpler for a user to
get started (give it a try if you haven't!).

The last thing I'll note that, when taken together, Instantbird and Thunderbird
come in as part of the top 10 (60 users, right before ChatZilla)! There's a lot
of great clients out there and I'm happy to say I've helped to create one of the
more popular ones (on moznet, at least!).

Let me know if I missed a great insight!

.. [#]  "Most" is a wild accusation here. But...from the numbers I've seen, it
        seems like a reasonable statement.
.. [#]  While running this I had a few users question what I was doing over
        private messages or in a channel. I'm *shocked* that clients bother
        their users by showing them they received a ``VERSION`` request. (Most)
        users just won't care! Why show that low-level of the protocol?!
.. [#]  I stole the code to plot this from the `plotting code`_ in the extension
        I wrote for this. When actually using that extension, something similar
        to this appears as a tab and refreshes as results come in. It uses
        `Flotr2`_ to do the plotting in JavaScript, I've been pretty happy with
        it.

.. _Mozilla Thunderbird: https://www.mozilla.org/en-US/thunderbird/
.. _Instantbird: http://instantbird.com/
.. _Usage share of browsers: http://en.wikipedia.org/wiki/Usage_share_of_web_browsers
.. _CTCP: http://www.irchelp.org/irchelp/rfc/ctcpspec.html
.. _user agent: http://en.wikipedia.org/wiki/User_agent
.. _user agent spoofing: http://en.wikipedia.org/wiki/Usage_share_of_web_browsers#User_agent_spoofing
.. _extension: https://bitbucket.org/clokep/irc-extras/src/tip/stats/
.. _IRC handler API: http://dxr.mozilla.org/comm-central/source/chat/protocols/irc/ircHandlers.jsm
.. _add panel API: http://hg.mozilla.org/comm-central/file/dbab5a531594/im/content/tabbrowser.xml#l432
.. _one of our GSoC students: http://blog.nhnt11.com/
.. _moznet: https://wiki.mozilla.org/IRC
.. _ChatZilla: http://chatzilla.hacksrus.com/

.. _plotting code: https://bitbucket.org/clokep/irc-extras/src/41a9572caf957ab8ae3969a145834bcd5be74abe/stats/content/ircStats.js?at=default#cl-55
.. _Flotr2: http://humblesoftware.com/flotr2/
