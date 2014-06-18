Status Update - January 18, 2011
################################
:date: 2011-01-19 03:17
:author: Patrick Cloke
:category: Mozilla
:tags: Instantbird, IRC, Mozilla, programming
:slug: status-update-january-18-2011

I haven't had an update in a few weeks (since early December)
actually, so I thought I would post a bit about what I've worked on. 
I've fixed a bunch of bugs in the backend of Instantbird that allow work
on JavaScript IRC protocol to continue:

-  `Bug 519`_ - Extend jsProtoHelper to implement purpleIConvChat
   (`check-in`_)
-  `Bug 495`_ - purpleIAccount cannot access preferences via JavaScript
   protocol (`check-in <http://hg.instantbird.org/instantbird/rev/a188a5cc3ff1>`__)
-  `Bug 648`_ -Provide a default JS implementation of
   purpleIChatRoomField
   (`check-in <http://hg.instantbird.org/instantbird/rev/61fc80a569d3>`__)
-  [Reviewed] `Bug 647`_ - Username split for JavaScript protocols
   (`check-in <http://hg.instantbird.org/instantbird/rev/a6c8fbf77e10>`__)
-  [Reviewed] <no bug> -Share the nsIClassInfo implementation between
   all the objects implemented in jsProtoHelper
   (`check-in <http://hg.instantbird.org/instantbird/rev/035f7d8d7f78>`__)

Also a few other random bugs I've worked on:

-  `Bug 625`_ - Findbar broken on Windows in Conversation window
   (`check-in <http://hg.instantbird.org/instantbird/rev/2e8af77af2f2>`__)
-  `Bug 629`_ - Remove workaround for bug 503048
   (`check-in <http://hg.instantbird.org/instantbird/rev/ba4b9401791b>`__)
-  `Bug 473`_ - JS Logger line breaks don't play well on Windows
   `(check-in`_)
-  `Bug 593`_ - JavaScript component does not have a method named:
   "onBeforeLinkTraversal"
   (`check-in <http://hg.instantbird.org/instantbird/rev/1b75f9fa4859>`__)

Although none of these are really things that weren't working a few
weeks ago, there are now real APIs for these for JavaScript protocols,
allowing other protocols to use them and to *FULLY* implement them
instead of hard coding values.  In addition, a lot of the purplexpcom
layer is now hidden from JavaScript protocols.

There's a few things left to do for the JavaScript protocol layer:

-  `Bug 118`_ - Extensions should be able to register commands.
-  `Bug 650`_ - JavaScript accounts must be notified of status changes
   (a sketchy patch that exists that will work, but a better patch to
   core should be done)
-  `Bug 623`_ - Auto-Join option field is hard coded for certain
   protocols (not *really* necessary, since it's still IRC, but it
   should be fixed)
-  `Bug 649`_ - Proxy should be available to JavaScript protocols
   (hopefully being handled by Florian)

A good summary of this is `the dependency graph of bug 507`_
(Implement IRC in JavaScript).  Note that the IRC JavaScript work blocks
*a  lot* of UI work done for IRC.  In particular Mook has been working
on implementing notifications (i.e. Invites, and perhaps a few other
commands), see `Bug 628`_.  For other bugs, see the link above -- and if
there's a strange UI feature that you think should be added, please file
a bug and let us know about it!

I've also worked a bit on sending outgoing text with rich formatting
(bold, italics, underline, text size, etc.), this work is being tracked
in `Bug 634`_. There's a proof on concept, but a lot of work needs to be
done for it, but it's sort of working right now. 

As I alluded to in my last blog post, the JavaScript protocols would
be used to implement Twitter. Work for this is occurring in `Bug 598`_,
where Florian has implemented (very) basic Twitter support.

My plans for the next bit:

-  I'm hoping to finish up some of the work blocking JavaScript
   protocols so IRC can be put into a state that needs alpha/beta
   testers (if you're interested in testing/hacking please drop me a
   line here, on IRC or via email).
-  Move into my new apartment
-  Start my new job
-  Work on richtext messages a bit more

.. _Bug 519: https://bugzilla.instantbird.org/show_bug.cgi?id=519
.. _check-in: http://hg.instantbird.org/instantbird/rev/0166084ce2ae
.. _Bug 495: https://bugzilla.instantbird.org/show_bug.cgi?id=495
.. _Bug 648: https://bugzilla.instantbird.org/show_bug.cgi?id=648
.. _Bug 647: https://bugzilla.instantbird.org/show_bug.cgi?id=647
.. _Bug 625: https://bugzilla.instantbird.org/show_bug.cgi?id=625
.. _Bug 629: https://bugzilla.instantbird.org/show_bug.cgi?id=629
.. _Bug 473: https://bugzilla.instantbird.org/show_bug.cgi?id=473
.. _(check-in: http://hg.instantbird.org/instantbird/rev/6a600b8a32c9
.. _Bug 593: https://bugzilla.instantbird.org/show_bug.cgi?id=593
.. _Bug 118: https://bugzilla.instantbird.org/show_bug.cgi?id=118
.. _Bug 650: https://bugzilla.instantbird.org/show_bug.cgi?id=650
.. _Bug 623: https://bugzilla.instantbird.org/show_bug.cgi?id=623
.. _Bug 649: https://bugzilla.instantbird.org/show_bug.cgi?id=649
.. _the dependency graph of bug 507: https://bugzilla.instantbird.org/showdependencygraph.cgi?id=507&display=web&rankdir=LR
.. _Bug 628: https://bugzilla.instantbird.org/show_bug.cgi?id=628
.. _Bug 634: https://bugzilla.instantbird.org/show_bug.cgi?id=634
.. _Bug 598: https://bugzilla.instantbird.org/show_bug.cgi?id=598
