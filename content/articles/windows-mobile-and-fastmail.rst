Windows Mobile (or Windows Phone) and FastMail
##############################################
:date: 2016-07-24 13:19
:author: Patrick Cloke
:tags: email, contacts, calendar, FastMail, Windows Phone

.. contents::

I've been a big fan of Windows Phone (now Windows Mobile) for a while and have
had a few phones across versions 7, 8, and now 10. A while ago I switched to
FastMail_ as my e-mail provider [#]_, but had been stuck using Google as my
calendar provider still (and my contacts were on my Windows Live account). I had
a desire to move all these onto a single account, but Windows 10 Mobile only
officially supports e-mail from arbitrary providers. Calendar and contacts are
limited to a few special providers.

Below I've outlined how I've gotten all three services (email, contacts, and
calendar) from my FastMail account onto my Windows Mobile device.

Email
=====

Email is the easy one, FastMail even has a
`guide to setting up email on Windows Phone`_. This guide did not handle sending
emails with a custom domain name, if you don't have that situation, probably
just use the FastMail guide.

1.  Add a new account, choose "other account".
2.  Type in your email address (e.g. ``you@yourcustomdomain.com``) and password.
3.  It will complain about being unable to find proper account settings. Click
    "try again".
4.  It will complain again, but not give you an option for "advanced", click it.
5.  Choose "Internel email account".
6.  Enter any "Account name" and "Your name" that you want.
7.  Choose "IMAP4" as the "Account type".
8.  Change the incoming mail server to ``mail.messagingengine.com``.
9.  Change the username to your FastMail username (e.g. ``you@fastmail.com``).
10. Change the outgoing mailserver to ``mail.messagingengine.com``.

Now when you send email it should show up properly as
``you@yourcustomdomain.com``, but be sent via FastMail's servers!

Contacts
========

FastMail `added support for CardDAV last year`_ and Windows Phone
`added support back in 2013`_, so why is this hard? Well...turns out that there
isn't a way to make a CardDAV account on Windows Mobile, it's just used for
certain account types. Luckily, there is a `forum post`_ about hooking up
CardDAV via a hack. Steps are reproduced below:

1.  Add a new account, choose "iCloud".
2.  Type in your FastMail username, but add ``+Default`` before the ``@`` (e.g.
    ``you+Default@fastmail.com``), note that this isn't anything special, just
    the `scheme FastMail uses for CardDAV usernames`_.
3.  Put in your password. [#]_
4.  Click "sign in", it will fail.
5.  Go back into the account settings (click "Manage") and modify the advanced
    settings ("Change mailbox sync settings"). Choose manually for when to
    download new email. Disable syncing of email and calendar.
6.  Go to "Advanced account settings". Change the "Incoming email server",
    "Outgoing (SMTP) email server" and "Calendar server (CalDAV)" to
    ``localhost``. [#]_
7.  Change "Contacts server (CardDAV)" to
    ``carddav.messagingengine.com:443/dav/addressbooks/user/you@fastmail.com/Default``,
    changing ``you@fastmail.com`` to your FastMail username.
8.  Click "Done"!

Your contacts should eventually appear in your address book! I couldn't figure
out a way to force my phone to sync contacts, but they appeared fairly quickly.

Calendar
========

FastMail `added support for CalDAV`_ back in the beginning of 2014 [#]_. These
steps are almost identical to the `Contacts`_ section above, but using
information from the `guide for setting up Calendar.app`_.

1.  Add a new account, choose "iCloud".
2.  Type in your FastMail username (e.g. ``you@fastmail.com``).
3.  Put in your password.
4.  Click "sign in", it will fail.
5.  Go back into the account settings (click "Manage") and modify the advanced
    settings ("Change mailbox sync settings"). Choose manually for when to
    download new email. Disable syncing of email and contacts.
6.  Go to "Advanced account settings". Change the "Incoming email server",
    "Outgoing (SMTP) email server" and "Contacts server (CardDAV)" to
    ``localhost``.
7.  Change "Calendar server (CalDAV)" to
    ``caldav.messagingengine.com/dav/principals/user/you@fastmail.com/``,
    changing ``you@fastmail.com`` to your FastMail username.
8.  Click "Done"!

My default calendar appeared very quickly, but additional calendars took a bit
to sync onto my phone.

Good luck and let me know if there are any errors, easier ways, or other tricks
to getting the most of FastMail on a Windows Mobile device!

.. [#]  There are a variety of reasons why I switched, I had
        `recently bought a domain name`_ to get better control over my online
        presence (email, website, etc.). I was also tired of my email being used
        to server me advertisements and various other issues with free webmail.
        I highly recommend FastMail, they have awesome security_ and privacy_
        policies. They also have *amazing* support, give back to (a lot) to open
        source and a whole slew of other things.
.. [#]  I put a dummy one in and then changed it after I updated the servers in
        step 6. This was to not send my password to iCloud servers. The password
        is hopefully encrypted and hashed, but I don't know for sure.
.. [#]  We're just ensuring that our credentials for these other services will
        not hit Apple servers for any reason.
.. [#]  That article talks about beta.fastmail.fm, but this is now available on
        the production FastMail servers too!

.. _FastMail: https://www.fastmail.com/
.. _guide to setting up email on Windows Phone: https://www.fastmail.com/help/clients/winphone.html
.. _added support for CardDAV last year: https://blog.fastmail.com/2015/08/21/carddav-your-contacts-everywhere-you-need-them/
.. _added support back in 2013: https://blogs.windows.com/windowsexperience/2013/01/30/syncing-google-services-with-windows-phone/
.. _forum post: http://www.emaildiscussions.com/showthread.php?t=70967
.. _scheme FastMail uses for CardDAV usernames: https://www.fastmail.com/help/clients/iphone.html#contacts
.. _added support for CalDAV: https://blog.fastmail.com/2014/01/23/calendar-now-available-on-beta-fastmail-fm-for-testing/
.. _guide for setting up Calendar.app: https://www.fastmail.com/help/clients/maccalendar.html
.. _recently bought a domain name: {filename}/articles/new-blog.rst
.. _security: https://www.fastmail.com/help/ourservice/security.html
.. _privacy: https://www.fastmail.com/about/privacy.html
