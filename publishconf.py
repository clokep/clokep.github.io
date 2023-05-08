#!/usr/bin/env python

import os
import sys

sys.path.append(os.curdir)
from pelicanconf import *

SITEURL = "https://patrick.cloke.us"

# Don't publish drafts.
WITH_FUTURE_DATES = False

# Configure RSS and atom feeds.
FEED_DOMAIN = SITEURL
FEED_ALL_ATOM = "feeds/atom.xml"
FEED_ALL_RSS = "feeds/rss.xml"
TAG_FEED_ATOM = "feeds/tag/{slug}.atom.xml"
TAG_FEED_RSS = "feeds/tag/{slug}.rss.xml"

# By default only include the latest 10 articles.
FEED_MAX_ITEMS = 10

# Include the full articles, not just a summary.
RSS_FEED_SUMMARY_ONLY = False

DELETE_OUTPUT_DIRECTORY = True

# Following items are only useful when publishing
DISQUS_SITENAME = "clokep"

# Enable analytics.
ANALYTICS_ENABLED = True
