RSS Feeds for Wikipedia Current Events and NHL News
###################################################
:date: 2017-05-26 08:13
:modified: 2017-09-13 17:15
:author: Patrick Cloke
:tags: programming, python, RSS

I subscribe to a fair amount of feeds for news, blogs, articles, etc. I'm
currently subscribed to 122 feeds, some of which have tens of articles a day
(news sites), some of which are dead. [#]_ Unfortunately there's still a few
sites that I was visiting manually each day to get updates from because they
don't offer any feeds. This included:

* The `Wikipedia Current Events portal`_, which usually has a nice daily summary
  of interesting worldwide stories. [#]_
* The `NHL News`_ (and specifically the `Islanders News`_) pages. (I still
  follow a `broken feed`_ from the older site, but it seems one of the redesigns
  of the NHL team sites broke this feed.)

Having the Wikipedia Current Events as a feed is a pretty specific thing that's
outside of the scope of `MediaWiki`_, so I can understand why that doesn't
exist. The NHL not having news feeds over RSS or Atom though? That shocks me! I
hope I've just been unable to find them and that they do exist. Please point me
to them if they do!

Wikipedia Current Events
========================

The Wikipedia Current Events feed is `publically available`_, code can be found
in the GitHub repository: `clokep/wp-current-events-rss`_. Note that this pulls
data on demand and thus always serves the most up-to-date versions of the
articles. This works by:

1.  Pulling the last 7 days of Wikipedia's current event articles (e.g. like
    `this one`_) using `requests`_. Each of these is processed individually as a
    separate article in the RSS feed.
2.  The `wikicode`_ for each article is converted to an `AST`_ using
    `mwparserfromhell`_
3.  Some of the headers and templates are removed from each article.
4.  It then converts each article *back* to HTML. (This was the surprisingly
    hard part. I couldn't find a good library to do this and ended up
    `writing this myself`_.)
5.  The articles are then turned into an RSS feed using `feedgenerator`_.
6.  The feed itself is served via `Flask`_.

Feel free to `check it out`_ and `let me know of any issues`_!

NHL News
========

After building the above, I figured there was no reason not to do the same for
the NHL News section (and specifically for the Islanders). You can `see the NHL
feed`_ or `pick your favorite team`_. Again, the code is available on GitHub:
`clokep/nhl-news-rss`_. The stack is pretty similar to the above, it works by:

1.  Pulling the current NHL News page.
2.  Parsing the HTML with `BeautifulSoup4`_ to pull out each article's title,
    date, author, and short summary. (Note that the full article isn't
    available, we could get it by loading each article individually, but I
    didn't implement that.)
3.  The articles are then turned into an RSS feed using `feedgenerator`_.
4.  The feed itself is served via `Flask`_.

Luckily the NHL News site and the news page for each team are in the same
format, so it's just loading different URLs to get the different articles. It
was pretty trivial to get the full list of teams and add support for all of
them, so that's included too! Articles are pulled during page load, so should
always be up to date.

I hope one (or both) of these are useful to people! Again, please
`let me know if you have any issues or ideas`_!

.. [#]  I recently switched from using `Thunderbird`_ to `Feedly`_ in order to
        get cross device read status syncing on articles, but that's not really
        related to the rest of this article. Switching has mostly worked out
        well, but I do miss the filtering capabilities of Thunderbird!

        I also tried a few other services (e.g. `The Old Reader`_), but most had
        too many weird social features. I just wanted to read feeds.
.. [#]  I do know that Wikipedia page updates can be consumed via RSS, but I
        don't want to know every time the article is updated, just the state of
        the article at the end of the day. (It also doesn't work for the current
        events article since it's dynamically generated from a bunch of
        templates.)

.. note::

    An update, as of September 13, 2017:

    1. The links to each RSS feed were updated.
    2. These apps are now hosted together on https://www.to-rss.xyz.
    3. These projects are no longer being updated on GitHub. The combined site
       might be open sourced in the future.

.. _Wikipedia Current Events portal: https://en.wikipedia.org/wiki/Portal:Current_events
.. _NHL News: https://www.nhl.com/news
.. _Islanders News: https://www.nhl.com/islanders/news
.. _broken feed: http://islanders.nhl.com/rss/news.xml
.. _MediaWiki: https://www.mediawiki.org/
.. _publically available: https://www.to-rss.xyz/wikipedia/current_events/
.. _clokep/wp-current-events-rss: https://github.com/clokep/wp-current-events-rss
.. _this one: https://en.wikipedia.org/wiki/Portal:Current_events/2017_May_8
.. _requests: http://python-requests.org/
.. _wikicode: https://en.wikipedia.org/wiki/Help:Wiki_markup
.. _AST: https://en.wikipedia.org/wiki/Abstract_syntax_tree
.. _mwparserfromhell: http://mwparserfromhell.readthedocs.io/
.. _writing this myself: https://github.com/clokep/wp-current-events-rss/blob/7a6e2eb12d7fbe6efae6659dda65e2ad24e89611/parser.py#L23-L193
.. _feedgenerator: https://github.com/getpelican/feedgenerator/
.. _Flask: http://flask.pocoo.org/
.. _check it out: https://www.to-rss.xyz/wikipedia/
.. _let me know of any issues: https://github.com/clokep/wp-current-events-rss/issues/new
.. _see the NHL feed: https://www.to-rss.xyz/nhl/news/
.. _pick your favorite team: https://www.to-rss.xyz/nhl/
.. _clokep/nhl-news-rss: https://github.com/clokep/nhl-news-rss
.. _BeautifulSoup4: https://www.crummy.com/software/BeautifulSoup/bs4/
.. _let me know if you have any issues or ideas: https://github.com/clokep/nhl-news-rss/issues/new

.. _Thunderbird: http://thunderbird.net
.. _Feedly: https://feedly.com
.. _The Old Reader: https://theoldreader.com
