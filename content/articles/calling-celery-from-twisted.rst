Calling Celery from Twisted
###########################
:date: 2018-10-23 19:24
:author: Patrick Cloke
:tags: twisted, celery

.. contents::

Background
==========

I use Twisted_ and Celery_ daily at work, both are useful frameworks, both have
a lot of great information out there, but a particular use (that I haven't seen
discussed much online, hence this post) is calling Celery tasks *from* Twisted
(and subsequently using the result).

The difference between Twisted and Celery seems to be a frequent question people
have (check out the number of questions on StackOverflow_). The main difference,
from my point of view, is that Twisted is a "batteries included" networking
framework that is asynchronous / evented for handling of I/O, Celery is a *distributed*
task queue which excels at short CPU-bound tasks where the asynchronous nature
comes from running multiple processes. The txCelery_ project has a nice summary
on their page:

    Celery is an outstanding choice for dispatching *short-lived*,
    computationally-expensive tasks to a distributed backend system. Note the
    emphasis; Celery is ill-suited for tasks tasks that require updating some
    in-memory representation with out-of-process data. If you want a specific
    process to read data from standard input, for instance, good luck...

    Twisted can be though of as having the opposite problem. Twisted is very
    good at maintaining and updating in-memory representations over extended
    periods of time, but fails miserably at performing expensive computations.
    Twisted notably has no built-in constructs for managing distributed task
    queues.

The two main ways to interact with Celery are:

1. Call a task (and have it happen asynchronously).
2. Get the result of that task.

In order to call Celery from Twisted we'll need to ensure that both of these can
happen in a way that matches Twisted's execution model. This might be
illustrated best by a code example, we would want to do something like the
following:

.. code-block:: python

    from celery import Celery

    from twisted.internet import defer, task

    app = Celery(broker='amqp://guest:guest@127.0.0.1:5672//', backend='rpc')

    @app.task
    def my_task(a, b):
        # Normally you'd do a CPU bound task here.
        return a + b

    @defer.inlineCallbacks
    def main():
        # Normally you'd open some listening sockets or some outbound
        # connections here.

        # Call into Celery!
        result = yield my_task.delay(1, 2)
        # Should print '1 + 2 = 3'.
        print("{} + {} = {}".format(1, 2, result))

    if __name__ == '__main__':
        task.react(main)

Initial Approach
================

