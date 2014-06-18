Shared Lightning profile across Linux and Windows
#################################################
:date: 2011-07-08 00:46
:author: Patrick Cloke
:tags: Lightning, Mozilla
:slug: shared-lightning-profile-across-linux-and-windows

In `#calendar on Mozilla IRC`_ the past few days a user has been
asking about using a shared profile on Thunderbird between Linux and
Windows ("shared" meaning a dual boot system of Linux/Windows, but not
at the same time, obviously).  Generally this isn't a big deal UNLESS
you have a binary extension, in which case you'd have to reinstall the
extension every time! That's awfully lame.

BUT there should be a way to make a unified extension for all
operating systems.  In fact `ssitter had written an article to do
that`_.  It needs some updating to account for the Mozilla 2 XPCOM
changes, however.

The steps are mostly the same, with some added.

#. Download whatever versions you want (`perhaps 1.0b4`_?).
#. Unzip them all and choose which one will be your "unified" version.
#. Find the <em:targetPlatform> section in the install.rdfs and include
   all the necessary ones.
#. Find the libcalbasecomps.\* (where \* is dll, dylib, so, etc. for
   your platform) inside the components directories.
#. Copy the libraries together into one directory.
#. Copy the lines from each components.manifest together into one
   manifest.
#. For some systems you'll need to specify the ABI (and possibly change
   the path), note that the ABI is just what was inside the
   <em:targetPlatform>.
#. Rezip this up into an XPI and you should be good to go!

In my test I ended up with an XPI that was approximately 10% bigger
after combining Mac (x86 and x64), Linux (x86 and x64), Win32, Solaris
Sparc and Solaris x86.  Why is this not done by default?  Probably just
cause no one has done it...there is a `bug about it`_ though.  One issue
that might be encountered using this method is pre-processing of some
script files (as is discussed in that big) but hopefully it should
"mostly" work.  (Note that this is mostly untested.)

**Edit:** I should also mention that you would need to do something
similar with the themes folders if they differ dramatically (it seems
there's `just two`_: winstripe and pinstripe: i.e. Windows & Mac; Linux
and Solaris most likely also use winstripe).

.. _#calendar on Mozilla IRC: irc://irc.mozilla.org/calendar
.. _ssitter had written an article to do that: https://wiki.mozilla.org/User:Ssitter/UnifiedLightning
.. _perhaps 1.0b4: http://releases.mozilla.org/pub/mozilla.org/calendar/lightning/releases/1.0b4/
.. _bug about it: https://bugzilla.mozilla.org/show_bug.cgi?id=352543
.. _just two: http://mxr.mozilla.org/comm-central/source/calendar/lightning/themes/
