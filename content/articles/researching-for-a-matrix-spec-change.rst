Researching for a Matrix Spec Change
####################################
:date: 2023-01-12 15:24
:author: Patrick Cloke
:tags: matrix

The `Matrix protocol`_ is modified via `Matrix Spec Changes`_ (frequently abbreviated
to "MSCs"). These are short documents describing any technical changes and why they
are worth making (see `an example`_). I've `written a bunch`_ and wanted to
document my research process. [#]_

.. note::

  I treat my research as a *living document*, not an *artifact*. Thus, I don't worry
  much about the format. The important part is to start writing everything down
  to have a single source of truth that can be shared with others.

First, I write out a **problem statement**: what am I trying to solve? (This step
might seem obvious, but it is useful to frame the technical changes in why
they matter. Many proposals seem to skip this step.) Most of my work tends to be
from the point of view of an end-user, but some changes are purely technical. Regardless,
there is benefit from a shared written context of the issue to be solved.

From the above and prior knowledge, I list any **open questions** (which I update
through this process). I'll augment the questions with answers I find in my research,
write new ones about things I don't understand, or remove them as they become irrelevant.

Next, I begin collecting any previous work done in this area, including:

* What is the **current specification** related to this? I usually pull out blurbs
  (with links back to the source) from `the latest specification`_.
* Are there any |related known issues|_? It is also worth checking the issue
  trackers of projects: I start with the `Synapse`_, `Element Meta`_, and
  `Element Web`_ repositories.
* Are there **related outstanding MSCs** or **previous research**? I search the
  `matrix-spec-proposals`_ repository for keywords, open anything that looks
  vaguely related and then crawl those for mentions of other MSCs. I'll document
  the related ones with links and a brief description of the proposed change.

  I include both proposed and closed MSCs to check for previously rejected ideas.
* Are others interested in this? Have others had conversation about it? I roughly
  follow the `#matrix-spec`_ room or search for rooms that might be interested in
  the topic. I would recommend joining the `#matrix-spec`_ room for brainstorming
  and searching.

  This step can help uncover any missed known issues and MSCs. I will also ask
  others with a longer history in the project if I am missing anything.
* A brief **competitive analysis** is performed. Information can be gleaned from
  technical blog posts and API documentation. I consider not just competing
  *products*, but also investigate if others have solved similar *technical*
  problems. Other protocols are worth checking (e.g. IRC, XMPP, IMAP).

You can see an example of my research on `Matrix read receipts & notifications`_.

Once I have compiled the above information, I jump into the **current implementation**
to ensure it roughly matches the specification. [#]_ I start considering what
protocol changes would solve the problem and are reasonable to implement. I find
it useful to write down all of my ideas, not just the one I think is best. [#]_

At this point I have:

* A problem statement
* A bunch of background about the current protocol, other proposed solutions, etc.
* A list of open questions
* Rough ideas for proposed solutions

The next step is to iterate with my colleagues: answer any open questions, check
that our product goals will be met, and seek agreement that we are designing a
buildable solution. [#]_

*Finally*, I take the above and formalize it in into one or more Matrix Spec Changes.
At this point I'll think about error conditions / responses, backwards compatibility,
security concerns, and any other parts of the full MSC. Once it is documented, I
make a pull request with the proposal and self-review it for loose ends and clarity.
I leave comments for any parts I am unsure about or want to open discussion on.

Then I ask me colleagues to read through it and wait for feedback from both them and
any interested community members. It can be useful to be in the `#matrix-spec`_ room
as folks might want to discuss the proposal.

.. [#] There's a useful `proposal template`_ that I eventually use, but I do much
       of this process before constraining myself by that.

.. [#] This consists of looking through code as well as just trying it out by
       manually making API calls or understanding how APIs power product features.

.. [#] Part of the MSC proposal is documenting alternatives (and why you didn't
       choose one of those). It is useful to brainstorm early before you're set
       in a decision!

.. [#] I usually do work with Matrix homeservers and am not as experienced with
       clients. It is useful to bounce ideas off a client developer to understand
       their needs.

.. _Matrix protocol: https://spec.matrix.org/
.. _Matrix Spec Changes: https://spec.matrix.org/proposals/
.. _an example: https://github.com/matrix-org/matrix-spec-proposals/pull/2457
.. _written a bunch: https://github.com/matrix-org/matrix-spec-proposals/pulls?q=is%3Apr+author%3Aclokep+label%3Aproposal
.. _the latest specification: https://spec.matrix.org/v1.5/client-server-api/
.. |related known issues| replace:: **related known issues**
.. _related known issues: https://github.com/matrix-org/matrix-spec/issues
.. _Synapse: https://github.com/matrix-org/synapse
.. _Element Meta: https://github.com/vector-im/element-meta
.. _Element Web: https://github.com/vector-im/element-web
.. _#matrix-spec: https://matrix.to/#/#matrix-spec:matrix.org
.. _matrix-spec-proposals: https://github.com/matrix-org/matrix-spec-proposals/
.. _Matrix read receipts & notifications: {filename}/articles/matrix-read-receipts-and-notifications.md


.. _proposal template: https://github.com/matrix-org/matrix-spec-proposals/blob/9b3f01b0193caa1e1c563cfc861ab021bcddcb2c/proposals/0000-proposal-template.md
