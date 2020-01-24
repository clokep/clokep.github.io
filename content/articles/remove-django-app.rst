Cleanly removing a Django app (with models)
###########################################
:date: 2020-01-23 21:57
:author: Patrick Cloke
:tags: django

While pruning features from our product it was necessary to fully remove some
Django apps that had models in them. If the code is just removed than the tables
(and some other references) will be left in the database.

After doing this a few times for work I came up with the following basic steps
to completely remove a Django app.

1.  Remove any references to the app outside of itself (e.g. ``grep`` for the
    model names and other imports).
2.  Remove the any other files: e.g. ``forms.py``, ``urls.py``, ``views.py``,
    etc. Be sure to leave the migrations alone.
3.  Remove all content from the ``models.py`` file (but leave the file itself).
4.  Deploy to ensure nothing is attempting to access the model's tables.
5.  Run ``python manage.py makemigrations`` to generate the migrations that will
    delete the database tables.
6.  Deploy & run the migrations.
7.  Delete the app completely.
8.  Remove references to the app in ``INSTALLED_APPS``.
9.  Deploy so that nothing is referencing the app.
10. Run the following SQL commands to remove other references to the app in the
    database (replace ``my_app`` with the name of the app being removed):

.. code-block:: sql

    # Remove Django migrations.
    DELETE FROM `django_migrations` WHERE `app` = 'my_app';
    # Get rid of permissions and content types.
    DELETE FROM `auth_permission` WHERE `content_type_id` in (SELECT `id` FROM `django_content_type` WHERE `app_label` = 'my_app');
    # Get rid of admin changes.
    DELETE FROM `django_admin_log` WHERE `content_type_id` in (SELECT `id` FROM `django_content_type` WHERE `app_label` = 'my_app');
    # Finally, delete the content type.
    DELETE FROM `django_content_type` WHERE `app_label` = 'my_app';

If you're in the unfortunate situation of removing a third-party application
that has models, I've found it easiest to replace steps 2 - 3 & 5 - 6 with
standard drop table calls:

.. code-block:: sql

    DROP TABLE `my_app_some_model`;
    DROP TABLE `my_app_other_model`;

I'm fairly certain I got the initial idea for this from somewhere else, but
unfortunately I didn't save the original source. It has evolved over the past
years to be easier to run (e.g. the sub-queries) and I have used it > 5 times
without issues. It probably should be abstracted into a management command, but
I never got around to it.

I'm still surprised there isn't (to my knowledge) an easier way to do this
within Django!
