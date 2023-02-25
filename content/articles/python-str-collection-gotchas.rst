Python ``str`` Collection Gotchas
#################################
:date: 2023-02-24 19:42
:author: Patrick Cloke
:tags: python

We have been slowly adding Python type hints [#]_ to `Synapse`_ and have made
great progress (see `some of our motivation`_). Through this process we have
learned a lot about Python and type hints. One bit that was unexpected is that
many of the `abstract base classes`_ representing groups of ``str`` instances
also match an individual ``str`` instance. This has resulted in more than one
*real* bug for us [#]_: a function which has parameter of type ``Collection[str]``
was called with a ``str``, for example [#]_:

.. code-block:: python

  def send(event: Event, destinations: Collection[str]) -> None:
      """Send an event to a set of destinations."""
      for destination in destinations:
          # Do some HTTP.
          ...

  def create_event(sender: str, content: str, room: Room) -> None:
      """Create & send an event."""
      event = Event(sender, content)
      send(event, "matrix.org")

The correct version should call ``send`` with a ``list`` of destinations instead
of a single one. The "s" at the end of "destinations" takes on quite a bit of
importance! See the fix:

.. code-block:: diff

  @@ -7,5 +7,5 @@
     def create_event(sender: str, content: str, room: Room) -> None:
         """Create & send an event."""
         event = Event(sender, content)
  -      send(event, "matrix.org")
  +      send(event, ["matrix.org"])

A possible solution is redefine the ``destinations`` parameter as a ``List[str]``,
but this forces the caller to convert a ``set`` or ``tuple`` to a ``list``
(meaning iterating, allocate memory, etc.) or maybe using a ``cast(...)`` (and
thus losing some of the protections from type hints). As a team we have a desire
to keep the type hints of function parameters as broad as possible.

Put another way, ``str`` is an instance of ``Collection[str]``, ``Container[str]``,
``Iterable[str]``, and ``Sequence[str]``. [#]_ [#]_

Since our type hints are only used internally we do not need to worry too much
about accepting exotic types and eventually came up with |StrCollection|_:

.. code-block:: python

  # Collection[str] that does not include str itself; str being a Sequence[str]
  # is very misleading and results in bugs.
  StrCollection = Union[Tuple[str, ...], List[str], AbstractSet[str]]

This covers lists, tuples, sets, and frozen sets of ``str``, the one case it does
not seem to cover well is if you are using a dictionary as an ``Iterable[str]``,
the easy workaround there is to call ``keys()`` on it to explicitly convert to a
|KeysView|_, which inherits from ``Set``.

.. [#] Looking at the `commits`_ to ``mypy.ini`` is probably the best way to see progress.

.. [#] `matrix-org/synapse#14809`_ is our tracking issue for fixing this, although
       `matrix-org/synapse#14880`_ shows a concrete bug fix which occurred.

.. [#] This is heavily simplified, but hopefully illustrates the bug!

.. [#] And ``Reversible[str]``, but I don't think I have ever seen that used and
       I think it less likely to introduce a bug.

.. [#] ``bytes`` doesn't have quite the same issue, but it might be surprising
       that ``bytes`` is an instance of ``Collection[int]``, ``Container[int]``,
       ``Iterable[int]``, and ``Sequence[int]``. I find this less likely to
       introduce a bug.

.. _Synapse: https://github.com/matrix-org/synapse
.. _some of our motivation: https://matrix.org/blog/2021/12/03/type-coverage-for-sydent-motivation
.. _abstract base classes: https://docs.python.org/3/library/collections.abc.html#collections-abstract-base-classes
.. |StrCollection| replace:: ``StrCollection``
.. _StrCollection: https://github.com/matrix-org/synapse/blob/335f52d595c2c32e4b512b97e2851bc98b819ca7/synapse/types/__init__.py#L84-L86
.. |KeysView| replace:: ``KeysView``
.. _KeysView: https://docs.python.org/3/library/collections.abc.html#collections.abc.KeysView

.. _commits: https://github.com/matrix-org/synapse/commits/develop/mypy.ini
.. _matrix-org/synapse#14809: https://github.com/matrix-org/synapse/issues/14809
.. _matrix-org/synapse#14880: https://github.com/matrix-org/synapse/pull/14880/files#diff-0b449f6f95672437cf04f0b5512572b4a6a729d2759c438b7c206ea249619885R1161
