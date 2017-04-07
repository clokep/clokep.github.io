"Adding Two-Factor Authentication to Django (with ``django-allauth``)" Lightning Talk
#####################################################################################
:date: 2017-04-06 21:14
:author: Patrick Cloke
:tags: django, talks
:slug: django-allauth-2fa-lightning-talk

A bit late on this article, but better late than never! Back on October 27th,
2016 I gave a talk at `Django Boston`_ entitled "Adding Two-Factor
Authentication to Django (with ``django-allauth``)". It was a ~20 minute talk on
integrating the `django-allauth-2fa`_ package into a Django_ project. The
package (which I should note is maintained by my employer and used in production
on `Strongarm`_) expands the excellent `django-allauth`_ package by adding
`two-factor authentication`_ using `TOTP`_ (and backup codes).

Integrating this into your project is (mostly) just some configuration changes
to your ``settings.py``, and URL configuration! It takes advantage of the awesome
`adapter`_ methodology, the `django-otp`_ package to do all the 2FA bits, and
some custom middleware to enforce 2FA during login.

You can view a `rendered version`_ of the slides online (use the arrow keys to
navigate) or check out the `source`_. We're always look for more contributors to
`django-allauth-2fa`_, there's plenty to do, including:

*   More testing needed (different configurations, interaction with social
    accounts).
*   Support for more device types (e.g. HOTP, YubiKey, Twilio). (`#23`_)
*   Support for multiple devices per user. (`#36`_)
*   Improving the documentation (e.g. add a quickstart document).
*   Setting up and adding translations.
*   Any other feedback you might have!

You can also check out the open `issues on GitHub`_ or `reach out`_ directly if
you're interested!

.. _Django Boston: http://www.meetup.com/djangoboston/
.. _django-allauth-2fa: https://github.com/percipient/django-allauth-2fa/
.. _Django: https://www.djangoproject.com/
.. _Strongarm: https://strongarm.io
.. _django-allauth: http://www.intenct.nl/projects/django-allauth/
.. _two-factor authentication: https://en.wikipedia.org/wiki/Multi-factor_authentication
.. _TOTP: https://en.wikipedia.org/wiki/Time-based_One-time_Password_Algorithm

.. _adapter: http://django-allauth.readthedocs.io/en/latest/advanced.html
.. _django-otp: https://bitbucket.org/psagers/django-otp/

.. _rendered version: http://files.patrick.cloke.us/boston-django-20161027/
.. _source: https://github.com/percipient/talks/tree/master/boston_django_10_27_2016/adding-two-factor-authentication-to-django
.. _issues on GitHub: https://github.com/percipient/django-allauth-2fa/issues
.. _reach out: {filename}/pages/contact.rst

.. _#23: https://github.com/percipient/django-allauth-2fa/issues/23
.. _#36: https://github.com/percipient/django-allauth-2fa/issues/36
