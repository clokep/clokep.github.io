Matrix Push Rules & Notifications
#################################
:date: 2023-05-08 14:56
:author: Patrick Cloke
:tags: matrix

In a previous post about `read receipts & notifications in Matrix`_ I briefly
mentioned that push rules generate notifications, but with little detail. After
completing a rather large project to improve notifications in Matrix I want to
fill in some of those blanks. [#]_

.. comment:

  Adapted from https://docs.google.com/presentation/d/1odrbD5wMwGz_qUtG5U1pFb7p3sFwLApDaYtyHpdI-Oo/edit

.. contents::

.. note::

    These notes are true as of the v1.6 of the Matrix spec and also cover some
    Matrix spec changes which may or may not have been merged since.

Push notifications in Matrix
============================

Matrix includes a `push notifications module`_ which defines when Matrix events
are considered an unread **notification** or **highlight notification** [#]_
and *how* those events are **sent to third-party push notification services**.

**Push rules** are a set of *ordered* rules which clients upload to the homeserver.
These are shared by all device and are evaluated per event by the homeserver (and
also by clients). `Default push rules`_ are defined in the Matrix spec. Push rules
power the unread (and highlight) counts for each room, push notifications, and the
notifications API.

Each rule defines **conditions** which must be met for the rule to match and
**actions** to take if the rule matches.

Processing of push rules occur until a rule matches or all rules have been evaluated.

Getting notifications
---------------------

As some background, clients receive notifications in one of two ways, via polling
``/sync`` and/or via push notifications.

Web-based clients often receive events via polling:

.. center::

    .. image:: /thumbnails/matrix-push-rules-and-notifications/web-push-flow_medium.png
        :target: {static}/images/matrix-push-rules-and-notifications/web-push-flow.png
        :alt: Notification flow for web applications.

The `sync response`_ (both initial and incremental) include the count of unread
notifications and unread highlight notifications per room.

Mobile applications often `receive events via push`_ [#]_:

.. center::

    .. image:: /thumbnails/matrix-push-rules-and-notifications/mobile-push-flow_medium.png
        :target: {static}/images/matrix-push-rules-and-notifications/mobile-push-flow.png
        :alt: Notification flow for mobile applications.


Push notifications include the event information (or just the event ID) and
whether the event was a highlight notification. (The event being pushed implies
it increased the notification count.)

.. note::

    The deployment of the push gateway must be paired with the application (the
    push keys must be paired). I.e. if you make your own application (or even
    your own build of Element iOS / Android) you cannot re-use the deployment at
    matrix.org and must have your own deployment.


Getting events which generated notifications
--------------------------------------------

There’s `an API to retrieve a list of events`_ which the user has been notified
about. This powers the "notification panel" on Element Web and is meant to help
users catch-up on missed notifications.

It is fairly underspecified and the Synapse implementation has limitations:

* Highlight notifications are only kept for 30 days
* Non-highlight notifications are only kept for 72 hours

Additionally it `works poorly for encrypted rooms`_.

Push rules background
=====================

Getting the configured push rules?
----------------------------------

There’s a `set of APIs to fetch or modify push rules`_, they let you:

* Fetch all push rules
* Create or delete an individual push rule
* Fetch or update an individual push rule’s actions
* Fetch or enable/disable an individual push rule

An initial sync includes all of a user’s push rules under the user’s account data.

Any changes to push rules are included in incremental syncs. *Except* for newly
added rules to the specification (this is likely a homeserver bug).

Note that you cannot use `the account data APIs`_ to configure push rules. [#]_

What makes up a push rule?
--------------------------

A push rule is a `JSON object with the following fields`_:

* ``rule_id``: Unique (per-user) ID for the rule.

  * The ``rule_id`` for default rules have a special form (they start with a
    dot: ``.``).
* ``default``: Whether the rule is part of the predefined set of rules.
* ``enabled``: Whether the rule is enabled.
* ``conditions``: an array of 0 or more conditions to match.
* ``actions``: 0 or more actions to take if the rule matches.

All conditions must match for a push rule to match. If there are no conditions,
then the push rule always matches. Possible conditions include:

* Check event properties against patterns or exact values

  * Strings can be compared via globbing or exact values.
  * The globbing behavior changes if you’re checking the ``body`` property or not.
* Check against the number of room members

  * Used to (incorrectly) check if a room is a direct message.
* Check if a user can `perform an action`_ via power rules

  * The only defined option is whether a user can send @room.

Push rule actions define `what to do once a push rule`_ matches an event.

* ``notify``: increment the notification count and send a push notification. Uses
  "tweaks" to optionally:

  * Play a sound.
  * Create a highlight notification, this causes the highlight count to be
    incremented (in addition to the notification count).
* Can be an empty list to do nothing.

There are other undefined or no-op actions (``dont_notify``, ``coalesce``) which will be
removed in the next version of the spec. [#]_

Types of push rules
-------------------

Push rules have a type associated with them, these are executed in order:

* Override: generic high priority rules
* Content-specific: applies to messages which have a ``body`` that matches a ``pattern``
* Room-specific: applies to messages of a room
* Sender-specific: applies to messages from a sender
* Underride: generic low priority rules

The previously discussed shape of push rules is not the full story! There are
special cases which do not accept conditions, but can be mapped to them.

* Content-specific: has a ``pattern`` field which maps to a pattern against the
  ``body`` property.
* Room-specific: the ``rule_id`` is re-used to match against the room ID.
* Sender-specific: the ``rule_id`` is re-used to match against the event ``sender``.

Why do clients care? Doesn’t the homeserver do this all for me?
===============================================================

Encryption ruins everything! Some of the push rules require the decrypted event
content to be properly processed. The enable this, the default rules declare
**all encrypted events as notifications**. Clients are expected to
**re-run push rules on the decrypted content**. [#]_

This can result in one of the following: [#]_

* Increment the highlight count (the decrypted event results in a highlight)
* No change (the decrypted event results in a notification)
* Decrement notification counts (the decrypted event results in no notification)

Due to gappy syncs clients frequently can only make a best estimate of the true
unread / highlight count of events in encrypted rooms.

.. warning::

  Element iOS / Android get encrypted events pushed to them, but do not properly
  implement mentions & keywords.

What happens by default?
========================

The `default rules are in the Matrix spec`_ and include:

* Highlight:

  * Tombstones
  * Room & user mentions
* Do nothing:

  * Notice messages
  * Other room member events
  * Server ACL updates
* Notification:

  * Invites to me
  * Messages and encrypted events in non-DMs
* Notification with sound:

  * Incoming calls
  * Messages and encrypted events in DMs

Default rules can be disabled or have their actions modified on a per-user basis.
Some of the above features are handled by multiple push rules.

Other "standard" rules
----------------------

Element creates custom push rules based on a known form. [#]_

* Keywords (implemented as a content-specific rule with a pattern)
* Per-room overrides:

  * All messages (implemented as a room-specific rule with a notify action)
  * Mentions & keywords (implemented as a room-specific rule with no actions)
  * Mute (implemented as an override rule to match the room ID with no actions)

Matrix also allows defining arbitrary rules (e.g. to change behavior for particular
rooms, senders, message types, etc.)

What about unread rooms?
------------------------

The unread ("bold") rooms logic in Element Web is completely custom and outside
of the Matrix specification.

* Will the `event be shown`_ ?
* Is it `not an ignored event type`_ ?
* Is it `not redacted`_ ?
* Does a `renderer exist for the event`_ ?

Note that if you enable hidden events (or tweak other options to show events)
then the behavior changes!

Putting it altogether...
========================

...it gets complicated trying to figure out whether a message will generate a
notification or not.

.. center::

    .. image:: /thumbnails/matrix-push-rules-and-notifications/default-push-rules_medium.png
        :target: {static}/images/matrix-push-rules-and-notifications/default-push-rules.png
        :alt: Flow chart of the default Matrix push rules when using Element.

    The default Matrix push rules (also showing the options available within
    Element).

.. [#] Improving unintentional mentions (:msc:`3952`) is the main feature we were
       working on, but this was powered by ...

.. [#] Notification count (the grey badge with count in Element Web) is the number
       of unread messages in a room. Highlight count (the red badge with count in
       Element Web) is the number of unread mentions in a room.

       .. warning::

         The unread ("bold") rooms feature in Element Web, which represents a room
         with unread messages (but no notification count) is not powered by push
         rules (and is not specced).

       See the `Element Web docs on the room list`_.

.. [#] This post generally defines "push notifications" as a notification which
       is sent via a push provider to an application. Push providers include Apple,
       Google, Microsoft, or Mozilla.

.. [#] :msc:`4010` aims to make this explicit.

.. [#] See :msc:`3987`.

.. [#] It was not clear how clients should handle encrypted events `until recently`_

.. [#] Adapted from a `Gist from Half-Shot`_.

.. [#] These don't seem to be specced, I'm unsure if other clients create similar
       rules or understand these rules.

.. _read receipts & notifications in Matrix: {filename}/articles/matrix-read-receipts-and-notifications.md
.. _push notifications module: https://spec.matrix.org/v1.6/client-server-api/#push-notifications
.. _Default push rules: https://spec.matrix.org/v1.6/client-server-api/#predefined-rules
.. _sync response: https://spec.matrix.org/v1.6/client-server-api/#_matrixclientv3sync_unread-notification-counts
.. _receive events via push: https://spec.matrix.org/v1.6/push-gateway-api/#overview
.. _an API to retrieve a list of events: https://spec.matrix.org/v1.6/client-server-api/#listing-notifications
.. _works poorly for encrypted rooms: https://github.com/vector-im/element-web/issues/6874
.. _set of APIs to fetch or modify push rules: https://spec.matrix.org/v1.6/client-server-api/#push-rules-api
.. _the account data APIs: https://spec.matrix.org/v1.6/client-server-api/#client-config
.. _JSON object with the following fields: https://spec.matrix.org/v1.6/client-server-api/#_matrixclientv3pushrules_pushrule
.. _perform an action: https://spec.matrix.org/v1.6/client-server-api/#mroompower_levels
.. _what to do once a push rule: https://spec.matrix.org/v1.6/client-server-api/#actions
.. _default rules are in the Matrix spec: https://spec.matrix.org/v1.6/client-server-api/#predefined-rules
.. _event be shown: https://github.com/matrix-org/matrix-react-sdk/blob/d33e416fc75369d3fec1c1f27ef9d5b2ea0b3703/src/shouldHideEvent.ts#L58-L82
.. _not an ignored event type: https://github.com/matrix-org/matrix-react-sdk/blob/d33e416fc75369d3fec1c1f27ef9d5b2ea0b3703/src/Unread.ts#L41-L48
.. _not redacted: https://github.com/matrix-org/matrix-react-sdk/blob/d33e416fc75369d3fec1c1f27ef9d5b2ea0b3703/src/Unread.ts#L52
.. _renderer exist for the event: https://github.com/matrix-org/matrix-react-sdk/blob/d33e416fc75369d3fec1c1f27ef9d5b2ea0b3703/src/Unread.ts#L53

.. _Element Web docs on the room list: https://github.com/matrix-org/matrix-react-sdk/blob/develop/docs/room-list-store.md#list-ordering-algorithm-importance
.. _until recently: https://github.com/matrix-org/matrix-spec/pull/1461
.. _Gist from Half-Shot: https://gist.github.com/Half-Shot/f9501916363894761a1659250aa25181
