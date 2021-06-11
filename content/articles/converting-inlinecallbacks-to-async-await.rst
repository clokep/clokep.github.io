Converting Twisted's ``inlineCallbacks`` to ``async``
#####################################################
:date: 2021-06-11 15:11
:author: Patrick Cloke
:tags: twisted

.. contents::

Almost a year ago we had a push at Element to convert the remaining instances of
Twisted's |inlineCallbacks|_ to use native ``async``/``await`` syntax from Python [#]_.
Eventually this work got covered by `issue #7988`_ (which is the original basis
for this blogpost).

Note that Twisted itself `gained some support`_ for ``async`` functions in 16.4.

Why bother?
===========

``inlineCallbacks`` are very similar to ``async``/``await``, they use a generator
internally to wait for a task to complete and (modern [#]_) versions of Twisted let
you directly return values. There are some real benefits to switching though:

* ``inlineCallbacks`` mangle stack traces, while ``async``/``await`` does not
  (as much). This helps with profiling and understanding exceptions (e.g. in Sentry).
* ``async``/``await`` is more modern and standard -- there's a better chance of
  people understanding it who don't haven't used Twisted before.
* ``async``/``await`` has better support from other packages, static analyzers,
  tools, etc.
* ``async`` functions can provide better type hints for return values.
* We postulated that there might be a performance benefit, but were never able
  to measure any.

In fact the `Twisted documentation`_ (as of v21.2.0) even suggest some of the above:

    Unless your code supports Python 2 (and therefore needs compatibility with older
    versions of Twisted), writing coroutines with the functionality described in
    "Coroutines with async/await" is preferred over ``inlineCallbacks``. Coroutines
    are supported by dedicated Python syntax, are compatible with ``asyncio``, and
    provide higher performance.

Example
=======

As an example, consider this function from the `Twisted documentation`_:

.. code-block:: python

  from twisted.internet.defer import Deferred, inlineCallbacks

  @inlineCallbacks
  def makeRequest(method: str, url: str):
      # ... do some HTTP stuff ...
      return response

  @inlineCallbacks
  def getUsers():
      responseBody = yield makeRequest("GET", "/users")
      return json.loads(responseBody)

  def main(reactor):
    return getUsers()

This could be rewritten to a bit more of modern:

.. code-block:: python

  async def makeRequest(method: str, url: str) -> str:
      # ... do some HTTP stuff ...
      return response

  async def getUsers() -> dict:
      responseBody = await makeRequest("GET", "/users")
      return json.loads(responseBody)

  def main(reactor):
    return defer.ensureDeferred(getUsers())

Not too big of a difference, but definitely a bit nicer. In particular, note:

* There's no decorator, so tools like mypy know what ``getUsers`` actually returns.
* ``main`` now includes a call to |defer.ensureDeferred|_ to transition back to
  something that Twisted understands. [#]_

Rules for conversion
====================

The result of calling an ``async`` function is an ``Awaitable``, the result of
calling an ``inlineCallbacks`` function is a ``Deferred``. ``async`` functions
use ``await`` internally to wait for another ``Awaitable``, ``inlineCallbacks``
use ``yield`` internally to wait for another ``Deferred``.

This results in the following rules:

* You can ``await`` a ``Deferred`` (since it is also an ``Awaitable``).
* You cannot ``yield`` an ``Awaitable``.
* You can convert an ``Awaitable`` into a ``Deferred`` via ``defer.ensureDeferred``.
* Calling ``await`` on a non-``Awaitable`` is a runtime error (though note that
  you can ``yield`` on a non-``Deferred`` and it just immediately continues).
* Twisted APIs still expect ``Deferreds``.

To convert a single function this turns out to be pretty simple:

+---------------------+--------------------------------------+-----------+
| What                | Twised                               | asyncio   |
+=====================+======================================+===========+
| Function definition | ``@defer.inlineCallbacks`` decorator | ``async`` |
+---------------------+--------------------------------------+-----------+
| Wait for result     | ``yield``                            | ``await`` |
+---------------------+--------------------------------------+-----------+

Methodology for conversion
==========================

The difficult comes when you have a large codebase that you want to convert from
``defer.inlineCallbacks`` to ``async``/``await``. Below is how I approached this
for the Synapse code:

Since you can ``await`` a ``Deferred`` the easiest way to do this is to start at
the outer layers and work inward. By doing this you end up with ``async``
functions which call into code which return a ``Deferred``, but this is fine.

For Synapse we converted things via:

1. The REST layer.
2. The handler layer.
3. The database layer.

In order to avoid doing an entire layer at once it is ideal to start with the
modules which are called into the least (and preferably only via a higher layer).
If there are other callers which have not yet been converted, the call-site is
modified to wrap the returned ``Awaitable`` with ``defer.ensureDeferred``. Additionally,
this is used whenever a Twisted API expects a ``Deferred``.

The REST layer in Synapse is built on ``twisted.web`` and needed some extra magic,
see |AsyncResource|_ and sub-classes, in particular it:

1. Overrides the ``render`` method (which is a Twisted API from ``IResource``).

   1. Calls the async function with ``defer.ensureDeferred`` to ensure it gets
      scheduled with the reactor.
   2. Returns ``NOT_DONE_YET`` so that Twisted doesn't close the connection.
2. It then searches for a method called ``_async_render_<HTTP METHOD>`` and calls
   it with the ``Request`` object.
3. If the result is an ``Awaitable`` it calls ``await`` to get the "real" result.
4. Finally it sends the response using Twisted APIs.

Other thoughts
==============

The Synapse code had many places which were undecorated functions which called
return a ``Deferred`` via calling something else. While doing this conversion we
updated these functions to be ``async`` and then internally ``await`` the called
function, for clarity. (Originally this was done for performance, but the overhead
should be minimal when using ``async``/``await``.)

This also involved updating the tests to match the type as well (i.e. if a
function was made ``async`` and we mock that function somewhere, the mock should
also be ``async``).

While doing this we also fixed up some of the type hints of return values since
mypy will actually check them once you remove the ``defer.inlineCallbacks`` decorator.

Measuring progress
==================

As part of this I threw together an "`Are We Async Yet?`_" site. It is pretty
basic, but tracks the amount of code using ``defer.inlineCallbacks`` vs. ``async``.
As a side-effect you can see how the code has grown over time (with a few instances
of major shrinking). [#]_

And last, but not least, I definitely did not convert all of Synapse myself! It
was done incrementally by the entire team over years! My coworkers mostly laid
the groundwork and I did much of the mechanical changes. And...we're still not
*quite* done, although the remaining places heavily interact with Twisted APIs
or manually generate a ``Deferred`` and use ``addCallback`` (so they're not
straightforward to convert).

.. [#] Added in Python 3.5 via `PEP 492`_.
.. [#] Newer than version 15.0 according to the `Twisted documentation`_.
.. [#] The `documentation for async/await`_ suggests using |Deferred.fromCoroutine|_
       instead, but that is new in Twisted v21.2.0.
.. [#] You can `find the code on GitHub`_.

.. |inlineCallbacks| replace:: ``inlineCallbacks``
.. _inlineCallbacks: https://twistedmatrix.com/documents/21.2.0/api/twisted.internet.defer.html#inlineCallbacks
.. _issue #7988: https://github.com/matrix-org/synapse/issues/7988
.. _Twisted documentation: https://twistedmatrix.com/documents/21.2.0/core/howto/defer-intro.html#inline-callbacks-using-yield
.. _gained some support: https://twistedmatrix.com/documents/21.2.0/core/howto/defer-intro.html#coroutines-with-async-await
.. |defer.ensureDeferred| replace:: ``defer.ensureDeferred``
.. _defer.ensureDeferred: https://twistedmatrix.com/documents/21.2.0/api/twisted.internet.defer.html#ensureDeferred
.. |AsyncResource| replace:: ``_AsyncResource``
.. _AsyncResource: https://github.com/matrix-org/synapse/blob/4b965c862dc66c0da5d3240add70e9b5f0aa720b/synapse/http/server.py#L228-L309
.. _IResource: https://twistedmatrix.com/documents/21.2.0/api/twisted.web.resource.IResource.html#render
.. _Are We Async Yet?: https://patrick.cloke.us/areweasyncyet/

.. _PEP 492: https://www.python.org/dev/peps/pep-0492/
.. _documentation for async/await: https://twistedmatrix.com/documents/21.2.0/core/howto/defer-intro.html#coroutines-with-async-await
.. |Deferred.fromCoroutine| replace:: ``Deferred.fromCoroutine``
.. _Deferred.fromCoroutine: https://twistedmatrix.com/documents/21.2.0/api/twisted.internet.defer.Deferred.html#fromCoroutine
.. _find the code on GitHub: https://github.com/clokep/areweasyncyet
