Boston Python: Twisted async networking framework
#################################################
:date: 2015-08-28 08:42
:author: Patrick Cloke
:tags: python, community, programming, twisted
:slug: boston-python-twisted-talk

Yesterday, `Stephen DiCato`_ and I gave a talk for `Boston Python`_ titled:
`Twisted async networking framework`_. It was an introduction to intermediate
level talk about using the `Twisted networking framework`_ based on our
experiences at `Percipient Networks`_.

The talk, available `on our GitHub`_ (`PDF`_) covered a few basic
topics:

#. What is asynchronous programming?
#. What is Twisted_?
#. When/why to use Twisted?
#. What is the event loop (reactor)?
#. What are `Deferreds`_ and how do you use them?
#. What are protocols (and related objects) and how do you use them?

Additionally there was a 'bonus' section: Using Twisted to build systems &
services.

We used an example of a very simple chat server (NetCatChat: where the official
client is netcat) to demonstrate these principles. All of our (working!) demo
code is included in the `repository`_.

There was a great turn out (almost 100 people showed up) and I greatly enjoyed
the experience. Thanks to everyone who came, the sponsors for the night,
`Boston Python`_ for setting this up, and Stephen for co-presenting! Please let
us know if you have any questions or comments.

.. _Stephen DiCato: http://stephendicato.com/
.. _Boston Python: http://www.meetup.com/bostonpython/
.. _Twisted async networking framework: http://www.meetup.com/bostonpython/events/221406450/
.. _Twisted networking framework: https://twistedmatrix.com/
.. _Percipient Networks: https://percipientnetworks.com/
.. _on our GitHub: https://github.com/percipient/talks/tree/master/boston_python_08_27_2015
.. _PDF: https://github.com/percipient/talks/raw/master/boston_python_08_27_2015/boston_python_08_27_2015.pdf
.. _Twisted: https://twistedmatrix.com/
.. _Deferreds: https://twistedmatrix.com/documents/current/core/howto/defer.html
.. _repository: https://github.com/percipient/talks/tree/master/boston_python_08_27_2015
