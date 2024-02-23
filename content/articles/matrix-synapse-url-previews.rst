Synapse URL Previews
####################
:date: 2024-02-23 15:35
:author: Patrick Cloke
:tags: matrix

Matrix includes the ability for a client to request that the server
`generate a "preview" for a URL`_. The client provides a URL to the server which
returns `Open Graph`_ data as a JSON response. This leaks any URLs detected in
the message content to the server, but protects the end user's IP address, etc.
from the URL being previewed. [#]_ (Note that clients generally disable URL previews
for encrypted rooms, but it can be enabled.)

Improvements
============

Synapse implements the URL preview endpoint, but it was a bit neglected. I was
one of the few main developers running with URL previews enabled and sunk a bit of
time into improving URL previews for my on sake. Some highlights of the improvements
made include (in addition to lots and lots of refactoring):

* Support `oEmbed`_ for URL previews:
  `#7920 <https://github.com/matrix-org/synapse/pull/7920>`_,
  `#10714 <https://github.com/matrix-org/synapse/pull/10714>`_,
  `#10759 <https://github.com/matrix-org/synapse/pull/10759>`_,
  `#10814 <https://github.com/matrix-org/synapse/pull/10814>`_,
  `#10819 <https://github.com/matrix-org/synapse/pull/10819>`_,
  `#10822 <https://github.com/matrix-org/synapse/pull/10822>`_,
  `#11065 <https://github.com/matrix-org/synapse/pull/11065>`_,
  `#11669 <https://github.com/matrix-org/synapse/pull/11669>`_ (combine with HTML results),
  `#14089 <https://github.com/matrix-org/synapse/pull/14089>`_,
  `#14781 <https://github.com/matrix-org/synapse/pull/14781>`_.
* Reduction of 500 errors:
  `#8883 <https://github.com/matrix-org/synapse/pull/8883>`_ (empty media),
  `#9333 <https://github.com/matrix-org/synapse/pull/9333>`_ (unable to parse),
  `#11061 <https://github.com/matrix-org/synapse/pull/11061>`_ (oEmbed errors).
* Improved support for document encodings:
  `#9164 <https://github.com/matrix-org/synapse/pull/9164>`_,
  `#9333 <https://github.com/matrix-org/synapse/pull/9333>`_,
  `#11077 <https://github.com/matrix-org/synapse/pull/11077>`_,
  `#11089 <https://github.com/matrix-org/synapse/pull/11089>`_.
* Support previewing XML documents (`#11196 <https://github.com/matrix-org/synapse/pull/11196>`_)
  and ``data:`` URIs (`#11767 <https://github.com/matrix-org/synapse/pull/11767>`_).
* Return partial information if images or oEmbed can't be fetched:
  `#12950 <https://github.com/matrix-org/synapse/pull/12950>`_,
  `#15092 <https://github.com/matrix-org/synapse/pull/15092>`_.
* Skipping empty Open Graph (``og``) or ``meta`` tags:
  `#12951 <https://github.com/matrix-org/synapse/pull/12951>`_.
* Support previewing from `Twitter card information`_:
  `#13056 <https://github.com/matrix-org/synapse/pull/13056>`_.
* Fallback to favicon if no images found:
  `#12951 <https://github.com/matrix-org/synapse/pull/12951>`_.
* Ignore navgiation tags: `#12951 <https://github.com/matrix-org/synapse/pull/12951>`_.
* Document how Synapse `generates URL previews`_:
  `#10753 <https://github.com/matrix-org/synapse/pull/10753>`_,
  `#13261 <https://github.com/matrix-org/synapse/pull/13261>`_.

I also helped review many changes by others:

* Improved support for encodings: `#10410 <https://github.com/matrix-org/synapse/pull/10410>`_.
* Safer content-type support: `#11936 <https://github.com/matrix-org/synapse/pull/11936>`_.
* Attempts to fix Twitter previews: `#11985 <https://github.com/matrix-org/synapse/pull/11985>`_.
* Remove useless elements from previews: `#12887 <https://github.com/matrix-org/synapse/pull/12887>`_.
* Avoid crashes due to unbounded recursion:
  `GHSA-22p3-qrh9-cx32 <https://github.com/matrix-org/synapse/security/advisories/GHSA-22p3-qrh9-cx32>`_.

And also fixed some security issues:

* Apply ``url_preview_url_blacklist`` to oEmbed and pre-cached images:
  `#15601 <https://github.com/matrix-org/synapse/pull/15601>`_.

Results
=======

