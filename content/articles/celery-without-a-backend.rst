Celery without a Results Backend
################################
:date: 2019-7-17 20:35
:modified: 2019-07-19 08:28
:author: Patrick Cloke
:tags: celery

The `Celery`_ |send_task|_ method allows you to invoke a task by name without
importing it. [#]_ There is an undocumented [#]_ caveat to using ``send_task``:
it doesn't have access to the configuration of the task (from when the task was
created using the |@task|_).

Much of this configuration doesn't matter to the caller, for example the caller
doesn't care about:

* Whether the task is bound or not.
* The retry configuration of tasks.

There is also configuration from the caller that *must* be right for the task to
execute as you'd expect:

* The number of arguments and the keywords for any keyword arguments.
* The serializer or compressor must match what the worker can handle.
* If a non-default results backend is to be used.

Another piece of configuration that matters (which surprised me and had a
performance impact for us [#]_) is whether to ignore a task result or not.
Unexpectedly, Celery will attempt to connect to the results backend *on task call*.
I assumed that the results backend would never be contaced since we never
attempted to **retrieve** a result! This turned out to be untrue.

Once identified, The fix was straightforward! We ensured that every task which
had ``ignore_result=True`` on task declaration also had ``ignore_result=True``
on task call (when using ``send_task``). [#]_ This duplciation is unfortunate,
but easy enough.

We figured this out due to a calling process which doesn't use any results, but
th e``celery.backends`` module was appearing in the `pyflame`_ profiles.
Another solution (for this particular setup) was to use the (`undocumented`_)
``disabled`` results backend.

.. [#]  There are a variety of reasons you might want to do this, but I've
        used it when tasks that use `Django`_ models but the calling process
        does not have Django configured.
.. [#]  I couldn't find any documentation about it at least. Maybe this is meant
        to be obvious, but it didn't click for me without deep understanding of
        how Celery works.
.. [#]  The performance impact we were seeing was due to the TCP negotiation and
        login to the results backend. This got especially bad if the results
        backend was under load or down.
.. [#]  Note that it is a `best practice`_ to ignore results on tasks where you
        don't need the result!

.. _Celery: http://www.celeryproject.org/
.. |send_task| replace:: ``send_task``
.. _send_task: https://docs.celeryproject.org/en/latest/reference/celery.html#celery.Celery.send_task
.. |@task| replace:: ``@task`` decorator
.. _@task: https://docs.celeryproject.org/en/latest/reference/celery.html#celery.Celery.task
.. _pyflame: https://pyflame.readthedocs.io
.. _undocumented: http://docs.celeryproject.org/en/latest/userguide/configuration.html#task-result-backend-settings

.. _Django: https://www.djangoproject.com/
.. _best practice: https://docs.celeryproject.org/en/latest/userguide/tasks.html?highlight=argsrepr#ignore-results-you-don-t-want
