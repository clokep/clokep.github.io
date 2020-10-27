django-render-block 0.8 (and 0.8.1) released!
#############################################
:date: 2020-10-27 16:57
:author: Patrick Cloke
:tags: django, django-render-block
:slug: django-render-block-0.8-released

A couple of weeks ago I released version 0.8 of `django-render-block`_, this was
followed up with a 0.8.1 to fix a regression.

django-render-block is a small library that allows you render a specific ``block``
from a Django (or Jinja) template, this is frequently used for emails when you
want multiple pieces of an email together in a single template (e.g. the subject,
HTML body, and text body), but they need to be rendered separately before sending.

See the example below:

.. code-block:: jinja

  {% block subject %}Hello from django-render-block!{% endblock %}

  {% block text %}
  Hello!

  This is the text email body!
  {% endblock %}

  {% block html %}
  <h1>Hello!</h1>

  <p>This is the <b>HTML</b> email body!</p>
  {% endblock %}

Using django-render-block, each ``block`` can be rendered separately and then
passed into Django's `email system`_:

.. code-block:: python

  from django.core.mail import send_mail
  from render_block import render_block_to_string

  subject = render_block_to_string('email.html', 'subject')
  text_body = render_block_to_string('email.html', 'text')
  html_body = render_block_to_string('email.html', 'html')

  send_mail(
      subject,
      text_body,
      html_message=html_body,
  )

This particular release of django-render-block includes support for passing
a fully instantiated |Context|_ (instead of a simple ``dict``) into
``render_block_to_string``. This allows the caller to control whether
``autoescape`` is enabled and a few other features.

The full changelog is included below:

0.8.1 (October 15, 2020)
========================

*   Fixes a regression in v0.8 where a ``Context`` could not be re-used. Contributed
    by `@evanbrumley <https://github.com/evanbrumley>`_. (`#25 <https://github.com/clokep/django-render-block/pull/25>`_)

0.8 (October 6, 2020)
=====================

*   ``render_block_to_string`` now forwards the ``Context`` passed as ``context`` parameter.
    Contributed by `@bblanchon <https://github.com/bblanchon>`_. (`#21 <https://github.com/clokep/django-render-block/pull/21>`_)
*   Drop support for Python 3.5, officially support Python 3.9. (`#22 <https://github.com/clokep/django-render-block/pull/22>`_)

.. _django-render-block: https://github.com/clokep/django-render-block/
.. _email system: https://docs.djangoproject.com/en/3.1/topics/email/
.. |Context| replace:: ``Context``
.. _Context: https://docs.djangoproject.com/en/dev/ref/templates/api/#django.template.Context
