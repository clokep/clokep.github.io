Compiling Instantbird
#####################
:date: 2011-05-17 01:30
:author: Patrick Cloke
:category: Mozilla
:tags: Instantbird, Mozilla, programming
:slug: compiling-instantbird

In the past I've tried to compile a few different programs that use
the Mozilla toolkit to various levels of success.  I've tried to compile
Thunderbird, Songbird and Instantbird at various points.  I got
Thunderbird to compile, but it only worked sporadically (although I
think that was Firefox moving so fast that Thunderbird couldn't keep
up), Songbird I gave up on rather quickly and Instantbird I've tried a
few times.

Last summer I had Instantbird compiling on my old laptop (a Lenovo
T60), which is >5 years old at this point and has had the heatsink / fan
replaced twice -- a known issue with that model laptop.  Needless to
say, that laptop didn't like compiling something on Windows that took
approximately an hour with a large number of reads and writes to the
hard drive.  This mixed with it being an old dual core + a 5400 RPM
meant I'd be waiting a LONG time for my code to compile.  I got a
Thinkpad X201 this past summer, so I finally got around to setting up a
development environment on it and was able to get Instantbird to compile
fully today.  I've outlined the steps I've followed: kind of to mirror
the `Simple Thunderbird Build`_ page on MDC.

I've done this using Microsoft Windows 7 Professional (64-bit) with
Service Pack 1. (4.00 GB of RAM, Intel Core i7 M620 2.67 GHz). 
Throughout these steps, the defaults locations and options are used in
the installers.

Build Requirements:
===================

Visual Studio Express:
----------------------

We need to install Visual Studio Express, specifically VC8 (2005) with
Service Pack 1.  (Mozilla compiles with VC9 and VC10 to various degrees,
but it seems libpurple only compiles with VC8, also this is what's on
the Instantbird buildbot, so I like having the same version.)  I
couldn't find this on Microsoft's website but I found it on `Softpedia`_
(which is a legitimate site).  Anyway, download the installer and
install it (which will download the actual compiler from Microsoft),
ensure that you also install the IDE (which is checked by default).

This will only install VC8, the initial release.  We also need to
install `Service Pack 1`_.  I personally did this using Windows Update,
but one of the installers from there should also work.

Microsoft Windows SDK:
----------------------

Specifically we need the `Windows 7 SDK`_ (for Jumplist, Aero, etc.
support).  Download and install the SDK, this one took a while for me to
install.  I ate dinner while it was installing (pasta, if you're curious
-- I already had sauce made).

