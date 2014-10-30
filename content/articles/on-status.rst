On Status
#########
:date: 2012-10-16 21:33
:author: Patrick Cloke
:tags: chat, instant messaging, Instantbird, messaging, status, Thunderbird
:slug: on-status

Something that comes up often about Instantbird is why we only support
three statuses: Available, Unavailable and Offline.  (We do actually
support a fourth one too, Idle, but that is set automatically, not
chosen by the user.)  Frequently this discussion is in the context of
wanting an "Invisible" status, but I'll get to that later...

Many users have talked to us on IRC, email or via bugs and complained
about wanting an "Away" status or a "Do Not Disturb" status.  There's a
few issues with this:

#. What's really the difference between "Unavailable", "Away" and "Do
   Not Disturb"?  Do you really need to choose them individually? 
   (Other things that fit into here: "Not at my desk", "on the phone",
   "busy", "stepped out".  It is amazing how some protocols have so many
   ways to describe being unavailable!)
#. A technical issue that we often run into is trying to shoehorn
   different protocol implementations into our abstract protocol
   interface.  (We already have some fairly complicated interfaces
   around joining chat rooms, creating different account, etc. because
   of this.)
#. Setting yourself as "Away" or "Invisible" is a lie.  Perhaps this is
   me being overly idealistic, but why would you set yourself as
   "Away"?  It seems that this is something that should be done
   automatically (when you lock your display, perhaps?).  You can't be
   "Away" and using your computer at the same time!
   Again, perhaps being idealistic, but what is the point of the
   "Invisible" status?  If you wish to be hidden from someone
   (everyone?) why not just block those users.  Or ignore them when they
   send you a message.  If you are busy, set yourself to "Unavailable"
   and people should understand that they should not talk to you...if
   they don't, well...do you really want them talking to you ever?  (Are
   they really your friend?  I guess you don't get to choose your
   co-workers, but still.)  Now, perhaps this is just my opinion as
   being someone who never really hard an "Invisible" status (I actually
   remember it being added to the AIM client at some point).

At this point you probably don't believe me that there's really *that*
many different protocol statuses out there, so I figured I'd illustrate
a few protocols in a matrix.  Note that this isn't meant to be
exhaustive, just to show how complicated of a situation this really is. 
All protocols can obviously be "offline" as well, but that's not shown
in the table.

+-------------------------+-----------+------------------+--------------+----------------+
|                         | Available | Unavailable      | Phone        | Invisible      |
+=========================+===========+==================+==============+================+
| Oscar (AIM/ICQ)         | Online    | Away             |              | Invisible      |
+-------------------------+-----------+------------------+--------------+----------------+
| IRC                     | Online    | Away             |              |                |
+-------------------------+-----------+------------------+--------------+----------------+
| Microsoft Lync          | Online    | * Busy           | In a call    |                |
|                         |           | * Away           |              |                |
|                         |           | * In a meeting   |              |                |
+-------------------------+-----------+------------------+--------------+----------------+
| Yahoo! Messenger        | Available | * Busy           | On the phone |                |
|                         |           | * Stepped out    |              |                |
|                         |           | * Be right back  |              |                |
|                         |           | * Not at my desk |              |                |
+-------------------------+-----------+------------------+--------------+----------------+
| Windows Live Messenger  | Online    | * Busy           | On the phone | Appear offline |
|                         |           | * Away           |              |                |
|                         |           | * Be Right Back  |              |                |
|                         |           | * Out to lunch   |              |                |
+-------------------------+-----------+------------------+--------------+----------------+
| XMPP (e.g. Google Talk) | Available | Busy             |              |                |
+-------------------------+-----------+------------------+--------------+----------------+
