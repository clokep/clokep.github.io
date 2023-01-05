Title: Matrix Read Receipts & Notifications
Slug: matrix-read-receipts-and-notifications
Date: 2023-01-05 12:15
Tags: matrix, notes
Author: Patrick Cloke

I recently wrapped up a project on improving notifications in threads for Matrix.
This is adapted from my [research notes](https://hackmd.io/bbucQKOLTv66N4B_wjDLFQ)
to understand the status quo before adapting the Matrix protocol for threads
(in [MSC3771](https://github.com/matrix-org/matrix-spec-proposals/pull/3771) and
[MSC3773](https://github.com/matrix-org/matrix-spec-proposals/pull/3773)).
Hopefully others find the information useful!

!!! note
    These notes are true as of the v1.3 of the Matrix spec and also cover some
    Matrix spec changes which may or may not have been merged since. It is known
    to be out of date with the changes from [MSC2285](https://github.com/matrix-org/matrix-spec-proposals/pull/2285),
    [MSC3771](https://github.com/matrix-org/matrix-spec-proposals/pull/3771), and
    [MSC3773](https://github.com/matrix-org/matrix-spec-proposals/pull/3773).

----

## Receipts

Matrix uses "receipts" to note which part of a room has been read by a user.
It considers the history for a room to be split into three sections[^1]:

1. Messages the user has read (or indicated they aren’t interested in them).
2. Messages the user might have read some but not others.
3. Messages the user hasn’t seen yet.

The **fully read marker** is between 1 & 2 while the **read receipt** is between
2 & 3. Note that fully read markers are not shared with other users while read receipts are.

Another way to consider this is[^2]:

1. **Fully read marker**: a private bookmark to indicate the point which has been
   processed in the discussion. This allows a user to go back to it later.
2. **Read receipts**: public indicators of what a user has seen to inform other
   participants that the user has seen it.
3. **Hidden read receipts**: a private mechanism to synchronize "unread messages"
   indicators between a user's devices (while still retaining the ability from 1
   as a separate concept). (See [MSC2285](https://github.com/matrix-org/matrix-spec-proposals/pull/2285).)

### [Fully read markers](https://spec.matrix.org/v1.3/client-server-api/#fully-read-markers)

They are stored in the room account data for the user (but modified via a separate API).

The API is:

`POST /_matrix/client/v3/rooms/{roomId}/read_markers`

The read receipt can optionally be updated at the same time.

In Element Web your fully read marker is displayed as the green line across the
conversation.

### [Read receipts](https://spec.matrix.org/v1.3/client-server-api/#receipts)

Only `m.read` is defined at the moment, but it is meant to be generic infrastructure.

Updating a read receipt updates a "marker" which causes any notifications prior
to and including the event to be marked as read.[^3] A user has a single read receipt
"marker" per room.

Passed to clients as an `m.receipt` event under the `ephemeral` array for each
room in the `/sync` response. The event includes a map of event ID -> receipt type
-> user ID -> data (currently just a timestamp). Note that the event is a delta
from previous events. An example:

```json
{
  "content": {
    "$1435641916114394fHBLK:matrix.org": {
      "m.read": {
        "@rikj:jki.re": {
          "ts": 1436451550453
        }
      }
    }
  },
  "room_id": "!jEsUZKDJdhlrceRyVU:example.org",
  "type": "m.receipt"
}
```

The API is:

`POST /_matrix/client/v3/rooms/{roomId}/receipt/{receiptType}/{eventId}`

In Element Web read receipts are the small avatars on the right hand side of the
conversation. Note that your own read receipt is not shown.

### [Hidden read receipts (MSC2285)](https://github.com/matrix-org/matrix-spec-proposals/pull/2285)

A new receipt type (`m.read.hidden`) to set a read receipt without sharing it with
other users. It also modifies the `/read_markers` API to accept the new receipt type
and modifies the `/receipts` API to accept the fully read marker.

This is useful to synchronize notifications across devices while keeping read
status private.

## [Push rules](https://spec.matrix.org/v1.2/client-server-api/#push-rules)

A user's push rules determine one or more user-specific actions on each event.
They are customizable, but the homeserver provides default rules. They can result
in an action to:

1. Do nothing
2. Notify the user (`notify` action), which can have additional actions ("tweaks"):
    1. Highlight the message (`highlight` action)
    2. Play a sound (`sound` action)

By default, all new `m.room.message` and `m.room.encrypted` events generate a
notification, events with a user's display name or username in them or `@room`
generate highlights, etc.

### [Push rules for relations (MSC3664)](https://github.com/matrix-org/matrix-spec-proposals/pull/3664)

Augments push rules to allow applying them to the target of an event relationship
and defines a default push rule for replies (not using the reply fallback).

### [Event notification attributes and actions (MSC2785)](https://github.com/matrix-org/matrix-spec-proposals/pull/2785)

A proposed replacement for push rules, the results are essentially the same
actions (and presumedly would not change the data returned in `/sync`, see below).

## [Notification counts in `/sync`](https://spec.matrix.org/v1.3/client-server-api/#get_matrixclientv3sync)

The number of notification events and highlight events since the user's last read
receipt are both returned on a per room basis as part of a `/sync` response (for
joined room).

Notification and highlight events are any messages where the push rules resulted
in an action of `notify` or `highlight`, respectively. (Note that a `highlight`
action must be a `notify` action, thus `highlight_count <= notification_count`.)

An example:

```json
{
  "account_data": [...],
  "ephemeral": [...],
  "state": [...],
  "summary": {...},
  "timeline": {...},
  "unread_notifications": {
      "highlight_count": 0,
      "notification_count": 0
  }
}
```

### [Unread messages count (MSC2654)](https://github.com/matrix-org/matrix-spec-proposals/pull/2654)

A new field is added under the `unread_notifications` field (`unread_count`) which
is the total number of events matching particular criteria since the user's last
read receipt.

This replaces [MSC2625](https://github.com/matrix-org/matrix-spec-proposals/pull/2625),
which adds a new push rule action (`mark_unread`) to perform the same task. In this
rendition, `notify` implies `mark_unread` and thus
`highlight_count <= notification_count <= unread_count`.

## [Push notifications](https://spec.matrix.org/v1.2/push-gateway-api/#post_matrixpushv1notify)

Push notifications receive either the number of unread messages (across all rooms)
or the number of rooms with unread messages (depending on the value of
`push.group_unread_count_by_room` in the Synapse configuration). Unread messages
are any messages where the push rules resulted in an action of `notify`.

This information is sent from the homeserver to the push gateway as part of every
notification:

```json
{
  "notifications": {
    "counts": {
      "unread": 1,
      ...
    },
    ...
  }
}
```

[^1]: From [the fully read marker](https://spec.matrix.org/v1.3/client-server-api/#fully-read-markers) specification.
[^2]: See [a discussion on MSC2285](https://github.com/matrix-org/matrix-spec-proposals/pull/2285#discussion_r436383889).
[^3]: [Spec on receiving notifications](https://spec.matrix.org/v1.3/client-server-api/#receiving-notifications)
