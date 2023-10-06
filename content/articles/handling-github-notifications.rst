Handling GitHub Notifications
#############################
:date: 2023-10-06 7:55
:author: Patrick Cloke
:tags: thunderbird

.. note::

  This was originally written for some coworkers and assumes a mostly GitHub-based
  workflow. It has been lightly edited to be more readable, but if your organization
  doesn't use GitHub like we do then it might not apply great.

`GitHub`_ can generate a lot of notifications which can be difficult to follow,
this documents some of my process for keeping up with it! For reference, I
subscribe to:

1. All notifications for the repositories I work in somewhat frequently;
2. Only releases and security alerts for repositories which might affect me (e.g.
   upstream repositories);
3. Other issues that might be related to the project I'm working on (e.g. bugs
   in upstream projects).

I also watch a bunch of open source projects and have some of my own projects.
(These are mostly Twisted or Celery related.)

I generally enjoy having some idea of "everything" going on in my team (in enough
detail to know what people are generally working on).

To avoid being overwhelmed by notifications I only subscribe to specific issues
for repositories from other teams or projects. These are usually:

* Things that personally annoy me (and I want to see fixed);
* Things that are directly related to or blocking my work;

For reference, I currently `watch 321 repositories`_, although most of my
notifications probably come from < 20 repositories. I also have 32 repositories
with custom notification rules -- those are set to only releases & Security alerts.
(And I have 1 muted repository.) [#]_

When / how
==========

I tend to do the following daily:

* Catch-up on notifications in the morning (takes ~15 - 45 minutes for GitHub,
  chat, e-mail, etc.).
* Check notifications a few times during the day (between meetings, after lunch,
  while tests runs, etc.).

Each time I check notifications I quickly triage each notification by skimming
the title to see if I'm interested (sometimes the title is enough info!). From
this I do one of several things:

* Open any issue in a separate tab to come back to if I need to read more (or
  potentially take action). I usually skim the update, leaving it open if I need
  to respond, closing the tab if I don't.
* "Mark as read" if I know it does not require anything from me:

  * A review someone else is handling (unless it is a bit of code I'm keen to
    understand, or know is tricky and feel some ownership over).
  * The title contains enough information I don't need to read the issue (e.g.
    a colleague following a follow-up issue).
  * Obvious support requests, unless I'm the maintainer. [#]_
  * Random MSCs / matrix-doc issues that I don't care about.
* **Unsubscribing** if I'm not interested in following the issue (e.g. an open
  source project is re-doing their CI). This was key for me watching other
  projects that I only somewhat care about.

I use both Thunderbird and the GitHub website (specifically the
`unread notifications view`_) to go through notifications. Note that the website
has quick buttons on the right which I use frequently: "Done" and "Unsubscribe"
(there is also "Save" -- which I do not use, I mark as unread if I need to come back).
It can also be useful to "Mark as done" an entire repository for projects I
follow out of vague interest, but don't have time to read at the moment.

"Open unread" is useful to get everything into separate tabs for later processing
(and to avoid waiting for GitHub to load). I usually use it when I have < 10
notifications left for a particular repository.

I usually attempt to go through notifications that I know I won't have to respond
to first, as they can be quickly processed and reduce the overwhelming number of
notifications.

Setup
=====

This workflow refers to using GitHub with `Mozilla Thunderbird`_ (via `Fastmail`_)
and `Mozilla Firefox`_, none of it is particular to those applications and can be
adapted to others.

GitHub
------

If you use GitHub for both work and other personal / open source projects it can
be helpful to route your work notifications to a separate email address. (This is
a good idea regardless for security & intellectual property concerns.)

Your default email can be configured on the `Notifications page`_ and
separation by organization can be configured on the `Custom routing page`_.
Under "Subscriptions" on the Notification page, I have both "Watching" and
"Participating, @mentions and custom" set to notify on both GitHub & email.

You may also want to tweak your "Customize email preferences". I have the
following enabled:

* "Pull Request reviews"
* "Comments on Issues and Pull Requests"
* "Include your own updates" -- this sounds weird, but you only need to lose a
  massive comment on GitHub once to want a copy of it in your inbox. (I
  automatically mark them as read, see below.)

I disable "Pull Request pushes" because I don't find it useful, although you will
still get these via the website.

Fastmail
--------

