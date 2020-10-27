New Blog
########
:date: 2014-07-03 23:04
:modified: 2014-07-06 18:24
:tags: blog, pelican

.. contents::

If you're reading this you might have noticed that I have a shiny new blog! I
had been pretty disappointed in Blogger_ practically since I started using it.
But it was free, I was a poor college student, etc. I finally managed to get
myself a `domain name`_ and set up a more proper blog!

I was between a few different pieces of blog software (namely WordPress_,
DotClear_ and Jekyll_) and couldn't really decide. I loved the idea of the
simplicity of Jekyll, but it's Ruby_. (Who's got time for that?) I wanted
something I could read the code of and understand if necessary. (And it has
been necessary!) My main requirements for blog software were:

* Easy to use and set up.
* Free.
* Support for syntax highlighted code blocks. (This was the only "hard" one to
  come by.)
* Support for RSS_ feeds.

After a quick Google search for "`jekyll python`_", I ended up on Hyde_. It
seemed alright, but no one seemed to use it. Farther down the page I came across
`a blog`_ talking about moving to Pelican_. I was hooked. (Note that I don't
necessarily agree with all the ideas in that post, it just introduced me to
Pelican.)

Set up Pelican
==============

(Since I dislike writing my own descriptions:)

    "Pelican is a static site generator, written in Python_, that requires no
    database or server-side logic."

Cool! Sounds real simple to use! And it was. Mostly.

I pretty much followed the quickstart_:

.. code-block:: bash

    mkdir -p blog/blog # The first blog is to store other repos, etc.
    cd blog/blog
    git init && git checkout -b source # Explained later on.
    brew install pandoc # If you're not on Mac you'll need to do something else.
    mkvirtualenv blog
    pip install pelican markdown Fabric ghp_import feedparser
    pelican-quickstart

I'll let you read the rest of the quickstart guide, but it was super quick to
get up and running! (I also referenced another `blog post`_ I found that had some
good information!) I, of course, had no content...but wait I did, it was just
in Blogger!

Importing Content from Blogger
==============================

Pelican does not directly support importing from Blogger (*Edit: Seems someone
just put up a `pull request`_ to support Blogger natively!*), but it supports
`importing from a RSS feed`_. The first time I did this it missed a couple of
articles (which I didn't notice right away), so make sure you bump up the max
amount in the URL like so (this also outputs in the folder "content"):

.. code-block:: bash

    pelican-import --feed http://clokep.blogspot.com/feeds/posts/default\?alt\=rss\&max-results\=240 -o content

No import is ever perfect and I had to clean up a bunch of stuff by hand
including:

* The slugs did not match the ones from Blogger (this is important later on!)
* Some of the dates were strangely wrong
* Some HTML formatting was included (in particular around <code>/<pre> blocks I
  had added).
* Some formatting was messed up.
* The (single) image I had on my blog had to be manually downloaded and added.
* I had bolded things I really wanted to be headers. (This is my fault!)

I probably spent a couple of hours cleaning all the reStructuredText content up,
but now I feel that I have a portable set of all of my blog posts, which I'm
pretty happy about!

Customizing Pelican
===================

I tried a few different themes for Pelican, but eventually settled on just using
and modifying the default theme. I, frankly, haven't tried it on too many
different systems, so hopefully it doesn't totally break on small screen sizes
or something. I'm not HTML expert, so I'd rather talk about the other stuff I
modified. (Although, if you're curious, the main elements I *did* modify are
adding the sidebar to the left and the organization of the archives page.)

Blogger has a concept of "labels", Pelican has a concept of "category" and
"tags". I *hate* this. What's the difference? Anyway, I wanted to eradicate the
concept of a "category" (and "authors" since I'm the only one on my blog!), so I
added a few things to my pelicanconf.py:

.. code-block:: python

    # Disable categories.
    DISPLAY_CATEGORIES_ON_MENU = False
    DISPLAY_CATEGORY_ON_ARTICLE = False
    CATEGORY_FEED_ATOM = None
    CATEGORY_SAVE_AS = ''
    CATEGORIES_SAVE_AS = ''

    # Disable author pages.
    AUTHOR_SAVE_AS = ''
    AUTHORS_SAVE_AS = ''

Note that ``DISPLAY_CATEGORY_ON_ARTICLE`` is actually a variable I added and
used in the template to not show categories above the list of tags on each
article.

This is getting pretty long so I'll leave how I'm actually serving this content
to my next article!

.. _Blogger: https://www.blogger.com/
.. _domain name: http://patrick.cloke.us
.. _WordPress: https://wordpress.com/
.. _DotClear: http://dotclear.org/
.. _Jekyll: http://jekyllrb.com/
.. _Ruby: http://www.ruby-lang.org/
.. _jekyll python: https://www.google.com/search?q=jekyll+python
.. _RSS: https://en.wikipedia.org/wiki/RSS
.. _Hyde: https://hyde.github.io/
.. _a blog: http://arunrocks.com/moving-blogs-to-pelican/
.. _Pelican: http://getpelican.com/
.. _Python: http://www.python.org/
.. _quickstart: http://docs.getpelican.com/en/3.4.0/quickstart.html
.. _blog post: http://terriyu.info/blog/posts/2013/07/pelican-setup/
.. _pull request: https://github.com/getpelican/pelican/pull/1390
.. _importing from a RSS feed: http://docs.getpelican.com/en/3.4.0/importer.html
