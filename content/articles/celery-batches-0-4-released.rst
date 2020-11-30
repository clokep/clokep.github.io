celery-batches 0.4 released!
############################
:date: 2020-11-30 16:50
:author: Patrick Cloke
:tags: celery, celery-batches
:slug: celery-batches-0.4-released

Earlier today I released a version `0.4`_ of `celery-batches`_ with support for
Celery 5.0. As part of this release support for Python < 3.6 was dropped and
support for Celery < 4.4 was dropped.

celery-batches is a small library that allows you process multiple calls to a
`Celery`_ task together. The batches can be processed based on a count of task
calls or a timer. It started as an update of the ``celery.contrib.batches``
code to support Celery 4.0+ and has grown to support some additional features.

The project was also transferred on GitHub to my personal namespace (from my
previous employer). Realistically it was maintained by me already and this is
just a formality. As part of this release the `documentation`_ is now available
on Read the Docs.

.. _0.4: https://pypi.org/project/celery-batches/0.4/
.. _celery-batches: https://github.com/clokep/celery-batches/
.. _Celery: https://github.com/celery/celery/
.. _documentation: https://celery-batches.readthedocs.io/en/v0.4/
