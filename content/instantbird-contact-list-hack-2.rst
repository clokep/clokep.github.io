Instantbird Contact List Hack #2
################################
:date: 2012-01-15 10:00
:author: Patrick Cloke
:tags: customizing, Instantbird, programming
:slug: instantbird-contact-list-hack-2

There was a \ `request`_ on the Instantbird Bugzilla to always show
contacts in the contact list as the "big" contact (as shown when a
contact is selected).  Similarly to my `last post`_, this can easily be
done with userChrome.css.  See the post if you don't know what
userChrome.css is.

Again, we're simply going to always apply a specific CSS style to the
contacts, namely we'll be modifying the behavior of `blist.css`_.  I'm
sure you don't really care about that and just want the code, well I'll
oblige:

.. code-block:: javascript

    /* Expand all contacts to the big contact. */
    contact {
        -moz-binding: url("chrome://instantbird/content/contact.xml#contact-big") !important;
        -moz-box-orient: vertical !important;
        -moz-box-align: stretch !important;
    }

And that's it!  Restart Instantbird and you should always have big
contacts.  I haven't seen any issues of using this (missing or wrong
behavior), but of course your mileage might vary.  Have fun!

.. _request: https://bugzilla.instantbird.org/show_bug.cgi?id=987
.. _last post: {filename}/instantbird-contact-list-hack.rst
.. _blist.css: http://lxr.instantbird.org/instantbird/source/instantbird/content/blist.css#38
