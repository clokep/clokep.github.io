#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = u'Patrick Cloke'
SITENAME = u'Like bricks in the sky'

TIMEZONE = 'America/New_York'
DEFAULT_DATE_FORMAT = '%m/%d/%Y %I:%M %p UTC'

DEFAULT_LANG = u'en'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None

# Blogroll
LINKS =  (('Pelican', 'http://getpelican.com/'),
          ('Python.org', 'http://python.org/'),
          ('Jinja2', 'http://jinja.pocoo.org/'),
          ('You can modify those links in your config file', '#'),)

# Social widget
SOCIAL = ()

GITHUB_URL = "https://www.github.com/clokep"
TWITTER_URL = "https://www.twitter.com/clokep"
BITBUCKET_URL = "https://bitbucket.org/clokep"
MOZILLIANS_URL = "https://mozillians.org/clokep"

DEFAULT_PAGINATION = 5

# Uncomment following line if you want document-relative URLs when developing
RELATIVE_URLS = True

# Content directory.
PATH = 'content'
PAGE_DIR = '../pages'

STATIC_PATHS = ['images']

PAGE_EXCLUDES = ['theme']
ARTICLE_EXCLUDES = ['theme']

THEME = 'theme'
