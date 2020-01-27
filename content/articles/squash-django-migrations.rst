Squashing Django Migrations
###########################
:date: 2020-01-27 16:34
:author: Patrick Cloke
:tags: django

The `Django migration system`_ is great for modifying your database schema after
a database is live. If you're like me, you quickly end up with many 10s or 100s
of migrations. There's nothing inherently wrong with this, but there's a few
cases where it gets tiresome to run all these migrations:

* Occasionally I want to reset my database to a pristine state and reload fixtures.
* We check if there are any missing migrations as part of our continuous integration job.
* Unit tests must run all migrations.

I don't think running the additional migrations really takes that much longer,
but I like keeping the number of run migrations down, especially if there are
multiple data migrations, etc.

This articles details the rough steps that I follow when `squashing migrations`_.

Pre-squash steps
================

If you've previously squashed migrations do the following:

1.  Remove the ``replaces`` property from the previously squashed migration
    (this property gets created as part of squashing migrations).
2.  If the ``dependencies`` properties of any other migrations point to
    migrations that used to be in ``replaces``, you'll need to update these to
    point to the squashed migration. E.g. if a dependency is
    ``('my_app', '0001_initial')``, but you've previously squashed the
    dependencies for ``my_app``, you'll need to replace this with
    ``('my_app', '0001_squashed_0010_add_field')`` before squashing migrations
    for ``my_app`` a second time.

Squashing steps
===============

At this point you should have the migrations in the proper state for squashing
migrations. I do the following:

1.  Remove any ``RunPython`` operations that were only needed once (i.e. you
    don't need them in the squashed migration).
2.  Run the ``squashmigrations`` command for the desired application:

    .. code-block:: bash

        python manage.py squashmigrations my_app <name-of-last-migration>

3.  If there are any ``RunPython`` calls, copy them from the old migration to
    the squashed migration file.
4.  Delete the old migration files.
5.  Run ``pyclean`` to ensure the byte-code of the old migrations is gone.
6.  Edit the squashed migration file to reduce operations to as few as possible
    (this is usually 1 operation per field), starting at the list of
    ``operations`` in the file do the following:

    1.  Skip calls to ``CreateModel``, ``AlterUniqueTogether``.
    2.  For an ``AlterField`` call, copy the ``field`` kwarg to be the second
        tuple entry of where that field is initially created in an earlier
        ``CreateModel`` call.
    3.  For an ``AddField`` call, create a new tuple in the earlier
        ``CreateModel`` call with the contents of the ``name`` and ``field``
        kwargs.
    4.  For a ``RemoveField`` call, remove the tuple that matches the ``name``
        kwarg from the earlier ``CreateModel`` call.
    5.  For a ``DeleteModel`` call, remove the earlier ``CreateModel`` call.
    6.  Repeat for the above operations until all the number of operations is
        reduced to essentially the ``CreateModel`` calls. Note that some calls
        cannot be removed (e.g. you need both models to exist before having a
        foreign key between them).

        There is also a few other more complicate operations not detail above,
        but the modifications to the ``CreateModel`` call is usually pretty
        straightforward.

7.  Check if any migrations need to be created using the following:

    .. code-block:: bash

        python manage.py makemigrations --dry-run --check

    If any migraitons would be created then some operations were incorrectly
    squashed in step 6!

Throughout this process I usually make a commit after each step for easy
rollback in case I break something.

A brief example
===============

If we have the following migrations which create a model and then make some
operations:

.. code-block:: python

    # Source of 0001_initial
    from django.db import migrations, models

    class Migration(migrations.Migration):
        operations = [
            migrations.CreateModel(
                "Author",
                [
                    ("id", models.AutoField(primary_key=True)),
                    ("first_name", models.CharField(max_length=100)),
                    ("last_name", models.CharField(max_length=100)),
                ],
            ),
        ]

.. code-block:: python

    # Source of 0002_second
    from django.db import migrations, models

    def combine_name(apps, schema_editor):
        """Combine the first and last names with a space between into a new field."""
        Author = apps.get_model('my_app', 'Author')
        for author in Author.objects.iterator():
            author.name = '{} {}'.format(author.first_name, author.last_name)
            author.save(update_fields=['name'])

    class Migration(migrations.Migration):
        dependencies = [("migrations", "0001_initial")]
        operations = [
            migrations.AddField("Author", "name", models.CharField(max_length=255)),
            migrations.RunPython(combine_first_last_name),
            migrations.RemoveField("Author", "first_name"),
            migrations.RemoveField("Author", "last_name"),
        ]

After following steps 1 through 5 above you might get something like this for
the squashed migration:

.. code-block:: python
    :hl_lines: 15 16

    # Source of 0001_squashed_0002_second
    from django.db import migrations, models

    class Migration(migrations.Migration):
        replaces = [
            ("migrations", "0001_initial"),
            ("migrations", "0002_second"),
        ]

        operations = [
            migrations.CreateModel(
                "Author",
                [
                    ("id", models.AutoField(primary_key=True)),
                    ("first_name", models.CharField(max_length=100)),
                    ("last_name", models.CharField(max_length=100)),
                ],
            ),
            migrations.AddField("Author", "name", models.CharField(max_length=255)),
            migrations.RemoveField("Author", "first_name"),
            migrations.RemoveField("Author", "last_name"),
        ]

This can be edited down to the following:

.. code-block:: python
    :hl_lines: 15

    # Source of 0001_squashed_0002_second
    from django.db import migrations, models

    class Migration(migrations.Migration):
        replaces = [
            ("migrations", "0001_initial"),
            ("migrations", "0002_second"),
        ]

        operations = [
            migrations.CreateModel(
                "Author",
                [
                    ("id", models.AutoField(primary_key=True)),
                    ("name", models.CharField(max_length=255)),
                ],
            ),
        ]

Before squashing the migrations in this app again the ``replaces`` property
would need to be removed.

Final thoughts
==============

You might wonder why Django does not do this automatically, I believe this is
because Django sometimes reaches operations which it cannot combine without
knowledge of what is happening (e.g. a ``RunPython`` or ``RunSQL`` operation),
but it can be done manually using the above steps.

.. _Django migration system: https://docs.djangoproject.com/en/1.11/topics/migrations/
.. _squashing migrations: https://docs.djangoproject.com/en/1.11/topics/migrations/#squashing-migrations
