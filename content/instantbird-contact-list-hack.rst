Instantbird Contact List Hack
#############################
:date: 2011-11-01 00:20
:author: Patrick Cloke
:category: Mozilla
:tags: customizing, Instantbird, programming
:slug: instantbird-contact-list-hack

A friend of mine asked me if there was a way to have selected contacts
in the contact list NOT expand to two lines (where the status goes onto
the second line) in Instantbird.

There's actually no option to do this in Instantbird, but with a
little `userChrome`_ tweak, we can easily get this behavior (although
with a couple caveats).  You should be able to add a new folder `inside
your profile`_ called chrome.  Inside of this make a new file called
userChrome.css and place the following:

.. code-block:: css

    #buddylistbox:focus > contact[selected] {
        -moz-binding: url("chrome://instantbird/content/contact.xml#contact") !important;
        -moz-box-orient: horizontal !important;
    }

Save the file and restart...and that's it! Now your selected contacts
should be on one line, just like your unselected contacts.

I did mention there was a caveat though! If you want to expand a
contact (to see all the protocols, etc. that you've merged together)
you'll need to use the arrow keys: right arrow expands a contact, left
arrow collapses a contact.  (You need to do this since the chevron icon
that lets you expand/collapse isn't shown on a non-selected contact.)

(Some more technical details: we're forcing the standard contact
template to be used instead of the contact-big template, even when the
contact is expanded; i.e. we're overwriting the command given
`blist.css`_.)

.. _userChrome: http://www-archive.mozilla.org/unix/customizing.html
.. _inside your profile: http://instantbird.com/faq.html#profilefolder
.. _blist.css: http://lxr.instantbird.org/instantbird/source/instantbird/content/blist.css#44