I have two mail rules setup in Fastmail to move all GitHub email to a separate
folder and to mark my own emails as read: [#]_

1. From: ``Patrick Cloke <notifications@github.com>``:
   1. Mark as read
   2. Move to "GitHub"
2. From email address: ``notifications@github.com``:
   1. Move to "GitHub"

Similar filters can be setup on other mail services, e.g. Google Mail:

1. Matches: ``from:(Patrick Cloke <notifications@github.com>)``
   1. Skip Inbox
   2. Mark as read
   3. Apply label: "GitHub"
2. Matches: ``from:(notifications@github.com)``
   1. Skip Inbox
   2. Apply label: "GitHub"

You can also check for `more ways to filter GitHub emails`_.

Mozilla Thunderbird
-------------------

For all of my folders I use threads (View > Sort By > Threaded) and only view
threads which have unread messages (View > Threads > Threads with Unread).

Other things that are useful:

* Enable "Automatically mark messages as read", but with a short delay (I have
  "After displaying for" set to 1 second).  (This lets you move through messages
  quickly using the keyboard or shortcuts without marking them all by mistake.)
* Add GitHub to the exceptions list in under "Allow remote content in messages"
  for either `notifications@github.com` or the `https://github.com`: this can
  be added when viewing an email from GitHub. (This will
  `mark the notification as read`_ the GitHub website automatically.)

I sort my threads by date, oldest first so I can just click the "n" hotkey to
move through messages quickly. I also use the message pane to have some context
on remaining unread messages per thread, but it should work fine without that.
If you decide you don't care about the rest of the thread "r" marks it as read.
Note that reading any messages in a thread will mark the entire issue or pull
request as done on the website. I find this extremely efficient for going through
a small number of notifications quickly.

I very much wish there was a way to sync back the read status of notifications from
GitHub back to Thunderbird. Lacking that I tend to mark the entire folder as read
(Shift+C) if I've caught up on the website. [#]_

Mozilla Firefox
---------------

I  use a few GitHub related extensions which can help:

* `Refined GitHub`_: includes lots of small tweaks to make GitHub "better".
* `GitHub Issue Link Status`_: colors the issue / PR links with whether it is
  open / closed / etc and marks it as an issue / PR.
* `Notifications Preview for GitHub`_: makes the notification button a dropdown
  for quick processing.
* `File Icons for GitHub and GitLab`_: adds file icons per file type for GitHub
* `Advanced GitHub Notifier`_: adds a Firefox toolbar button with easy access to
  your notifications (including a count of unread notifications)

Conclusion
==========

Hopefully some of this is helpful, please let me know if you have any questions
or thoughts!

.. [#] In August 2021 I was watching 263 repositories and had 18 repositories with
       custom notification settings.

.. [#] My team rotates through who is the first-line of contacts for incoming
       community requests, releases, etc.

.. [#] I have similar filters setup for `GitLab`_, `Sentry`_, etc.

.. [#] You could probably do this with an Thunderbird extension, but I've failed to
       find time to look into it.

.. _GitHub: https://github.com
.. _watch 321 repositories: https://github.com/watching
.. _unread notifications view: https://github.com/notifications?query=is%3Aunread
.. _Mozilla Thunderbird: https://www.thunderbird.net/
.. _Fastmail: https://www.fastmail.com/
.. _Mozilla Firefox: https://getfirefox.net
.. _Notifications page: https://github.com/settings/notifications
.. _Custom routing page: https://github.com/settings/notifications/custom_routing
.. _more ways to filter GitHub emails: https://docs.github.com/en/account-and-profile/managing-subscriptions-and-notifications-on-github/setting-up-notifications/configuring-notifications#filtering-email-notifications
.. _mark the notification as read: https://docs.github.com/en/account-and-profile/managing-subscriptions-and-notifications-on-github/setting-up-notifications/configuring-notifications#notification-delivery-options
.. _Refined GitHub: https://github.com/sindresorhus/refined-github/
.. _GitHub Issue Link Status: https://github.com/fregante/github-issue-link-status
.. _Notifications Preview for GitHub: https://github.com/tanmayrajani/notifications-preview-github
.. _File Icons for GitHub and GitLab: https://github.com/homerchen19/github-file-icons
.. _Advanced GitHub Notifier: https://github.com/freaktechnik/advanced-github-notifier

.. _GitLab: https://gitlab.com
.. _Sentry: https://sentry.io
