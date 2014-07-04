GSoc Lessons: Part Deux: The Arms Race
######################################
:date: 2013-12-04 13:17
:author: Patrick Cloke
:tags: community, GSoC, Mozilla
:slug: gsoc-lessons-part-deux-arms-race

This post title might be a little excessive, but I'll blame `The Sum
of All Fears`_ that I was watching last night. This is the second part
of a set of posts about ideas I heard at the Google Summer of Code 2013
Mentor Summit (you can read `the first part about the application
process`_).

This will explore an interesting anecdote I heard about the
interaction between applicants from another organization that, on
reflection, seemed to resonate somewhat with what I had seen in my
corner of the Mozilla community.

The organization these students were applying to required patches to
be fixed for a student's application to be accepted (as discussed in my
previous post). For a particular project there existed multiple highly
motivated and skilled students, but only one slot. Thus, a "patch race"
of sorts occurred where the students competed by continually providing
more patches that were increasingly complex. (Note that this wasn't a in
response to a challenge from community members, it was a spontaneous
situation.) Once a single student started to submit extra patches the
other students felt they must also submit more patches to be considered
equal/superior (hence my allusion to an "`arms race`_\ ").
Interestingly, they would also sometimes work on the same bug in a sort
of race to see who could fix it first.

There's a couple things I took away from this:

#. Great, the project just had a lot of things fixed!
#. The students were investing escalating amounts of time *during the
   application phase*.
#. The students were not working in an open manner.

I won't really expand much more about the first point, it's always
good to fix things.

Although submitting patches might showcase a student's skill, it also
relates to how much time the student is willing and able to put into the
application period. This, in particular, matters since different areas
of the world end their school year at different times. A student that
has already finished his semester during the application period may have
a lot of free time to attempt to get a GSoC slot (but will most likely
not have as much time during the actual summer!) This something that
mentors should keep in mind while reviewing applications.

A downside of increasing amounts of time invested is that the
rejection is that much harder for both the mentor (especially if the
student is now part of the community!), as well as for the student who
has now vested a large amount of time in the project.

The realization that actually upset me, however, is that these
students were not working in an open manner! Instead of collaborating,
they were competing! To me, this would set off a very poor tone for the
rest of GSoC. In fact, one of the biggest challenges I've had with GSoC
students is getting them to work in the open (i.e. "show me the code",
anyone in `#instantbird`_ is probably tired of hearing me say that).

At this point you *might* think this is a hypothetical case I made up!
Upon letting it sink in and reflecting on it...I realized I had actually
seen similar situations during the application periods I've been
involved with. This year, we found a bug in Instantbird's IRC code (CTCP
quoting and dequoting); after referencing some `specifications`_, I was
pretty quickly able to figure out the vague areas where people should
look for a fix. A couple of GSoC students in the room started looking
into it and exhibited a greatly reduced form of the behavior I discussed
above. The students were sharing information, but were not comfortable
sharing code. Unfortunately, this led to some very vague questions which
I was unable to answer (or answered incorrectly) and led to me coining
my catchphrase from above.

I by no means think this reflects poorly on our students! I think this
is some what natural and expected for most students unfamiliar with open
development. (Extrapolating from my experiences in school...) Students
generally work individually (or in small groups) on projects and are
directly competing for grades (at least if the course is graded on a
curve). This would foster a sense of competition as opposed to
cooperation! Luckily the students working with us understood (with very
little prompting, I might add!) that we'd prefer they work together and
help each other. We were able to successfully fix the dequoting bug
(which then caused a bug in the quoting code to be visible...sigh...).

My **short take away** from all this: remember that students are not
yet a community and they're competing with each other until they've been
accepted. (And that they're used to competing, e.g. homework and exams,
not collaborating!) I don't really know whether I feel the above
situation is good or bad, but it's certainly an interesting effect from
the way the GSoC process works.

.. _The Sum of All Fears: http://en.wikipedia.org/wiki/The_Sum_of_All_Fears_%28film%29
.. _the first part about the application process: {filename}/gsoc-lessons-part-1-application-period.rst
.. _arms race: http://en.wikipedia.org/wiki/Arms_race#Nuclear_arms_race
.. _#instantbird: irc://irc.mozilla.org/#instantbird
.. _specifications: {filename}/the-so-called-irc-specifications.rst
