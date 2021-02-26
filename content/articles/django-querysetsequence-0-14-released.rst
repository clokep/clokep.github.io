django-querysetsequence 0.14 released!
######################################
:date: 2021-02-26 12:31
:author: Patrick Cloke
:tags: django, django-querysetsequence
:slug: django-querysetsequence-0-14-released

`django-querysetsequence`_ 0.14 has been released with support for Django 3.2 (and
Python 3.9). django-querysetsequence is a Django package for
|treating multiple QuerySet instances as a single QuerySet|_, this can be useful
for treating similar models as a single model. The ``QuerySetSequence`` class
supports `much of the API`_ available to ``QuerySet`` instances.

The marquee features of this release are:

* Support for |values()|_ and |values_list()|_ to retrieve the results as
  dictionaries / tuples (instead of ``Model`` instances).
* Partial support for |distinct()|_ -- this is only supported when each underlying
  ``QuerySet`` is a unique ``Model``.
* `Prettier documentation`_ is available.

.. _much of the API: https://django-querysetsequence.readthedocs.io/en/latest/api.html
.. |values()| replace:: ``values()``
.. _values(): https://docs.djangoproject.com/en/dev/ref/models/querysets/#values
.. |values_list()| replace:: ``values_list()``
.. _values_list(): https://docs.djangoproject.com/en/dev/ref/models/querysets/#values-list
.. |distinct()| replace:: ``distinct()``
.. _distinct(): https://docs.djangoproject.com/en/dev/ref/models/querysets/#distinct
.. _Prettier documentation: https://django-querysetsequence.readthedocs.io/

The full changelog is included below:

Features
--------

* Support Django 3.2 (`#78 <https://github.com/clokep/django-querysetsequence/pull/78>`_,
  `#81 <https://github.com/clokep/django-querysetsequence/pull/81>`_)
* Support Python 3.9. (`#78 <https://github.com/clokep/django-querysetsequence/pull/78>`_)
* Support the ``values()`` and ``values_list()`` methods.
  (`#73 <https://github.com/clokep/django-querysetsequence/pull/73>`_,
  `#74 <https://github.com/clokep/django-querysetsequence/pull/74>`_)
* Support the ``distinct()`` method when each ``QuerySet`` instance is from a
  unique model. Contributed by
  `@jpic <https://github.com/jpic>`_. (`#77 <https://github.com/clokep/django-querysetsequence/pull/77>`_,
  `#80 <https://github.com/clokep/django-querysetsequence/pull/80>`_)
* Add `Sphinx documentation <https://django-querysetsequence.readthedocs.io/>`_
  which is available at Read the Docs.

Bugfixes
--------

* Support calling ``filter()`` with |Q() objects|_. Contributed by
  `@jpic <https://github.com/jpic>`_. (`#76 <https://github.com/clokep/django-querysetsequence/pull/76>`_)

.. |Q() objects| replace:: ``Q()`` objects
.. _Q() objects: https://docs.djangoproject.com/en/dev/ref/models/querysets/#q-objects

Miscellaneous
-------------

* Add an additional test for the interaction of ``order_by()`` and ``only()``.
  (`#72 <https://github.com/clokep/django-querysetsequence/pull/72>`_)
* Support Django REST Framework 3.12. (`#75 <https://github.com/clokep/django-querysetsequence/pull/75>`_)
* Switch continuous integration to GitHub Actions. (`#79 <https://github.com/clokep/django-querysetsequence/pull/79>`_)
* Drop support for Python 3.5. (`#82 <https://github.com/clokep/django-querysetsequence/pull/82>`_)

.. _django-querysetsequence: https://github.com/clokep/django-querysetsequence/
.. |treating multiple QuerySet instances as a single QuerySet| replace:: treating multiple ``QuerySet`` instances as a single ``QuerySet``
.. _treating multiple QuerySet instances as a single QuerySet: {filename}/articles/combining-disparate-querysets-in-django.md
