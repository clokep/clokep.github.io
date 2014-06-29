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
TRANSLATION_FEED_ATOM = None

# Appliy the typogrify improvements.
TYPOGRIFY = True

# Uncomment following line if you want document-relative URLs when developing
RELATIVE_URLS = True

# Disable categories.
CATEGORY_FEED_ATOM = None
CATEGORY_SAVE_AS = ''
CATEGORIES_SAVE_AS = ''

# Disable author pages.
AUTHOR_SAVE_AS = ''
AUTHORS_SAVE_AS = ''

# Set up locations of articles, pages and theme.
PATH = 'content'
PAGE_DIR = '../pages'

PAGE_EXCLUDES = ['theme']
ARTICLE_EXCLUDES = ['theme']

# This is currently a modified copy of the gum theme:
# https://github.com/getpelican/pelican-themes/tree/master/gum
THEME = 'theme'

# Set up static content and output locations.
STATIC_PATHS = [
    'images',
    'static/CNAME'
]
EXTRA_PATH_METADATA = {
    'static/CNAME': {'path': 'CNAME'},
}

# Plugin setup.
PLUGIN_PATH = '../pelican-plugins/'
PLUGINS = ['extract_toc']

# Change the default URLs.
ARTICLE_URL = 'posts/{date:%Y}/{date:%b}/{date:%d}/{slug}/'
ARTICLE_SAVE_AS = 'posts/{date:%Y}/{date:%b}/{date:%d}/{slug}/index.html'

# Paginate, but have at least three items per page.
DEFAULT_ORPHANS = 2
DEFAULT_PAGINATION = 5

TAG_CLOUD_MAX_ITEMS=10

# Auto-generated content.
LINKS = ()
SOCIAL = (
    ('twitter', 'https://www.twitter.com/clokep'),
    ('bitbucket', 'https://bitbucket.org/clokep'),
    ('github', 'https://www.github.com/clokep'),
    ('mozillians', 'https://mozillians.org/clokep'),
)
