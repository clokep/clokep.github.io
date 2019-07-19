Thoughts on Applying to Google Summer of Code
#############################################
:date: 2016-03-07 09:18
:author: Patrick Cloke
:tags: GSoC, Mozilla
:slug: thoughts-on-applying-to-gsoc

.. contents::

..

    Over the past few years I've been involved in `Google Summer of Code`_
    (GSoC), a program that sponsors students to write code for open-source
    projects, as part of Mozilla. I've been both a mentor and administrator,
    `Florian Quèze`_ and I frequently get asked questions about what students
    should do to apply to GSoC. This post aims to give some resources and
    answers to those questions. (I should note that each open-source
    organization is different and this is based on my experiences at Mozilla.
    Your mileage may vary.)

    Remember that none of this is meant as a guarantee for acceptance, it is
    just a few things that can help get you ready and improve your chances!

If you haven't heard yet, then Mozilla has been accepted into
`Google Summer of Code`_ (GSoC) 2016, this will be our 10th time participating
in GSoC mentoring Organizations. Overally, the best way to prepare yourself for
applying to GSoC is to get involved with the community you would like to work
with. Some particular resources to help you in applying to GSoC are:

1.  Go read the `Google Summer of Code`_ website. Every part of it. Particular
    pages to point out are the:

    *   `Student Guide`_: Written by a variety of people in the GSoC community,
        it covers topics from contacting an organization, to applying, to not
        being accepted.
    *   FAQ_: If you still have questions after reading the above (or whenever
        you have a question), check here for answers *before* asking anyone. (In
        particular this includes questions about how to apply.)
    *   The final important page to internalize is the schedule_. It is a
        student's responsibility to meet each of the deadlines.

2.  Mozilla has some good `application advice`_ on the idea page. I've
    included/expanded on this below:

    *   Talk to the mentor. Contact them on IRC/e-mail/Slack/whatever that
        project uses. If you have trouble contacting a mentor, contact the
        organization administrators.
    *   Read `How Not To Apply For Summer Of Code <http://blog.gerv.net/2006/05/how_not_to_apply_for_summer_of/>`_
        and avoid doing the things listed there.
    *   Read our examples of good applications:
        `1 <https://wiki.mozilla.org/SummerOfCode/SampleApplications/1>`_
        `2 <https://wiki.mozilla.org/SummerOfCode/SampleApplications/2>`_
        `3 <https://wiki.mozilla.org/SummerOfCode/SampleApplications/3>`_
    *   It is entirely acceptable to apply for 2 or 3 projects, if more than one
        catches your eye; if the applications are high quality, that can improve
        your chances. However, more than 3 seems like spam.
    *   Note that if a project suggests it would be helpful to know a technology
        you don't know (e.g. XUL), you may be able to get away with learning on
        the job. Don't be put off from applying if the project otherwise looks
        right for you.

Picking an Organization
=======================

Pick an organization you're truly interested in helping. I really can't stress
this enough. "Truly interested in helping" might mean many things:

*   You believe in an organization on a philosophical ground.
*   You use the program/library/service/etc. that the organization produces.
*   ...many other things...

Throughout this post I use "organization" and "community" synonymously, but
organizations likely have smaller communities within them, each with their own
culture, beliefs, etc. Even within a small community, members will not share all
the same opinions!

..

    A pet peeve of mine is that a student should use (or at the very least
    *try*) the product the community makes. It is difficult (if not impossible)
    to understand the needs and wants of a community without utilizing what
    they've poured their time and energy into.

Introductions
-------------

Different communities interact in different ways (and frequently a single
community interacts in multiple ways). Common ways include:

*   Instant messaging (IRC, XMPP, Slack, hipChat, etc.) for day-to-day chatter,
    help, and off-topic banter.
*   E-mail / mailing lists / newsgroups for project wide discussion,
    announcements, etc.
*   Bug trackers (Bugzilla, GitHub, Trac) for technical discussion and reviewing
    code.

Choose whichever way of introducting yourself that you're comfortable with. It
can be useful to "idle" before introducing yourself (i.e.  watch how a community
interacts).

This can be important to figuring out a communities culture, e.g. how friendly
is the community to new-comers? Are they open to helping or do they just expect
patches to be submitted? Remember that it's important for you to feel
comfortable with a community, you'll be spending a significant amount of time
interacting with them!

If none of the above seem appropriate, or you're unsure, contact the
organization administrator directly. I'd suggest asking pointed questions, as an
organization administrator is much more likely to respond quickly in that case.

Getting Accepted
================

We're frequently asked how a student can improve their chances of getting
accepted by an organization. GSoC is a very **self-driven** program, especially
if your mentor is a volunteer. Being a self starter can be a boon for being
accepted.

*   Find a project you're interested in doing and talk to the mentor / community
    responsible.
*   Ensure you have a development environment set-up (for example, make sure you
    can build Firefox, understand what needs to be done after making changes,
    etc.).
*   Figure out where resources are for the project (i.e. Where are technical
    discussions? Where can you find documentation?)
*   Find minor bugs related to the project you're interested in and work on
    fixing them. (This might be more difficult if your project would add an
    entirely new piece of code!)
*   Get used to the way the community works and functions.

Building an Application
-----------------------

The above should help feed into your application. In particular, it should help
to build a realistic schedule for your application. (Scheduling is difficult
even for seasoned engineers, but the above work should help make a more accurate
schedule.)

*   Develop a plan for splitting your work into discrete chunks that can be
    merged separately. Smaller changes are easier to review, can (generally)
    land faster, and are easier to test. Of course, each project is different,
    but work with your (potential) mentor.
*   Estimate the amount of work each part of the project will take (you'll have
    some experience in the code base already, leverage that).
*   Estimate how long reviews will take. (All code at Mozilla must go through a
    review process before it is merged into a product. You might even need
    multiple reviewers if your code touches many different parts of a codebase!
    Different people review code on different schedules, etc.)
*   Understand how quickly your changes would be merged and released. (How
    quickly will your code hit a larger audience?)
*   Understand the pieces **besides** code that you might be asked to do. Will
    you need to add/update documentation? Add new tests? Keep an old API intact?

Summary
=======

This is just a few ideas of what I look for when reviewing a Google Summer of
Code application. To repeat, try to understand an organization's members, get
involved and gain experience, try to build an accurate schedule. An additional
thing I'd like to add is to `respect your mentors time`_, especially for GSoC,
many mentors are volunteers! You'll likely be working on their project **more**
than they do during GSoC!

Please let me know if you have any additions or comments! If you have specific
questions that pertain to your application at Mozilla, please
`contact`_ me individually.

.. _Google Summer of Code: https://developers.google.com/open-source/gsoc/
.. _Florian Quèze: http://blog.queze.net/
.. _FAQ: https://developers.google.com/open-source/gsoc/faq
.. _Student Guide: http://en.flossmanuals.net/GSoCStudentGuide/
.. _schedule: https://summerofcode.withgoogle.com/how-it-works/
.. _application advice: https://wiki.mozilla.org/Community:SummerOfCode16#Application_Advice
.. _respect your mentors time: {filename}/articles/mentoring-and-time.rst
.. _contact: {filename}/pages/about.rst
