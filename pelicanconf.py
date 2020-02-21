#!/usr/bin/env python
# -*- coding: utf-8 -*- #
import os
import sys

# Ensure that filters are importable.
sys.path.append(os.path.dirname(__file__))

from filters import chunk, paginate

AUTHOR = 'Patrick Cloke'
AUTHOR_EMAIL = 'patrick@cloke.us'
SITENAME = 'Like bricks in the sky'
GITHUB_URL = 'https://github.com/clokep/clokep.github.io'

TIMEZONE = 'America/New_York'
DEFAULT_DATE_FORMAT = '%A, %B %-d, %Y'

DEFAULT_LANG = 'en'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
TRANSLATION_FEED_ATOM = None

# Appliy the typogrify improvements.
TYPOGRIFY = True

# Uncomment following line if you want document-relative URLs when developing
RELATIVE_URLS = False

# Disable categories.
CATEGORY_FEED_ATOM = None
CATEGORY_SAVE_AS = ''
CATEGORIES_SAVE_AS = ''

# This is a hack to make the author URLs link to my about page (without
# modifying the template).
AUTHOR_URL = 'pages/about.html'
# Disable generating author pages.
AUTHOR_SAVE_AS = ''
AUTHORS_SAVE_AS = ''

# Disable time based archives.
YEAR_ARCHIVE_SAVE_AS = ''
MONTH_ARCHIVE_SAVE_AS = ''
DAY_ARCHIVE_SAVE_AS = ''

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

    # Custom plug-ins to add additional RST directives.
    'directives',
]

# Custom Jinja filters.
JINJA_FILTERS = {
    'chunk': chunk,
    'paginate': paginate,
}

# Change the default URLs.
ARTICLE_URL = 'posts/{date:%Y}/{date:%m}/{date:%d}/{slug}/'
ARTICLE_SAVE_AS = ARTICLE_URL + 'index.html'

# Paginate, but have at least three items per page.
DEFAULT_ORPHANS = 2
DEFAULT_PAGINATION = 5

TAG_CLOUD_MAX_ITEMS = 10

# Auto-generated content.
SOCIAL = (
    ('twitter', 'https://www.twitter.com/clokep', 'twitter'),
    ('mastodon', 'https://mastodon.social/@clokep', 'mastodon'),
    ('github', 'https://www.github.com/clokep', 'github'),
    ('gitlab', 'https://gitlab.com/clokep', 'gitlab'),
    ('bitbucket', 'https://bitbucket.org/clokep', 'bitbucket'),
    ('mozillians', 'https://mozillians.org/u/clokep/', 'firefox'),
)

# For thumbnails.
IMAGE_PATH = 'images'
THUMBNAIL_SIZES = {
    'small': '?x150',
    'medium': '?x350',
}