There's a linker error when using VC8 and the Windows 7 SDK, so we'll
need to install a `hotfix`_\ for that (I tried without it and I ran into
the issue).  I had to download the "VS80sp1-KB949009-IA64-INTL.exe"
version (there's also an X86 and an X64 version).  Choose the one that
works.

Microsoft Macro Assembler:
--------------------------

In order to properly assemble the code we need to `install MASM`_
(which I think will eventually be included in MozillaBuild, but it isn't
currently).  Again, just install it with the defaults.

MozillaBuild:
-------------

Almost there, I promise.  In order to get a \*nix type shell to run
make, etc. in we'll use a package from Mozilla that includes MSYS, make,
Mercurial, etc.  Download and `install MozillaBuild`_, the latest should
work fine.

Now, an unknown step: you might require the `Microsoft Visual C++ 2008
SP1 Redistributable Package`_.  I don't know if you need this or not
since I *already* had it, most likely from a previous program I've
installed.

We should be ready to build now pretty much.  For some more
information for this stuff you can check out the Mozilla Developer
Network pages I used to get this information: `Build Instructions`_,
`Windows Build Prerequisites`_ and `MSVC8 Build Instructions`_.

Checkout the Code:
==================

We need to checkout the code.  I originally checked out the code with
TortoiseHg (which is what I normally use), but the version of Mercurial
included is significantly greater than the one included in MozillaBuild
and this caused me issues later on.  Thus, we'll check out the code on
the command line.  Start by launching the bash shell, which is at
C:\\mozilla-build\\start-msvc8.bat (don't use the x64 version).  There's
a version here which corresponds to each version of VS.

Once this finishes loading you'll be in the home directory (which is
in the root of your user's documents and settings folder, i.e. for me:
C:\\Users\\clokep).  You'll want to do the following: ::

    hg clone https://hg.instantbird.org/instantbird

This might take a few minutes depending on how good your internet
connection is.  (The Instantbird source isn't THAT big though, it
shouldn't take too long.)

Then we'll need to change into the instantbird directory that was just
created and download the Mozilla source code: ::

    cd instantbird
    python client.py checkout

Now this step?  This one is gonna take a while.  It took me like a
couple of hours.  It pulls the Mozilla source code, which is large and
has many changesets.  Just let it go, it'll give you progress
occasionally (changes, manifests, files, etc.)

Compiling Instantbird:
======================

We need to set up the options we want to build with.  These are
read from a .mozconfig (don't miss the "." in the front!).  The contents
of the .mozconfig that worked for me are: ::

    ac_add_options --enable-application=instantbird
    mk_add_options MOZ_OBJDIR=@TOPSRCDIR@/objdir-ib-release
    ac_add_options --disable-accessibility

The first option says to build Instantbird, the second gives an output
directory and the third `disables accessibility`_ (not really sure why
we need to do this, but we'll get that error at that link otherwise).

Finally (back in the bash shell) type: ::

    make -f client.mk build

Now sit back and relax.  My build took about an hour to finish, maybe
a bit less -- I wasn't fully paying attention.  Once it's done you
should see something like: ::

    Processed 1 file, writing output:

    Output:
    "c:\\Users\\clokep\\instantbird\\objdir-ib-release\\instantbird\\installer\\windows\\instgen\\helper.exe"
    Install: 2 pages (128 bytes), 1 section (16416 bytes), 2579
    instructions (72212 bytes), 369 strings (10198 bytes), 1 language table (230 bytes).
    Uninstall: 5 pages (320 bytes),
    1 section (16416 bytes), 2063 instructions (57764 bytes), 388 strings
    (10828 bytes), 1 language table (314 bytes).
    Datablock optimizer saved 123940 bytes (~17.6%).
    Using zlib compression.
    EXE header size:               63488 / 39424 bytes
    Install code:                  99564 / 99560 bytes
    Install data:                 118002 / 241950 bytes
    Uninstall code+data:          398654 / 398646 bytes
    CRC (0x062AF3F5):                  4 / 4 bytes
    Total size:                   679712 / 779584 bytes (87.1%)
    c:/Users/clokep/instantbird/objdir-ib-release/mozilla/config/nsinstall.exe -D ../../../mozilla/dist/bin/uninstall
    cp instgen/helper.exe ../../../mozilla/dist/bin/uninstall
    make[5]: Leaving directory `/c/Users/clokep/instantbird/objdir-ib-release/instantbird/installer/windows'
    make[4]: Leaving directory `/c/Users/clokep/instantbird/objdir-ib-release/instantbird'
    make[3]: Leaving directory `/c/Users/clokep/instantbird/objdir-ib-release'
    make[2]: Leaving directory `/c/Users/clokep/instantbird/objdir-ib-release'
    make[1]: Leaving directory `/c/Users/clokep/instantbird/objdir-ib-release'

Now, to test that the build actually worked we can browse to the
compiled executable and run it: ::

    cd objdir-ib-release/mozilla/dist/bin/instantbird.exe -P dev -no-remote

The -P option specifies a profile name (dev), the second option
(-no-remote) allows you to run a second Instantbird instance (since I
assume you use Instantbird to IM...you probably want to be able to run a
second one, if you don't use it...shame on you. Try not to close the
wrong Instantbird when you're working on stuff).

Hopefully this will help someone else get started on hacking
Instantbird.  There's other good ways you can hack too if your computer
can't handle compiling, including unpacking omni.jar.

One last tidbit is to possibly add the option to your .mozconfig: ::

    --enable-chrome-format=flat

This will not package anything in JARs (which pretty much just get in
the way while developing).  See \ `here`_ for more info.

Edit: Fixed the path to the executable thanks to Florian. And fixed a
spelling error in the title.

.. _Simple Thunderbird Build: https://developer.mozilla.org/En/Simple_Thunderbird_build
.. _Softpedia: http://www.softpedia.com/get/Programming/Other-Programming-Files/Microsoft-Visual-C-Toolkit.shtml
.. _Service Pack 1: http://www.microsoft.com/downloads/en/details.aspx?FamilyID=7b0b0339-613a-46e6-ab4d-080d4d4a8c4e
.. _Windows 7 SDK: http://www.microsoft.com/downloads/en/details.aspx?FamilyID=c17ba869-9671-4330-a63e-1fd44e0e2505&displaylang=en
.. _hotfix: http://support.microsoft.com/kb/949009/
.. _install MASM: http://www.microsoft.com/downloads/en/details.aspx?familyid=7A1C9DA0-0510-44A2-B042-7EF370530C64&displaylang=en
.. _install MozillaBuild: http://ftp.mozilla.org/pub/mozilla.org/mozilla/libraries/win32/MozillaBuildSetup-Latest.exe
.. _Microsoft Visual C++ 2008 SP1 Redistributable Package: http://www.microsoft.com/downloads/en/details.aspx?FamilyID=a5c84275-3b97-4ab7-a40d-3802b2af5fc2&displaylang=en
.. _Build Instructions: https://developer.mozilla.org/En/Developer_Guide/Build_Instructions
.. _Windows Build Prerequisites: https://developer.mozilla.org/En/Developer_Guide/Build_Instructions/Windows_Prerequisites
.. _MSVC8 Build Instructions: https://developer.mozilla.org/cn/VC8_Build_Instructions
.. _disables accessibility: https://developer.mozilla.org/en/atlbase.h
.. _here: https://developer.mozilla.org/en/JAR_Packaging