The initial attempt to pair these libraries is to call Celery tasks like you
would normally (import the Celery task and call |delay()|_ on it). [#]_ There's
a hint that this won't work in `the documentation`_ however:

    Apply tasks asynchronously by sending a message.

The documentation around calling |AsyncResult.get()|_, to retrieve the result
also hints about issues:

    Wait until task is ready, and return its result.

It isn't incredibly clear from the documentation, but this points to two
separate issues with calling Celery from Twisted:

1.  In both of these situations, (synchronous) I/O is happening in the
    background when you make this call! [#]_ I/O happening outside of the
    reactor is a big no-no in a Twisted process since it can block the reactor
    from running. [#]_
2.  Additionally, the ``AsyncResult.get()`` call blocks until a result is ready,
    this doesn't fit well into an evented programming paradigm. [#]_

The second problem is handled well by the txCelery_ package, it allows you to
call a task and get a sub-class of |Deferred|_ which resolves into the result
of the task call by periodically monitoring the status of the result.

Unfortunately txCelery doesn't solve the first issue (to my knowledge) since it
just uses the normal mechanisms built into Celery for I/O (which causes I/O in
the reactor thread).

Threaded Approach
=================

Twisted has a thread pool and makes it super easy to ask it to "run this code in
a non-reactor thread and return the result to me". It is pretty straightforward
to cobble together a way to use |threads.deferToThread()|_ to call
|Celery.send_task()|_ [#]_. You still need an asynchronous way to check if the
task result is ready, however. You could just call ``AsyncResult.get()`` in a
thread, but you will likely quickly exhaust your thread pool since that blocks
until a result is ready. Alternately you can check the status of a task using
the |state|_ property of an ``AsyncResult``. (I found it very surprising that
accessing a *property* of this object causes I/O to happen, but it does.)

Connecting these ideas together we came up with something similar to the
following (note that this is heavily inspired by what txCelery does, but pushes
all I/O onto a separate thread instead of doing it in the reactor thread):

.. include:: ../code/calling-celery-from-twisted/threadedcelery.py
    :code: python
    :class: highlight

The calling syntax of this isn't as nice as the initial approach, but it is
pretty close (the modified lines are highlighted):

.. code-block:: python
    :hl_lines: 4 19

    from celery import Celery

    from twisted.internet import defer, task
    from twistedcelery import send_task

    app = Celery(broker='amqp://guest:guest@127.0.0.1:5672//', backend='rpc')

    @app.task
    def my_task(a, b):
        # Normally you'd do a CPU bound task here.
        return a + b

    @defer.inlineCallbacks
    def main():
        # Normally you'd open some listening sockets or some outbound
        # connections here.

        # Call into Celery!
        result = yield send_task(app, 'my_task', args=(1, 2))
        # Should print '1 + 2 = 3'.
        print("{} + {} = {}".format(1, 2, result))

    if __name__ == '__main__':
        task.react(main)

Twisted-native Approach
=======================

I think the above solutions are fundamentally wrong, but are easy-ish to
implement. They might work OK for small loads, or if increased latency is
acceptable, but will start to fail when a large number of pending tasks are
necessary. A better way is to consider:

1. Celery is designed to be `language`_ `independent`_.
2. Celery `message formats`_ are part of the public "API". [#]_
3. Celery uses standard networking protocols to enable distributed processing.
4. Twisted is designed to efficiency implement networking protocols.

This lead me to the conclusion that Twisted can just treat Celery tasks as if it
is implemented in a different language and just try to directly communicate with
the Celery broker and backend. It can just send task calls and query for
responses, when available. We can be a little bit more clever, however, and use
Celery to process the details of the messages to send, the queue to send them
to, etc.

The hope is to end up with code like this (again, modified lines are
highlighted):

.. code-block:: python
    :hl_lines: 4 18 19 20 23

    from celery import Celery

    from twisted.internet import defer, task
    from twistedcelery import TwistedCelery

    app = Celery(broker='amqp://guest:guest@127.0.0.1:5672//', backend='rpc')

    @app.task
    def my_task(a, b):
        # Normally you'd do a CPU bound task here.
        return a + b

    @defer.inlineCallbacks
    def main():
        # Normally you'd open some listening sockets or some outbound
        # connections here.

        # Turn the Celery app into a TwistedCelery app, which uses Twisted to do
        # I/O under the hood.
        tx_app = TwistedCelery(app)

        # Call into Celery!
        result = yield tx_app.send_task('my_task', args=(1, 2))
        # Should print '1 + 2 = 3'.
        print("{} + {} = {}".format(1, 2, result))

    if __name__ == '__main__':
        task.react(main)

I've started the `Twisted-Celery`_ project in order to accomplish this goal. It
uses Celery to create the messages and to decide what exchange/queue/etc. to
use, but allows Twisted to handle all communication to your configured Celery
broker and backend. It exposes a ``send_task()`` compatible API, but returns a
``Deferred`` instead of an ``AsyncResult`` so you can write Twisted-compatible
code easily.

It is just a proof of concept right now, but was successfully tested on a real
project. Note that it currently only supports AMQP, but this should be
expandable to other brokers. I won't go into the details of how it works here,
but the hope is that you can give it a configured Celery app and it "just works"
with Twisted.

If you're interested in helping out, checkout the `GitHub repository`_ or leave a
comment below.

.. [#]  If you're unfamiliar with Celery, briefly it allows a "task" is defined
        in Python code, a "worker" is used to execute those tasks. The code
        which wants to execute those tasks calls ``delay()`` or
        ``apply_async()`` on the "task", which returns an ``AsyncResult``, which
        can be used to retrieve the result of that task, once it runs.

.. [#]  Note that Celery is frequently used with web frameworks that might run
        on e.g. gunicorn_ with `async workers (using greenlets)`_, meaning that not
        everything is blocked, but that is somewhat beyond the scope of this
        post.

.. [#]  Twisted doesn't `magically make your code non-blocking`_.

.. [#]  Note that txCelery really only takes care of the second issue here.

.. [#]  ``Celery.send_task()`` is a generic way to call a task by name without
        importing it. It is generally useful, but in this particular case is a
        nice spot to generically interrupt how Celery communicates to the
        broker.

.. [#]  Note that there are two different versions of the protocol, they're
        fairly similar, but version 2 moves some meta data from the body to the
        headers to avoid needing to deserialize the entire mesage multiple
        times. You can read `the highlights`_ of the differences.

.. _Twisted: https://twistedmatrix.com/
.. _Celery: http://www.celeryproject.org/
.. _StackOverflow: https://stackoverflow.com/search?q=twisted+or+celery
.. _txCelery: https://github.com/SentimensRG/txCelery
.. |delay()| replace:: ``delay()``
.. _delay(): http://docs.celeryproject.org/en/latest/reference/celery.app.task.html#celery.app.task.Task.delay
.. _the documentation: http://docs.celeryproject.org/en/latest/reference/celery.app.task.html#celery.app.task.Task.delay
.. |AsyncResult.get()| replace:: ``AsyncResult.get()``
.. _AsyncResult.get(): http://docs.celeryproject.org/en/latest/reference/celery.result.html#celery.result.AsyncResult.get
.. |Deferred| replace:: ``Deferred``
.. _Deferred: http://twistedmatrix.com/documents/current/api/twisted.internet.defer.Deferred.html
.. |threads.deferToThread()| replace:: ``threads.deferToThread()``
.. _threads.deferToThread(): https://twistedmatrix.com/documents/current/api/twisted.internet.threads.html#deferToThread
.. |Celery.send_task()| replace:: ``Celery.send_task()``
.. _Celery.send_task(): http://docs.celeryproject.org/en/latest/reference/celery.html#celery.Celery.send_task
.. |state| replace:: ``state``
.. _state: http://docs.celeryproject.org/en/latest/reference/celery.result.html#celery.result.AsyncResult.state
.. _message formats: http://docs.celeryproject.org/en/latest/internals/protocol.html
.. _language: http://docs.celeryproject.org/en/latest/faq.html#is-celery-dependent-on-pickle
.. _independent: http://docs.celeryproject.org/en/latest/faq.html#is-celery-multilingual
.. _Twisted-Celery: https://github.com/clokep/twistedcelery
.. _GitHub repository: https://github.com/clokep/twistedcelery

.. _gunicorn: https://gunicorn.org/
.. _async workers (using greenlets): http://docs.gunicorn.org/en/latest/design.html
.. _magically make your code non-blocking: https://twistedmatrix.com/trac/wiki/FrequentlyAskedQuestions#HowdoIuseDeferredstomakemyblockingcodenon-blocking
.. _the highlights: http://docs.celeryproject.org/en/latest/history/whatsnew-4.0.html#new-protocol-highlights
