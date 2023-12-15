Matrix Intentional Mentions explained
#####################################
:date: 2023-12-15 15:41
:author: Patrick Cloke
:tags: matrix, notes

Previously I have written about how `push rules generate notifications`_ and how
`read receipts mark notificiations as read`_ in the Matrix protocol. This article
is about a change that I instigated to improve *when* a "mention" (or "ping")
notification is created. (This is a "highlight" notification in the Matrix
specification.)

This was part of the work I did at Element to reduce `unintentional pings`_. I
preferred thinking of it in the positive -- that we should only generate a mention
on purpose, hence "intentional" mentions. :msc:`3952` details the technical protocol
changes, but this serves as a bit of a higher-level overview (some of this content
is copied from the MSC).

.. note::

  This blog post assumes that default push rules are enabled, these can be heavily
  modified, disabled, etc. but that is ignored in this post.

Legacy mentions
===============

The legacy mention system searches for the current user's display name or the
localpart of the Matrix ID [#]_ in the text content of an event. For example, an
event like the following would generate a mention for me:

.. code-block:: javascript

  {
    // Additional fields ignored.
    "content": {
      "body": "Hello @clokep:matrix.org!"
    }
  }

A ``body`` content field [#]_ containing ``clokep`` or ``Patrick Cloke``
would cause a "highlight" notification (displayed as red in Element). This isn't uncommon
in chat protocols and is how IRC and XMPP.

Some of the issues with this are:

* Replying to a message will re-issue pings from the initial message due to
  `fallback replies`_.
* Each time a message is edited the new version will be re-evaluated for mentions.
* Mentions occurring `in spoiler contents`_ or `code blocks`_ are evaluated.
* If the `localpart of your Matrix ID is a common word`_ then spurious notifications
  might occur (e.g. Travis CI matching if your Matrix ID is ``@travis:example.org``).
* If the `localpart or display name of your Matrix ID matches the hostname`_
  (e.g. ``@example:example.org`` receives notifications whenever ``@foo:example.org``
  is replied to).

There were some `prior attempts`_ to fix this, but I would summarize them as attempting
to reduce edge-cases instead of attempting to rethink how mentions are done.

Intentional mentions
====================

I chose to call this "intentional" mentions since the protocol now requires
explicitly referring to the Matrix IDs to mention in a dedicated field, instead
of implicit references in the text content.

The overall change is simple: include a list of mentioned users in a new
content field, e.g.:

.. code-block:: javascript

  {
    // Additional fields ignored.
    "content": {
      "body": "Hello @clokep:matrix.org!"
      "m.mentions": {
        "user_ids": ["@clokep:matrix.org"]
      }
    }
  }

Only the ``m.mentions`` field is used to generate mentions, the ``body`` field is
no longer involved. Not only does this remove a whole class of potential bugs,
but also allows for "hidden" mentions and paves the way for mentions in extensible
events (see :msc:`4053`).

That's the gist of the change, although the MSC goes deeper into backwards
compatibility, and interacting with replies or edits.

Comparison to other protocols
=============================

The ``m.mentions`` field is similar to how `Twitter`_, `Mastodon`_, `Discord`_,
and `Microsoft Teams`_ handle mentioning users. The main downside of this approach
is that it is not obvious *where* in the text the user's mention is (and allows
for hidden mentions).

The other seriously considered approach was searching for "pills" in the HTML
content of the event. This is similar to how `Slack`_ handles mentions, where the
user ID is encoded with some markup [#]_. This has a major downside of requiring HTML
parsing on a hotpath of processing notifications (and it is unclear how this would
work for non-HTML clients).

Can I use this?
===============

You can! The MSC was approved and `included in Matrix 1.7`_, Synapase has had
support since v1.86.0; it is pretty much up to clients to implement it!

Element Web has handled (and sent intentional mentions) since v1.11.37, although
I'm not aware of other clients which do (Element X might now). Hopefully it will
become used throughout the ecosystem since many of the above issues are still
common complaints I see with Matrix.

.. [#] This post ignores room-mentions, but they're handled very similarly.

.. [#] Note that the plaintext content of the event is searched *not* the "formatted"
       content (which is `usually HTML`_).

.. [#] This solution should also reduce the number of unintentional mentions, but
       doesn't allow for hidden mentions.

.. _push rules generate notifications: {filename}/articles/matrix-push-rules-and-notifications.rst
.. _read receipts mark notificiations as read: {filename}/articles/matrix-read-receipts-and-notifications.md
.. _unintentional pings: https://github.com/vector-im/element-meta/issues/886
.. _fallback replies: https://spec.matrix.org/v1.5/client-server-api/#fallbacks-for-rich-replies
.. _in spoiler contents: https://github.com/matrix-org/matrix-spec/issues/16
.. _code blocks: https://github.com/matrix-org/matrix-spec/issues/15
.. _localpart of your Matrix ID is a common word: https://github.com/matrix-org/matrix-spec-proposals/issues/3011
.. _localpart or display name of your Matrix ID matches the hostname: https://github.com/matrix-org/matrix-spec-proposals/issues/2735
.. _prior attempts: https://github.com/matrix-org/matrix-spec-proposals/blob/main/proposals/3952-intentional-mentions.md#prior-proposals

.. _Slack: https://api.slack.com/reference/surfaces/formatting#mentioning-users
.. _Twitter: https://developer.twitter.com/en/docs/twitter-api/data-dictionary/object-model/tweet
.. _Mastodon: https://docs.joinmastodon.org/entities/Status/#Mention
.. _Discord: https://discord.com/developers/docs/resources/channel#message-object
.. _Microsoft Teams: https://learn.microsoft.com/en-us/graph/api/resources/chatmessagemention?view=graph-rest-1.0

.. _included in Matrix 1.7: https://spec.matrix.org/v1.9/client-server-api/#user-and-room-mentions

.. _usually HTML: https://spec.matrix.org/v1.9/client-server-api/#mroommessage-msgtypes