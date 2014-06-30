Adding a protocol to Instantbird (Part 2)
#########################################
:date: 2011-09-03 14:31
:author: Patrick Cloke
:tags: Instantbird, programming, SIPE
:slug: adding-a-protocol-to-instantbird-part-2

.. contents::

I had `previously talked about adding a protocol to Instantbird`_,
that focused on adding SIPE (Microsoft Office Communicator support). 
Since then I've been slowly working on defeating SIPE.  Fortunately I
found a few flags that help us compile it easily in Instantbird: we can
declare that we do *not* have gmime and the standard libpurple MIME
functions will be used (they might not be as good, but it keeps from
adding >10 MB of source to Instantbird).

Some modifications to the SIPE source were made to compile it in
Instantbird (note that most of the changes were probably more based on
using MSVC, than having to do with Instantbird).  The code is also
broken up into a few different sections the core, api, and purple are
ones we care about (they're working on making a general Office
Communicator protocol library, so the purple folder contains the
libpurple bindings that use the api, while the core is private).

Purple
======

Changes to purple consisted mostly of ifdefs that remove some header
files not supported on Windows.  For example, I encountered a few of: ::

    #include <unistd.h>

Luckily there was already a define ``HAVE_UNISTD_H``, so I just needed
to add: ::

    #ifdef HAVE_UNISTD_H
    #include <unistd.h>
    #endif

Easy!  There were also a couple other issues, but those were rather
trivial.

Core
====

There isn't a specific issue in the core I'd like to highlight, it did
use a few glib functions which we didn't have (we removed the files, as
they were unused), they were all reimplemented in libpurple though, so
we were able to just define the function calls to the libpurple
variants.

API
===

This had similar issues the core (in particular, there was a function
which used ``g_usleep``, which is blocking and a definite no-no for a
protocol plug-in, I've removed that...hopefully it doesn't break
anything!)  In addition to that, we needed to use the libpurple l10n
system instead of glib's gi18n.h, this was easily copied from
libpurple's internal API though.

So at this point...I have a copy of SIPE compiled!  Unfortunately
since I'm using Visual Studio Express I cannot compile on my computer
and deploy to other computers for testing (a Mozilla issue with how it
uses some of the header files, etc., I believe).  I'm looking into
trying to get this to work though, apparently using the exact same copy
of MSVC Redistributable might help.  Once this is tested, hopefully
it'll land in Instantbird for use!

Sametime support
================

Unrelated to SIPE, but recently I landed a patch in Instantbird to add
back Sametime support (Sametime is Lotus Notes' equivalent to Office
Communicator).  You can see the gory details in `bug 102`_, but in
general it's similar to what I've (not gone into great detail about)
here. Most of getting Sametime to work was rewriting some C code
that doesn't compile in MSVC.  There's also a `diff`_ of all the
changes I made to the libpurple Sametime plugin and the external library
(called `Meanwhile`_) to get it to work.  Once I get Monotone (a version
control system) set up I'll look into getting these changes pushed back
to libpurple to avoid diverging code bases.

.. _previously talked about adding a protocol to Instantbird: {filename}/adding-a-new-protocol-sipeoffice-communicator-to-instantbird-part-1.rst
.. _bug 102: https://bugzilla.instantbird.org/show_bug.cgi?id=102
.. _diff: https://bugzilla.instantbird.org/attachment.cgi?id=797&action=diff
.. _Meanwhile: http://meanwhile.sourceforge.net/
