Yahoo & Thunderbird Can Finally Play Nice?
##########################################
:date: 2010-11-22 23:03
:author: Patrick Cloke
:tags: email, Mozilla, programming, Thunderbird, Yahoo
:slug: yahoo-thunderbird

For years I've been dealing with Yahoo's lack of support for any sort
of decent (free) POP3/IMAP/SMTP protocol support. Why do I need this?
So I can check my `Yahoo mail`_ in `Mozilla Thunderbird`_ of course!

At first I used `YPOPS!`_, a program that read the HTML pages provided
by the Yahoo webmail client and served the emails on a local POP
server. Cool, right? Except it always broke whenever Yahoo changed
their pages around.

After a bit I moved onto using the `WebMail extension`_ for
Thunderbird. It essentially works the same way, but runs in the
Thunderbird process as an extension instead of as a separate service.
It's a little complicated to set up and requires two extensions. The
general WebMail extension and a Yahoo specific one (there's also ones
available for Hotmail, Gmail, Libero and AOL). You might wonder why
this exists for some services that have always had POP/IMAP access
(Gmail)? I was too, apparently some people cannot check those ports
because of firewall issues so this essentially allows them to check it
via port 80, over an HTTP connection.

A few months ago I came across `post`_ describing how a `simple
(nonstandard) command`_ could allow access to the Yahoo IMAP server, but
it required `patching the Thunderbird source`_ -- not an option for me
since I've been running nightlies of either Thunderbird 3.1 or 3.2/3.3
for a while now. (I mean sure, I could do it...but WebMail extension was
working fine.) There was `some discussion`_ about it and a `bug`_ was
filed for Thunderbird.

So how did this lead to free IMAP support? I noticed in the `Weekly
Status Meeting Notes (2010-11-16)`_ for Thunderbird a mention of `Free
Email Providers`_ page. Checking it out it said "Y! Mail is a free
email service provided by Yahoo! It offers webmail supported by targeted
advertising as well as IMAP access." Hmm...but I just said they don't
have support this for free! A quick Bing search brought up a `page with
IMAP server settings`_. I figured I'd check if they work, and sure
enough they did! The settings are copied below:

    :User name: :strike:`user@yahoo.com` user
    :IMAP server: :strike:`imap-ssl.mail.yahoo.com` imap.mail.yahoo.com
    :Port: 993
    :Password: Cleartext/Normal
    :SSL: yes
    :SMTP server: smtp.mail.yahoo.com
    :Port: 465
    :Password: Cleartext/Normal
    :SSL: yes

Awesome! Anyway, I replied with this info in the aforementioned bug
and `a patch`_ was quickly added by Mozilla's `Ben Bucksch`_ to support
this in Thunderbird, hopefully it'll make it into the next version! It
was also brought to my attention that imap-ssl.mail.yahoo.com provides
an SSL certificate that is valid for imap.mail.yahoo.com only, I'd
suggest using that former.

Note that I'm currently suffering from `another bug`_ while using
Yahoo IMAP. Everything works, there's just an annoying pop-up
occasionally about the error. Hopefully it will be fixed soon.

.. _Yahoo mail: http://mail.yahoo.com/
.. _Mozilla Thunderbird: http://www.mozillamessaging.com/en-US/thunderbird/
.. _YPOPS!: http://ypopsemail.com/
.. _WebMail extension: http://www.blogger.com/
.. _post: http://www.emaildiscussions.com/showthread.php?t=59575
.. _simple (nonstandard) command: http://en.wikipedia.org/w/index.php?title=Yahoo%21_Mail&oldid=396914770#Free_IMAP_and_SMTPs_access
.. _patching the Thunderbird source: http://www.crasseux.com/linux/
.. _some discussion: http://groups.google.com/group/mozilla.dev.apps.thunderbird/browse_thread/thread/546356554c73f8ca
.. _bug: https://bugzilla.mozilla.org/show_bug.cgi?id=493064
.. _Weekly Status Meeting Notes (2010-11-16): https://wiki.mozilla.org/Thunderbird/StatusMeetings/2010-11-16#Web_Update
.. _Free Email Providers: http://trunk.mozillamessaging.com/en-US/thunderbird/features/email_providers.html
.. _page with IMAP server settings: http://www.theanimail.com/imap_server_settings.html
.. _a patch: https://bugzilla.mozilla.org/attachment.cgi?id=492550&action=diff
.. _Ben Bucksch: http://www.bucksch.org/1/projects/mozilla/
.. _another bug: https://bugzilla.mozilla.org/show_bug.cgi?id=610264
