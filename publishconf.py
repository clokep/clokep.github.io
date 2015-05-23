#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

# This file is only used if you use `make publish` or
# explicitly specify it as your config file.

import os
import sys
sys.path.append(os.curdir)
from pelicanconf import *

SITEURL = 'http://patrick.cloke.us'
RELATIVE_URLS = False

# Don't publish drafts.
WITH_FUTURE_DATES = False

# Configure RSS and atom feeds.
FEED_DOMAIN = SITEURL
FEED_ALL_ATOM = 'feeds/atom.xml'
FEED_ALL_RSS = 'feeds/rss.xml'
TAG_FEED_ATOM = 'feeds/tag/%s.atom.xml'
TAG_FEED_RSS = 'feeds/tag/%s.rss.xml'

DELETE_OUTPUT_DIRECTORY = True

# Following items are often useful when publishing

DISQUS_SITENAME = "clokep"
GOOGLE_ANALYTICS = 'UA-52389517-1'
CLICKY = 100846713