Overall, there was an improved result (from my point of view). A summary of some
of the improvements. I tested 26 URLs (based on ones that had previously been
reported or found to give issues). See the table below for testing at a few versions.
The error reason was also broken out into whether JavaScript was required or some
other error occurred. [#]_

+---------+--------------+--------------------+---------------------------+----------------------------+
| Version | Release date | Successful preview | JavaScript required error | Found image & description? |
+=========+==============+====================+===========================+============================+
| 1.0.0   | 2019-06-11   | 15                 | 4                         | 14                         |
+---------+--------------+--------------------+---------------------------+----------------------------+
| 1.12.0  | 2020-03-23   | 18                 | 4                         | 17                         |
+---------+--------------+--------------------+---------------------------+----------------------------+
| 1.24.0  | 2020-12-09   | 20                 | 1                         | 16                         |
+---------+--------------+--------------------+---------------------------+----------------------------+
| 1.36.0  | 2021-06-15   | 20                 | 1                         | 16                         |
+---------+--------------+--------------------+---------------------------+----------------------------+
| 1.48.0  | 2021-11-30   | 20                 | 1                         | 11                         |
+---------+--------------+--------------------+---------------------------+----------------------------+
| 1.60.0  | 2022-05-31   | 21                 | 0                         | 21                         |
+---------+--------------+--------------------+---------------------------+----------------------------+
| 1.72.0  | 2022-11-22   | 22                 | 0                         | 21                         |
+---------+--------------+--------------------+---------------------------+----------------------------+
| 1.84.0  | 2023-05-23   | 22                 | 0                         | 21                         |
+---------+--------------+--------------------+---------------------------+----------------------------+

Future improvements
===================

I am no longer working on Synapse, but some of the ideas I had for additional improvements
included:

* Use `BeautifulSoup`_ instead of a custom parser to handle some edge cases in HTML
  documents better (WIP @ |bs4|_).
* Always request both oEmbed and HTML (WIP @ |oembed-and-html|_).
* Structured data support (`JSON-LD`_, `Microdata`_, `RDFa`_) (`#11540 <https://github.com/matrix-org/synapse/issues/11540>`_).
* Some minimal JavaScript support (`#14118 <https://github.com/matrix-org/synapse/issues/14118>`_).
* Fixing any of the other issues with particular URLs (see this `GitHub search`_).
* Thumbnailing of SVG images (which sites tend to use for favicons) (`#1309 <https://github.com/matrix-org/synapse/issues/1309>`_).

There's also a ton more that could be done here if you wanted, e.g. handling more
data types (text and PDF are the ones I have frequently come across that would be
helpful to preview). I'm sure there are also many other URLs that don't work right
now for some reason. Hopefully the URL preview code continues to improve!

.. [#] See some `ancient documentation`_ on the tradeoffs and design of URL previews.
       :msc:`4095` was recently written to bundle the URL preview information into
       evens.

.. [#] This was done by instantiating different Synapse versions via Docker and
       asking them to preview URLs. (See `the code`_.) This is not a super realistic
       test since it assumes that URLs are static over time. In particular some
       sites (e.g. Twitter) like to change what they allow you to access without
       being authenticated.

.. _generate a "preview" for a URL: https://spec.matrix.org/v1.8/client-server-api/#get_matrixmediav3preview_url
.. _Open Graph: https://ogp.me/
.. _oEmbed: https://oembed.com/
.. _Twitter card information: https://developer.twitter.com/en/docs/twitter-for-websites/cards/guides/getting-started
.. _generates URL previews: https://github.com/matrix-org/synapse/blob/be65a8ec0195955c15fdb179c9158b187638e39a/synapse/media/url_previewer.py#L101-L154
.. _BeautifulSoup: https://www.crummy.com/software/BeautifulSoup/
.. |bs4| replace:: ``clokep/bs4``
.. _bs4: https://github.com/matrix-org/synapse/tree/clokep/bs4
.. |oembed-and-html| replace:: ``clokep/oembed-and-html``
.. _oembed-and-html: https://github.com/matrix-org/synapse/tree/clokep/oembed-and-html
.. _JSON-LD: https://json-ld.org/
.. _Microdata: https://html.spec.whatwg.org/multipage/
.. _RDFa: https://rdfa.info/
.. _GitHub search: https://github.com/matrix-org/synapse/issues?q=is%3Aissue+is%3Aopen+sort%3Aupdated-desc+label%3AA-URL-Preview+

.. _ancient documentation: https://github.com/matrix-org/matrix-spec/blob/main/attic/drafts/url_previews.md
.. _the code: https://github.com/clokep/test-matrix-url-previews/tree/e0e20154ec348fc25d203546ddede0c881b9772a/docker
