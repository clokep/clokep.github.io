Instantbird Blog: WordPress to Pelican
######################################
:date: 2020-09-09 17:10
:author: Patrick Cloke
:tags: Instantbird, pelican
:slug: instantbird-blog-wordpress-to-pelican

The `Instantbird blog`_ is now (as of mid-April 2020) hosted on GitHub Pages
(instead of self-hosted `WordPress`_) [#]_. Hopefully it was converted faithfully,
but feel free to let us know if you see something broken! You can file an issue
at `the repo for the blog`_ or just comment below.

Note that there are some changes due to being a static site instead of being
backed by a dynamic language. Most of these would be around editing the blog,
which we don't do anymore. The biggest user-facing change was that
`search is now via DuckDuckGo`_ instead of being built into the site.

This was a bit of an arduous process with some trial and error. See below for
some of the details. Overall I did this work over 3 years (!!!), starting in
April of 2017 and getting the site live in April of 2020. It was mostly done in
5 sprints with some long gaps between.

As some background, the Instantbird blog was originally (in 2007) served via
Florian's custom blog engine [#]_. In 2011 it was
`converted to WordPress by an Instantbird contributor`_. This initial conversion
was not done perfectly and I attempted to fix some of these issues when
converting from WordPress to Pelican [#]_. The general steps I was hoping to follow:

1. Setup the project using the ``pelican-quickstart`` comment.
2. Export the content via WordPress to XML.
3.  Use the Pelican `WordPress importer`_ to convert the content to reStructuredText. [#]_
4. Go through the conversion by hand and fix any oddities.
5. Convert the PHP theme to `Jinja2`_.

This plan mostly held together through the process, but I ran into some
roadblocks, most of which were easily overcome:

1. For some reason the WordPress import failed halfway through and didn't convert
   every article. I didn't investigate why and `added the missing files manually`_.
2. A variety of hard-coded HTML made it through the conversion. This was manually
   converted to reStructuredText.
3. Converting the theme was much harder than expected and involved reading
   WordPress documentation to understand various functions the PHP templates called.
4. Wrote a `custom archive plugin`_ to be able to articles by year / month / day.
5. The alignment of images needed to be fixed (and lots of WordPress styles
   removed).
6. Some of our posts had multiple categories on them, which is not allowed in
   Pelican. Generally these overlapped with tags and I decided the easiest path
   here was to modify the content to have a single category per article.

A huge piece of work was that comments were not imported. I did not care about
people being able to write *new* comments, but I wanted the old content there.
For this I planned to use the `pelican_comment_system plugin`_, but I needed to
get the comments into a format that it understood (from the WordPress XML export
discussed above).

I ended up `writing a custom script`_ based on the `pelican_import`_ code to
iterate the comments in the XML file and write a reStructuredText file for each
comment. There was quite a bit of trial and error here, but I think the result
was reasonable. This also needed to handle comment threads and pingbacks, which
added some wrinkles.

The final step here was to get gravatars for comments working. The
pelican_comment_system supports identicons only, but I was able to
`combine it and the gravatar plugin`_.

One final piece was generating a reasonable 404 page. The WordPress one some
features that required two more custom plugins: a `tag cloud`_ and a list of the
`most used categories`_.

There was a few other odds-and-ends that aren't really worth mentioning, but
overall I'm quite happy with the result! Just to be clear, there's no plans to
restart development of Instantbird, but I wanted the blog content to archived
and searchable. There's some `interesting`_ `articles`_ on there about `design`_
`decisions`_. Many of which are features I miss today!

.. [#] Reasons for wanting to do this included reducing the infrastructure we
       were maintaining and that the WordPress version was vulnerable. An
       additional benefit is that it let us easily add TLS.

       .. See https://bugzilla.mozilla.org/show_bug.cgi?id=1346658

.. [#] I don't think there's any information about this engine anywhere, nor do
       I think the source was released.

.. [#] The main issues were images / resources that were not properly moved.
       Luckily I was able to recover them using the `Internet Archive`_.

.. [#] I started doing this work on Pelican 3.7.1 and switched to 4.2.0, in
       general everything in this article should be valid up through Pelican
       4.2.0, however.

.. _Instantbird blog: https://blog.instantbird.org
.. _WordPress: https://wordpress.com/
.. _the repo for the blog: https://github.com/instantbird/blog.instantbird.org/
.. _search is now via DuckDuckGo: https://github.com/instantbird/blog.instantbird.org/blob/source/theme/templates/searchform.html
.. _converted to WordPress by an Instantbird contributor: https://blog.instantbird.org/2011/10/weekly-meeting-october-10-2011/
.. _WordPress importer: https://docs.getpelican.com/en/3.7.1/importer.html
.. _Jinja2: https://jinja.palletsprojects.com/
.. _added the missing files manually: https://github.com/instantbird/blog.instantbird.org/commit/d94b2fc4bd8d45d993c080daf215dbdd91298ae3
.. _custom archive plugin: https://github.com/instantbird/blog.instantbird.org/blob/source/plugins/archives.py
.. _pelican_comment_system plugin: https://github.com/getpelican/pelican-plugins/tree/master/pelican_comment_system
.. _writing a custom script: https://github.com/instantbird/blog.instantbird.org/blob/source/wp2comments.py
.. _pelican_import: https://github.com/getpelican/pelican/blob/4.2.0/pelican/tools/pelican_import.py
.. _combine it and the gravatar plugin: https://github.com/instantbird/blog.instantbird.org/blob/source/plugins/comments.py
.. _tag cloud: https://github.com/instantbird/blog.instantbird.org/blob/source/plugins/tag_cloud.py
.. _most used categories: https://github.com/instantbird/blog.instantbird.org/blob/source/plugins/most_used_categories.py
.. _interesting: https://blog.instantbird.org/2011/06/introducing-time-bubbles/
.. _articles: https://blog.instantbird.org/2013/07/first-milestone-of-the-awesometab-has-landed/
.. _design: https://blog.instantbird.org/2012/08/tab-completion-in-instantbird-1-2/
.. _decisions: https://blog.instantbird.org/2011/06/introducing-magic-copy/
.. _Internet Archive: https://archive.org/
