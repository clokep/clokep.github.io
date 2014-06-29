IRC Auto-Performs
#################
:date: 2012-06-11 02:25
:author: Patrick Cloke
:tags: Instantbird, IRC, Mozilla
:slug: irc-auto-performs

There have been a `few`_ `requests`_ to support "auto-performs"
(sending commands to the IRC server after connection that the user types
into a box or whatever). Personally I find this to be:

#. A fairly awful user experience.
#. Confusing to new users.
#. Unnecessary.

I additionally don't like this idea since it requires us to have
commands for all the common tasks you'd want to do in an auto-perform
(or support sending absolutely raw messages to the server, which we
actually do already in the /quote command). Essentially what I just
described is writing our own scripting language...that seems pointless
(and frankly, I have better things to do). I'm hoping to convince you
with this post (and maybe a series of posts) that auto-performs aren't
necessary and a trivial restartless extension can replace them.

Design
======

Part of the desire to `replace the libpurple IRC protocol plugin`_
with a new JavaScript one built specifically for Instantbird (which is
also now used in Thunderbird!) was to make the protocol fully
extensible. There are `many revisions and unofficial extensions to IRC`_
and we might not necessarily want to support them all (especially if
they only apply to a single network). Allowing all parts of the protocol
implementation to be touched and extended seemed like a great way to
handle this.

Initially I tried to do this by making the IRC account into an XPCOM
component (well it is one already, it's an prplIAccount, but I meant an
IRC specific one: implementing ircIAccount, if you will). Unfortunately,
this seemed to have a lot of overhead and got complicated extremely
quickly. Anything I'd want to touch from a message handler (wait,
wait...what's a handler?! I'll get back to that) would need to have
methods written and exposed to access internal data of the
account...does that sound very extensible to you? Well, it doesn't to
me...

Onto design two! (Well actually my first design...) Lots of JavaScript
objects! The entire protocol is implemented as a set of JavaScript
objects and the handlers directly touch and modify the account's data
(of course there's methods for abstraction, etc.). This means that an
extension has absolutely FULL access to every about an account...this
also means an extension could seriously mess with and cause the protocol
to stop working or do really crazy things, etc. Unfortunately there
isn't really a way to avoid that. Hopefully people write good code.

Messages
========

I'm going to go into an aside about messages right now, even though it
doesn't quite seem relevent yet. It will. IRC has a bunch of
sub-protocols embedded within the IRC protocol (see the link above about
unofficial extensions). We attempt to parse all the string messages and
make pretty JavaScript objects out of them. I've actually identified
five (yes, count that: five) different sub-"protocols" within IRC that
we deal:

#. IRC itself (i.e. `RFC 1459`_ / `RFC 2812`_ / various numeric
   extensions)
#. `CTCP (the Client-to-Client Protocol)`_,embedded in PRIVMSG commands
   of IRC
#. DCC (Direct Client-to-Client), a subprotocol of CTCP
#. `ISUPPORT`_ (also known as Numeric 005), a method of negotiating
   capabilities between a client and server
#. And finally, handling of IRC Services (there's a lot of them and no
   specification, but we treat them specially)

Briefly what happens when we receive a raw message over the wire, we
create an `ircMessage object out of it using a variety of regular
expressions`_. This object has a variety of fields (see the link for
details), including the command, who sent the message and the
parameters.

If the message is identified as a CTCP message, we then morph the
ircMessage into a `CTCPMessage`_, which can be morphed into a
`DCCMessage`_. Additionally, a 005 reply can be parsed into a
`isupportMessage`_. And last, but not least, a received PRIVMSG can also
be parsed into a `ServiceMessage`_. Each of these extends the IRC
message without destroying information. (Yes, I'm realizing now that my
choice of whether to use capitals is all messed up...)

Well, why do we care...? By preparsing the strings into objects (as
defined by any "specifications" that exist), we keep extensions from
having to parse messages over and over again from strings.

Handlers
========

A handler is simply what I call the object that contains the methods
to deal with an incoming message. Pretty much, you get to say "Only send
me ISUPPORT messages!" or "Only send me CTCP messages!" and voila, you
only get that type of message. Each message type has a field that is
used to choose the method to run (for the IRC messages, the "command",
for CTCP the "CTCP command", ISUPPORT the "parameter", etc.) This sounds
a lot more complicated than it is, I think a brief `example`_ is in
order:

.. code-block:: javascript

    var ircSimpleExample = {
      // The name here is really only used in error messages.
      name: "IRC Simple Example",
      // Slightly above the default priority so we run before the main IRC handler.
      priority: ircHandlers.DEFAULT_PRIORITY + 10,
      // Run this for all accounts (note that the 'this' object in this method is
      // the JavaScript account object.
      isEnabled: function() true,

      // The commands we want to handle. For each of these, the account object is
      // bound to 'this' and the single parameter is of the type that you've
      // registered your handle.
      commands: {
        "001": function(aMessage) {
          // At the 001 response we've successfully connected to the server.
          // Send an IDENTIFY command to NickServ.
          this.sendMessage("PRIVMSG", ["NickServ", "IDENTIFY <your password>"]);

          // Return false so the default handler still runs.
          return false;
        }
      }
    }

Just like that we've designed a handler! Whenever the 001 method is
received from the server, this function will run and attempt to identify
with the NickServ (of course this could use a bit more security on it,
but it's to demonstrate the possibilities). (The sendMessage function
takes the command to send and an array of parameters to send.)

As this is already a long post, I think I'll cut this off now and
continue this at another time, but I hope I'm beginning to convince you
that allowing directy access to the account and protocol implementation
is a more powerful (and even simpler in many ways, in my opinion)
alternative to "auto-performs". The one major downside I see to this, is
that it requires a bit more understanding of the actual protocol level
implementation, I don't feel that knowing you need to use "PRIVMSG" as a
command instead of /msg is a huge issue, however.

.. _few: https://bugzilla.mozilla.org/show_bug.cgi?id=742675
.. _requests: https://bugzilla.instantbird.org/show_bug.cgi?id=1101
.. _replace the libpurple IRC protocol plugin: {filename}/why-rewrite-the-irc-protocol-plugin-part-2.rst
.. _many revisions and unofficial extensions to IRC: {filename}/the-so-called-irc-specifications.rst
.. _RFC 1459: http://tools.ietf.org/html/rfc1459
.. _RFC 2812: http://tools.ietf.org/html/rfc2812
.. _CTCP (the Client-to-Client Protocol): http://www.irchelp.org/irchelp/rfc/ctcpspec.html
.. _ISUPPORT: http://tools.ietf.org/html/draft-brocklesby-irc-isupport-03
.. _ircMessage object out of it using a variety of regular expressions: http://hg.instantbird.org/instantbird/file/b8d8b6e60aef/chat/protocols/irc/irc.js#l14
.. _CTCPMessage: http://hg.instantbird.org/instantbird/file/b8d8b6e60aef/chat/protocols/irc/ircCTCP.jsm#l44
.. _DCCMessage: http://hg.instantbird.org/instantbird/file/b8d8b6e60aef/chat/protocols/irc/ircDCC.jsm#l20
.. _isupportMessage: http://hg.instantbird.org/instantbird/file/b8d8b6e60aef/chat/protocols/irc/ircISUPPORT.jsm#l22
.. _ServiceMessage: http://hg.instantbird.org/instantbird/file/b8d8b6e60aef/chat/protocols/irc/ircServices.jsm#l19
.. _example: https://bitbucket.org/clokep/irc-extras/src/6f778f17172a/example/bootstrap.js
