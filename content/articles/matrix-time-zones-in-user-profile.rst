Matrix: Time Zones in User Profiles
###################################
:date: 2025-11-15 12:55
:author: Patrick Cloke
:tags: matrix

Matrix had very limited user profile information, only: display name and an avatar. [#]_
Users are able to get/set these fields with a simple CRU\ :strike:`D` REST API.
This is pretty limiting and doesn't match what users expect from a modern chat platform.
In particular, I've seen many folks work around the lack of location and time zone support by adding it to their display name.

This is structured data and should be easy to store directly in a profile! How hard can it be? As an initial target, I decided to look at adding time zone information which resulted in :msc:`4175`.

Prior Attempts
==============

There was an old Matrix Spec Change proposal to store "profiles as rooms" (:msc:`1769` [#]_), a brief overview:

* Each user would have a room with a special name that represents the user's metadata (e.g. ``#@clokep:matrix.org``).
* Metadata would be stored in a single state event with a vCard data (represented using jCard from :rfc-reference:`7095`).
* It required "peeking" (:msc:`1776`) and "peeking over federation" (:msc:`1777`), which are both additional (large) MSCs.

A Simpler Solution
==================

Another Matrix community member (`Tom Foster`_) had written :msc:`4133` to expand the allowed operations to include for arbitrary fields, instead of limiting it to only display name and avatar [#]_. This was a simpler building block to target. A brief overview:

* Allow arbitrary profile keys to be created and updated. (Arbitrary profile fields already allowed to be fetched!)
* Allow for deleting profile fields (instead of just setting them to null/empty).
* Profile keys should be namespaced (reserving the `m.` prefix for fields in the Matrix specification).
* Defining how a server can declare what keys can be created.

That is pretty much the gist, although it took ~10 months, > 2400 words, > 50 commits, and hundreds of comments to agree on an approach.

Earlier versions included several other (controversial) features that were removed:

* User-defined profile fields (:msc:`4208`).
* Providing a `PATCH` for the entire profile (:msc:`4255` is related, but not exactly a replacement).

This MSC was missing an actual use-case, however, which :msc:`4175` provided for user time zones.

Server Implementation
---------------------

I worked with Tom to `implement the above in Synapse`_, it was a bit trickier than initially expected due to:

* Profile fields can hold arbitrary JSON (not just strings).
* Needing to track the total profile size and ensure it did not go over a limit (including the display name and avatar).
* Ensuring the behavior of display names and avatars did not change.
* JSON functionality between PostgreSQL and SQLite are similar, but not identical.
* Some trickiness with handling whether a field doesn't exist or is set to null.

The actual implementation is an extra ``JSONB`` column on the ``profiles`` table to store "additional" profile fields as a JSON blob (additional meaning not the display name or avatar, which are stored in discrete fields).

Several of the `PostgreSQL JSON functions`_ or `SQLite JSON functions`_ are used to update/fetch fields within the JSON blob and count the expected length to assert the profile is not too large.

The server itself doesn't need to know anything else about the fields being stored in the profile, and :msc:`4175` recommends that servers do _not_ verify the time zone provided, as they might have less accurate information than clients.

Client Implementation
---------------------

:msc:`4175` defines the standardized field name and format for the time zone profile field, which is simply the `IANA Time Zone Database Zone ID`_, e.g.:

.. code-block:: javascript

  {
    "m.tz": "America/New_York"
  }

Luckily a couple of other community members quickly implemented this for clients for `Element Web`_ an `gomuks`_. I was not too involved in either of these implementations besides bugging people to implement it!

Conclusion
==========

Clients are now free to implement and experiment with arbitrary profile fields! The time zone profile field is specified in `Matrix v1.16`_.

There are a few limitations with this approach which are yet to be solved:

1. Propagating profile changes across federation (between servers) is completely undefined right now. :msc:`4259` has some ideas, but is not yet implemented.
2. Time zone information must be fetched individually for each user, so there is no easy way to show at a glance who may be around in the room.

Lessons learned
===============

There was a lot of back and forth between Tom and I on the pieces of this specification (and the implementation), some of my takeaways include:

1. Keep an MSC as discrete and small as possible to avoid unnecessary bikeshedding.
2. It is OK to _not_ take into account someone's feedback (politely) if you disagree.
3. Including impact on trust & safety concerns upfront can help.
4. ``JSONB`` columns in PostgreSQL are super powerful.
5. Writing up the changes to the specification are often shorter than writing the MSC itself.
6. Getting a feature specified, merged, and implemented in Matrix can be time consuming and require many different people (but is possible)!

Thanks to `Tom Foster`_ for the bulk of the work of writing :msc:`4133` and `Half-Shot`_ for offering client guidance and the initial implementation of :msc:`4175`.

.. [#] Although these can be set on a per-room basis, which is handy!
.. [#] An updated version of :msc:`1769` was published as :msc:`4201`, but it is not dramatically different.
.. [#] Turns out this was pretty similar to :msc:`3793` which was never merged.

.. _Tom Foster: https://tomfos.tr/
.. _implement the above in Synapse: https://github.com/element-hq/synapse/pull/17488
.. _PostgreSQL JSON functions: https://www.postgresql.org/docs/12/functions-json.html
.. _SQLite JSON functions: https://www.sqlite.org/json1.html
.. _Element Web: https://github.com/element-hq/matrix-react-sdk/pull/20
.. _gomuks: https://github.com/gomuks/gomuks/pull/574
.. _IANA Time Zone Database Zone ID: https://www.iana.org/time-zones
.. _Matrix v1.16: https://spec.matrix.org/v1.16/client-server-api/#get_matrixclientv3profileuserid
.. _Half-Shot: https://half-shot.github.io/
