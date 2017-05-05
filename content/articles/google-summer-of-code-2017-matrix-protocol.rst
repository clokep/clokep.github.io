Google Summer of Code 2017: Matrix protocol for Instantbird and Thunderbird
###########################################################################
:date: 2017-05-05 12:46
:author: Patrick Cloke
:tags: chat, GSoC, instant messaging, Instantbird, Matrix
:slug: google-summer-of-code-2017-matrix-protocol

I'll be mentoring Pavan Karthik on his `project for Google Summer of Code 2017`_
entitled "Matrix Protocol Support for Instantbird". `Matrix`_ is a new(er)
protocol that is an open, decentralized network with some unique features.
Initial support for this landed in `bug 1315926`_, but it is not feature
rich-enough to turn on for users. Pavan will work to finish Matrix support so we
can enable it for all users! The brief description of his proposal is below:

    Matrix is an open, decentralized protocol for instant messaging (and more!)
    It has bridges to many other networks and protocol, e.g. IRC, Slack, and
    more. Initial support for Matrix was added in bug 1199855, but there's a lot
    to do still : Support more features from the Matrix SDK (video/audio calls,
    room topics, typing notifications, read receipts and a lot more.) Support
    one-on-one conversations. Add tests specific to Matrix. Improve the Matrix
    JS-SDK that Instantbird and Thunderbird depend on. Improving and expanding
    shared code and APIs used by all JavaScript protocol plugins (IRC, XMPP,
    Yahoo and Twitter). Improving documentation of the process for adding a
    protocol to Instantbird/Thunderbird. Using the Matrix protocol on a
    day-to-day basis to dog-food the code.

I'm super excited to finalize support for Matrix in both Instantbird and
Thunderbird! You can also checkout the full 25 projects that
`Mozilla accepted`_.

.. _project for Google Summer of Code 2017: https://summerofcode.withgoogle.com/projects/#6473832528347136
.. _Matrix: http://matrix.org/
.. _bug 1315926: https://bugzilla.mozilla.org/show_bug.cgi?id=1315926
.. _Mozilla accepted: https://summerofcode.withgoogle.com/organizations/6421332469219328/
