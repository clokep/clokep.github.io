Status Update - February 17, 2011
#################################
:date: 2011-02-17 19:21
:author: Patrick Cloke
:tags: Instantbird, IRC, programming
:slug: status-update-february-17-2011

Another month has gone by so it's time for another status update.
Unfortunately not as much got done this month as I was hoping, but
here's a quick update of what I've worked on:

-  `Bug 690`_ - jsProtoHelper could help registering commands
-  `Bug 661`_ - JavaScript accounts do not automatically set
   containsNick field on messages
-  `Bug 686`_ - Implement default chat name for
   getChatRoomDefaultFieldValues for js-proto

Florian also implemented a few things that are really helpful for
JavaScript protocols:

-  `Bug 649`_ - purple proxies should not be in the way of JavaScript
   protocols
-  `Bug 118`_ - Extensions should be able to register commands.

In addition, Twitter support was added to nightly builds as a
JavaScript protocol (`bug 598`_).

Hopefully next I'll implement most of the commands for IRC (within the
next week) at which point I'll release a sample extension (which will
overwrite the libpurple IRC implementation), allowing people to test
without needing to make a new account, etc.

.. _Bug 690: https://bugzilla.instantbird.org/show_bug.cgi?id=690
.. _Bug 661: https://bugzilla.instantbird.org/show_bug.cgi?id=661
.. _Bug 686: https://bugzilla.instantbird.org/show_bug.cgi?id=686
.. _Bug 649: https://bugzilla.instantbird.org/show_bug.cgi?id=649
.. _Bug 118: https://bugzilla.instantbird.org/show_bug.cgi?id=118
.. _bug 598: https://bugzilla.instantbird.org/show_bug.cgi?id=598
