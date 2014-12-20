#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = u'Patrick Cloke'
AUTHOR_EMAIL = 'patrick@cloke.us'
SITENAME = u'Like bricks in the sky'
GITHUB_URL = 'https://github.com/clokep/clokep.github.io'

TIMEZONE = 'America/New_York'
DEFAULT_DATE_FORMAT = '%m/%d/%Y %I:%M %p %Z'

DEFAULT_LANG = u'en'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
TRANSLATION_FEED_ATOM = None

# Appliy the typogrify improvements.
TYPOGRIFY = True

# Uncomment following line if you want document-relative URLs when developing
RELATIVE_URLS = False

# Disable categories.
DISPLAY_CATEGORIES_ON_MENU = False
DISPLAY_CATEGORY_ON_ARTICLE = False
CATEGORY_FEED_ATOM = None
CATEGORY_SAVE_AS = ''
CATEGORIES_SAVE_AS = ''

# This is a hack to make the author URLs link to my about page (without
# modifying the template).
AUTHOR_URL = 'pages/about.html'
# Disable generating author pages.
AUTHOR_SAVE_AS = ''
AUTHORS_SAVE_AS = ''

# Set up locations of articles, pages and theme.
PATH = 'content'
ARTICLE_PATHS = ['articles']
PAGE_PATHS = ['pages']

# This is currently a modified copy of notmyidea, one of the default themes.
THEME = 'theme'

# Set up static content and output locations.
STATIC_PATHS = [
    'images',
    'js',
    'static',
]
EXTRA_PATH_METADATA = {
    # Disable GitHub's Jekyll parsing, this will allow folders starting with a .
    # to be served:
    # https://help.github.com/articles/files-that-start-with-an-underscore-are-missing/
    'static/.nojekyll': {'path': '.nojekyll'},
    # Tell GitHub the domain name:
    # https://help.github.com/articles/adding-a-cname-file-to-your-repository/
    'static/CNAME': {'path': 'CNAME'},
    # Server an Autoconfig entry for email:
    # https://developer.mozilla.org/en-US/docs/Mozilla/Thunderbird/Autoconfiguration
    'static/mail-config.xml': {'path': '.well-known/autoconfig/mail/config-v1.1.xml'},
}
TEMPLATE_PAGES = {
    # Custom 404 page for GitHub pages.
    '404.html': '404.html',
}

# Plugin setup.
PLUGIN_PATHS = [
    'pelican-plugins/',
]
PLUGINS = [
    'assets',
    'extract_toc',
    'gravatar',
    'share_post',
    'thumbnailer',

    # Custom plug-ins.
    'strikethrough',
]

# Change the default URLs.
ARTICLE_URL = 'posts/{date:%Y}/{date:%m}/{date:%d}/{slug}/'
ARTICLE_SAVE_AS = ARTICLE_URL + 'index.html'

# Paginate, but have at least three items per page.
DEFAULT_ORPHANS = 2
DEFAULT_PAGINATION = 5

TAG_CLOUD_MAX_ITEMS = 10

# Auto-generated content.
DISPLAY_PAGES_ON_MENU = True
LINKS = ()
SOCIAL = (
    ('twitter', 'https://www.twitter.com/clokep'),
    ('bitbucket', 'https://bitbucket.org/clokep'),
    ('github', 'https://www.github.com/clokep'),
    ('mozillians', 'https://mozillians.org/u/clokep/'),
)

# For thumbnails.
IMAGE_PATH = 'images'
THUMBNAIL_SIZES = {
    'small': '?x150',
    'medium': '?x350',
}
