New Blog: Serving the Content
#############################
:date: 2099-08-01 12:03
:tags: blog

.. contents::

In the `first part`_ of this blog post I talked about using Pelican to create a
blog, this is a bit more about how I got it up and running.

Getting a Domain
================

The most exciting part! Getting a domain! I used `gandi.net`_, it was
recommended to me by Florian as "awesome, but a bit expensive". I liked that
they actually said *exactly* what I was getting by registering a domain through
them. Nowhere else I looked was this explicit.

Once you get your domain you'll need to set up your CNAME_ record to forward to
wherever you're serving your content. I found it pretty interesting that gandi
essentially gives you an `DNS zone`_ file to modify. I ended up making a few
modifications:

* Created a patrick subdomain (patrick.cloke.us)
* Redirected the apex domain (cloke.us) to the patrick subdomain
* Redirected the www subdomain to the patrick subdomain

I also created a few email aliases which forward to the email accounts I already
own.

Serving the Content
===================

OK, we have a domain! We have content! How do we actually link them!? I used
`GitHub Pages`_, cause I'm cheap and don't like to pay for things. The quick
version:

* Create a repository that is named ``<your account name>.github.io``
* Push whatever HTML content you want into the master branch
* Voila it's available as <your account name>.github.io

Personally, I store my Pelican code in a separate source_ branch [#]_ and use
ghp-import_ to actually publish my content. I've automated a lot of the tasks by
extend the default `fabfile.py`_ that is generated with the quickstart. My workflow
looks something like:

.. code-block:: bash

    komodo content/new-article.rst
    # <edit article>
    # <check it out in a browser using fab build/serve/regenerate>
    git add content/ && git commit -m "Add 'New Article!'."
    fab publish # Which runs "ghp-import -p -b master output" underneath!
    git push origin source

One other thing you'll need to do is add a CNAME file that has the domain of
your host in it (and only the domain). I found the GitHub documents on this
extremely confusing, but it's pretty simple:

* Create a file called CNAME somewhere you have static files in Pelican (mine is
  at content/static/CNAME)
* Add a line to your pelicanconf.py to have this file end up in the root:

.. code-block:: python

    # Set up static content and output locations.
    STATIC_PATHS = [
        'images',
        'static/CNAME'
    ]
    EXTRA_PATH_METADATA = {
        'static/CNAME': {'path': 'CNAME'},
    }

It took 10 - 20 minutes for this to "kick in" on GitHub, until that time I had a
404 GitHub page.

This is already getting pretty long so I'm going to leave the last part:
Redirecting Blogger content to a separate file.

Redirect Blogger
================

This is the really fun part. How the hell do we redirect blogger links to
actually go to the new location of each blog post? With some hackery, some luck,
and some magic.

I found some help in an article about `switching to WordPress from Blogger`_ and
modified the template they had there. On the Blogger dashboard, choose
"Template", scroll to the bottom and click "Revert to Classic Template". Then
use something like the following template:

.. code-block:: html

    <html>
        <head>
            <title><$BlogPageTitle$></title>
            <script>
                <MainOrArchivePage>
                    window.location.href = "http://patrick.cloke.us/";
                </MainOrArchivePage>
                <Blogger>
                    <ItemPage>
                        // This is the full permalink.
                        var permalink = "<$BlogItemPermalinkURL$>";
                        // Split up each part by the slash.
                        var parts = permalink.split("/");
                        // Take the last part (the page) and strip off the .html.
                        var slug = parts.slice(-1)[0].slice(0, -5);

                        var article = "http://patrick.cloke.us/posts/<BlogDateHeader><$BlogDateHeaderDate$></BlogDateHeader>/" + slug;
                        window.location.href = article;

                        window.onload = function() {
                            document.getElementById("linkrel").href = article;
                            document.getElementById("simplelink").href = article;
                        }
                    </ItemPage>
                </Blogger>
            </script>
            <MainPage>
                <link rel="canonical" href="http://patrick.cloke.us/" />
            </MainPage>
            <Blogger>
                <ItemPage>
                    <link id="linkrel" rel="canonical" />
                </ItemPage>
            </Blogger>
        </head>
        <body>
            <MainOrArchivePage>
            <h1><a href="http://patrick.cloke.us"><$BlogTitle$></a></h1>
            </MainOrArchivePage>
            <Blogger>
                <ItemPage>
                    <h1>
                        <a id="simplelink">
                            <$BlogItemTitle$>
                        </a>
                    </h1>
                    <$BlogItemBody$>
                </ItemPage>
            </Blogger>
        </body>
    </html>

Obviously you'll need to change the URLs, but the key parts here are that we're
generating a URL based on the date and the full article name. The magic comes in
generating the date. The get it in the format I wanted (YYYY/MM/DD) I modified a
the "Date Header Format" in "Settings" > "Language and formatting". This matches
how I formatted my URLs in my pelicanconf.py. The ``slug`` that gets generated
needs to match the slug you used in your template so the link will work. (I had
some_ help_ in figuring out these template tags.)

I'd suggest you check the links to all your articles! A couple of the dates were
messed up in mine (so the day was off by way, but I had a broken link).

The last thing to do is to redirect the Atom/RSS feed (if anyone is using that).
Go to "Settings" > "Other" > "Post Feed Redirect URL" and set it to your new
Atom feed URL (wherever that might be).

.. [#] Pro-tip: You can change the "default" branch of your repository in the
       settings page on GitHub.

.. _first part: {filename}/new-blog.rst
.. _gandi.net: https://www.gandi.net/
.. _CNAME: https://en.wikipedia.org/wiki/CNAME
.. _DNS zone: https://en.wikipedia.org/wiki/DNS_zone
.. _GitHub Pages: https://pages.github.com/
.. _source: https://github.com/clokep/clokep.github.io
.. _ghp-import: https://github.com/davisp/ghp-import
.. _fabfile.py: http://www.fabfile.org/
.. _switching to WordPress from Blogger: http://www.labnol.org/internet/switch-from-blogger-to-wordpress/9707/
.. _some: https://support.google.com/blogger/answer/42095
.. _help: http://www.elizabethcastro.com/blogvqj/extras/templatetags.html
