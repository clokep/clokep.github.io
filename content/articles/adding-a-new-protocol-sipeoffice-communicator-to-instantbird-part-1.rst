Adding a new protocol (SIPE/Office Communicator) to Instantbird (part 1)
########################################################################
:date: 2011-06-18 21:53
:author: Patrick Cloke
:tags: Instantbird, programming, SIPE
:slug: adding-new-protocol-sipeoffice

`Microsoft Office Communicator`_ is an instant messaging client that
integrates into the `Exchange Messaging Server`_ (the protocol behind it
is an extended version of SIP/SIMPLE). Anyway, there's a `libpurple`_
(i.e. the backend of `Instantbird`_ and `Pidgin`_) protocol plug-in for
OCS (Office Communicator Server) called `SIPE`_. (It's also striving
for a generic library to connect to OCS, but that's not quite there
yet.)

I've been interested in getting this to compile in the Instantbird
framework for a while now, adding a new protocol to Instantbird. First
of course I need the SIPE source, I chose to grab a release `source
bundle`_ instead of using the `git repository`_, just for ease moving
files around, etc. There's a rather vague `Windows build`_ page on the
wiki that I started with, says I need:

-  libpurple >2.4.0 (we have 2.7.11)
-  libglib >2.12.0 (we have 2.28.6)
-  libxml2 (we have this)
-  gmime >2.4 (not currently used)

So great, `we have most of the dependencies`_! We just need one more.
So I go grab, `gmime`_ from the GNOME website (2.5.7, which is the
newest stable, currently), again as a source bundle and put the
necessary files in purple/libraries/gmime and edit the makefile so it
will (attempt) to compile. But great -- it requires `libiconv`_, which
apparently is very difficult to compile, especially on Windows. Luckily
for me there's a Windows version (not a port, but one that uses the
native Win32 APIs with the same interface): `win-iconv`_. This compiled
like a champ when added as purple/libraries/iconv.

Unfortunately when I went back to compiling gmime, it attempts to
access parts of glib we're not using (gio, in particular) and thus is
not in our source code. I can grab the `glib`_ source (2.28.6 to match,
of course) and add the gio subfolder, but first we should check if this
part of gmime is even used by SIPE! (My guess is that it is *not*, but
that's where I'm at now. I'll post back when I get further.

.. _Microsoft Office Communicator: http://en.wikipedia.org/wiki/Office_Communicator
.. _Exchange Messaging Server: http://en.wikipedia.org/wiki/Microsoft_Exchange_Server
.. _libpurple: http://developer.pidgin.im/wiki/WhatIsLibpurple
.. _Instantbird: http://instantbird.com/
.. _Pidgin: http://pidgin.im/
.. _SIPE: http://sipe.sourceforge.net/
.. _source bundle: http://sourceforge.net/projects/sipe/files/sipe/pidgin-sipe-1.11.2/
.. _git repository: 
.. _Windows build: http://sourceforge.net/apps/mediawiki/sipe/index.php?title=Windows_Build
.. _we have most of the dependencies: https://wiki.instantbird.org/Instantbird:Third_party_code
.. _gmime: http://developer.gnome.org/gmime/
.. _libiconv: http://www.gnu.org/software/libiconv/
.. _win-iconv: http://code.google.com/p/win-iconv/
.. _glib: http://developer.gnome.org/glib/
