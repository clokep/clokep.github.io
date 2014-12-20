IRC Client Usage Share
######################
:date: 2014-12-13 18:37
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
make a pretty plot of this. (If you're a network administrator reading this and
think this is insane, I'd be very curious to hear a better way to do this!)

Results
=======

In order to get some results I hooked my client up to `moznet`_ and let it run
in some of the main channels. TODO FILL IN THE CHANNELS. I would expect a bit of
skew in these results toward Mozilla-esque IRC clients (Instantbird, Thunderbird
and `ChatZilla`_).

The first thing I noticed is the large amount of information some of these
version responses given...

I plotted the data two separate ways: first by just showing the raw count of
each version response and then by "client family". By "client family" I mean
that all versions of the same client should be counted together. The most sane
way to try to guess this was to take the text up to the first space. These plots
follow [#]_.

.. raw:: html

    <style type="text/css">
        #client-count, #family-count {
          width: 100%;
          height: 300px;
        }
    </style>

    <script type="text/javascript" src="/js/flotr2.min.js"></script>
    <script type="text/javascript">
        function createPlot(aId, aTitle, aData) {
          // Put the data in order from biggest to smallest.
          var data = [d for (d of aData.entries())];
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
            console.log("BOOYAHO");

            var clients = new Map();
            clients.set("Instantbird 1.6pre", 3);
            clients.set("Instantbird 1.5", 1);
            clients.set("Thunderbird", 2);
            clients.set(undefined, 1);

            var families = new Map();
            families.set("Instantbird", 4);
            families.set("Thunderbird", 2);
            families.set(undefined, 1);

            // Update the plots.
            createPlot("client-count", "Clients", clients);
            createPlot("family-count", "Families", families);
        });
    </script>

    <div id="client-count"></div>
    <div id="family-count"></div>

TODO Final results.

.. [#]  "Most" is a wild accusation here. But...from the numbers I've seen, it
        seems like a reasonable statement.
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
