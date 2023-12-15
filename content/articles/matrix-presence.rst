Matrix Presence
###############
:date: 2023-12-15 11:24
:author: Patrick Cloke
:tags: matrix, notes

I put together some notes on presence when implementing `multi-device support for presence`_
in Synapse, maybe this is helpful to others! This is a combination of information
from the specification, as well as some information about how Synapse works.

.. note::

    These notes are true as of the v1.9 of the Matrix spec and also cover some
    Matrix spec changes which may or may not have been merged since.

Presence in Matrix
==================

Matrix includes basic presence support, which is explained decently from `the specification`_:

  Each user has the concept of presence information. This encodes:

  * Whether the user is currently online
  * How recently the user was last active (as seen by the server)
  * Whether a given client considers the user to be currently idle
  * Arbitrary information about the user’s current status (e.g. “in a meeting”).

  This information is collated from both per-device (``online``, ``idle``, ``last_active``)
  and per-user (status) data, aggregated by the user’s homeserver and transmitted
  as an ``m.presence`` event. Presence events are sent to interested parties where
  users share a room membership.

  User’s presence state is represented by the presence key, which is an enum of
  one of the following:

  * ``online`` : The default state when the user is connected to an event stream.
  * ``unavailable`` : The user is not reachable at this time e.g. they are idle. [#]_
  * ``offline`` : The user is not connected to an event stream or is explicitly suppressing their profile information from being sent.

:msc:`3026` defines a ``busy`` presence state:

  the user is online and active but is performing an activity that would prevent
  them from giving their full attention to an external solicitation, i.e. the user
  is online and active but not available.

Presence information is returned to clients in the ``presence`` key of the
`sync response`_ as a ``m.presence`` EDU which contains:

* ``currently_active``: Whether the user is currently active (boolean)
* ``last_active_ago``: The last time since this used performed some action, in milliseconds.
* ``presence``: ``online``, ``unavailable``, or ``offline`` (or ``busy``)
* ``status_msg``: An optional description to accompany the presence.

Updating presence
-----------------

Clients can call |PUT /status|_ to update the presence state & status message or
can set the presence state via |set_presence /sync|_.

Note that when using the ``set_presence`` parameter, ``offline`` is equivalent to
"do not make a change".

User activity
-------------

From the `Matrix spec on last active ago`_:

  The server maintains a timestamp of the last time it saw a pro-active event from
  the user. A pro-active event may be sending a message to a room or changing presence
  state to ``online``. This timestamp is presented via a key called ``last_active_ago``
  which gives the relative number of milliseconds since the pro-active event.

If the presence is set to ``online`` then ``last_active_ago`` is not part of the
``/sync`` response and ``currently_active`` is returned instead.

Idle timeout
------------

From the `Matrix spec on automatically idling users`_:

  The server will automatically set a user’s presence to ``unavailable`` if their
  last active time was over a threshold value (e.g. 5 minutes). Clients can manually
  set a user’s presence to ``unavailable``. Any activity that bumps the last active
  time on any of the user’s clients will cause the server to automatically set their
  presence to ``online``.

:msc:`3026` also recommends:

  If a user's presence is set to ``busy``, it is strongly recommended for implementations
  to not implement a timer that would trigger an update to the ``unavailable`` state
  (like most implementations do when the user is in the ``online`` state).

Presence in Synapse
===================

.. note::

  This describes Synapse's behavior *after* v1.93.0. Before that version Synapse
  did not account for multiple devices, essentially meaning that the latest device
  update won.

  This also only applies to *local* users; per-device information for remote users
  is not available, only the combined per-user state.

User's devices can set a device's presence state and a user's status message.
A user's device knows better than the server whether they're online and should
send that state as part of ``/sync`` calls (e.g. sending ``online`` or ``unavailable``
or ``offline``).

Thus a device is only ever able to set the "minimum" presence state for the user.
Presence states are coalesced across devices as
``busy`` > ``online`` > ``unavailable`` > ``offline``. You can build simple
truth tables of how these combine with multiple devices:

+-----------------+-----------------+-----------------+
| Device 1        | Device 2        | User state      |
+=================+=================+=================+
| ``online``      | ``unavailable`` | ``online``      |
+-----------------+-----------------+-----------------+
| ``busy``        | ``online``      | ``busy``        |
+-----------------+-----------------+-----------------+
| ``unavailable`` | ``offline``     | ``unavailable`` |
+-----------------+-----------------+-----------------+

Additionally, users expect to see the latest activity time across all devices.
(And therefore if any device is online and the latest activity is recent then
the user is currently active).

The status message is global and setting it should always override any previous
state (and never be cleared automatically).

Automatic state transitions
---------------------------

.. note::

  Note that the below only describes the logic for *local* users. Data received
  over federation is handled  differently.

If a device is ``unavailable`` or ``offline`` it should transition to ``online``
if a "pro-active event" occurs. This includes sending a receipt or event, or syncing
without ``set_presence`` or ``set_presence=online``.

If a device is ``offline`` it should transition to ``unavailable`` if it is syncing
with ``set_presence=unavailable``.

If a device is ``online`` (either directly or implicitly via user actions) it should
transition to ``unavailable`` (idle) after a period of time [#]_ if the device is
continuing to sync. (Note that this implies the sync is occurring with
``set_presence=unavailable`` as otherwise the device is continuing to report as
``online``). [#]_

If a device is ``online`` or ``unavailable`` it should transition to  ``offline``
after a period of time if it is not syncing and not making other actions which
would transition the device to `online`. [#]_

Note if a device is ``busy`` it should not transition to other states. [#]_

There's a `huge testcase`_ which checks all these transitions.

Examples
''''''''

1. Two devices continually syncing, one ``online`` and one ``unavailable``. The
   end result should be `online`. [#]_
2. One device syncing with ``set_presence=unavailable`` but had a "pro-active"
   action, after a period of time the user should be ``unavailable`` if no additional
   "pro-active" actions occurred.
3. One device that stops syncing (and no other "pro-active" actions" are occurring),
   after a period of time the user should be ``offline``.
4. Two devices continually syncing, one ``online`` and one ``unavailable``. The
   ``online`` device stops syncing, after a period of time the user should be
   ``unavailable``.

.. [#] This should be called ``idle``.
.. [#] The period of time is implementation specific.
.. [#] Note that syncing with ``set_presence=offline`` does not transition to offline,
       it is equivalent to not syncing. (It is mostly for mobile applications to
       process push notifications.)
.. [#] The spec doesn't seem to ever say that devices can transition to offline.
.. [#] See the `open thread on the MSC3026`_.
.. [#] This is essentially the `bug illustrated by the change in Element Web's behavior`_.

.. _multi-device support for presence: https://github.com/matrix-org/synapse/pull/16066
.. _the specification: https://spec.matrix.org/v1.7/client-server-api/#presence
.. _sync response: https://spec.matrix.org/v1.7/client-server-api/#_matrixclientv3sync_presence
.. |PUT /status| replace:: ``PUT /_matrix/client/v3/presence/{userId}/status``
.. _PUT /status: https://spec.matrix.org/v1.8/client-server-api/#put_matrixclientv3presenceuseridstatus
.. |set_presence /sync| replace:: the ``set_presence`` parameter on ``/sync`` request
.. _set_presence /sync: https://spec.matrix.org/v1.8/client-server-api/#get_matrixclientv3sync
.. _Matrix spec on last active ago: https://spec.matrix.org/v1.7/client-server-api/#last-active-ago
.. _Matrix spec on automatically idling users: https://spec.matrix.org/v1.7/client-server-api/#idle-timeout
.. _huge testcase: https://github.com/matrix-org/synapse/blob/be65a8ec0195955c15fdb179c9158b187638e39a/tests/handlers/test_presence.py#L971-L1106

.. _open thread on the MSC3026: https://github.com/matrix-org/matrix-spec-proposals/pull/3026/files#r1287453423
.. _bug illustrated by the change in Element Web's behavior: https://github.com/matrix-org/synapse/issues/16057
