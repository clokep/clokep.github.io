Using MySQL's ``LOAD DATA`` with Django
#######################################
:date: 2020-01-23 20:49
:author: Patrick Cloke
:tags: django

While attempting to improve performance of bulk inserting data into MySQL
database my coworker came across the |LOAD DATA|_ SQL statement. It allows you
to read data from a text file (in a comma separated variable-like format) and
quickly insert it into a table. There's two variations of it, a local remote
version. We did not experiment with the local version since we were connecting
to a remote MySQL server and did not have access to the database's local disk.

Since we are using Django we were hoping to match the calling behavior of the
|bulk_create|_ method of a ``QuerySet`` to do the following:

1. Write the data to be inserted into a temporary file.
2. Execute the ``LOAD DATA`` referencing the file.
3. Clean-up the temporary file.

After a bit of experimentation we were able to come up with a sub-class of
``QuerySet`` with the desired features. This is heavily based on
`Django's implementation`_ of |bulk_create|. There were a few details to get
this to work properly:

* Dynamically getting the fields to insert into the database.
* Converting the Python value to a proper string value for database insertion.
* Ensuring the proper database was used when using a read-replica with a router.

.. warning::

    The below code is not fully vetted if the escaping of the database values is
    safe.

    It is also missing error checking and handling of edge-cases (e.g. an empty
    list of objects; see the start of the |bulk_create| implementation).

Without further ado, see the implementation:

.. include:: ../code/query_load_data.py
    :code: python
    :class: highlight

This can be used by `using a custom manager`_ to the ``LoadDataQuerySet``
manager.

.. code-block:: python
    :hl_lines: 6

    from django.db import models

    class OpinionPoll(models.Model):
        question = models.CharField(max_length=200)
        poll_date = models.DateField()
        objects = LoadDataQuerySet.as_manager()

You can then easily call ``load_data()`` just like you would ``bulk_create()``!

.. code-block:: python
    :hl_lines: 14

    from datetime import date

    # Ask the same poll on the first of each month.
    polls = []
    for month in range(12):
        polls.append(
            OpinionPoll(
                question="What's your favorite ice cream?",
                poll_date=date(2020, month, 1)
            )
        )

    # Insert all the polls at once.
    OpinionPoll.objects.load_data(polls)

Although the above code did work (using Django 1.11.x and MySQL 5.6, it should
work without much work on similar versions) only a small increase in insertion
rate was observed. In order to avoid complexity (and custom code) it was decided
that the above code was not worth keeping, but it was a fun journey into
extending Django's ``QuerySet`` methods (and investigating obscure MySQL
features).

.. |LOAD DATA| replace:: ``LOAD DATA``
.. _LOAD DATA: https://dev.mysql.com/doc/refman/5.6/en/load-data.html
.. |bulk_create| replace:: ``bulk_create()``
.. _bulk_create: https://docs.djangoproject.com/en/1.11/ref/models/querysets/#bulk-create
.. _Django's implementation: https://github.com/django/django/blob/7fd1ca3ef63e5e834205a8208f4dc17d80f9a417/django/db/models/query.py#L402-L451
.. _using a custom manager: https://docs.djangoproject.com/en/1.11/topics/db/managers/#custom-managers
