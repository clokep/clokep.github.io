Adding an Auxiliary Audio Input to a 2005 Subaru Outback
########################################################
:date: 2014-08-30 17:34
:author: Patrick Cloke
:tags: hacking, auto, hardware

I own a `2005 (fourth generation) Subaru Outback`_, I've had it since the fall
of 2006 and it has been great. I have a little over 100,000 miles and do not
plan to sell it anytime soon.

There is one thing that just *kills* me though. You cannot (easily [#]_) change
the radio in it...and it is *just* old enough [#]_ to have neither BlueTooth nor
an auxiliary audio input. I've been carrying around a book of CDs with me for
the past 8 years. I decided it was time to change that.

I knew that it was possible to "modify" the radio to accept an auxiliary input,
but it `involved always playing a silent CD`_, which I did not find adequate. I
recently `came across`_ a post of how to do this in such a way that the radio
functions as normal, but when you plug in a device to the auxiliary port it cuts
out the radio and plays from the device. `Someone else`_ had also confirmed that
it worked for them. Cool!

I vaguely followed the directions, but made a few changes here and there. Also,
everyone online seems to make it seem like the radio is *super* easy to get
out...I seriously think I spent at least two hours on it. There were two_
videos_ and a PDF_ I found useful for this task.

.. center::

    .. image:: /thumbnails/subaru-outback-radio/uninstall-front_small.jpg
        :target: {static}/images/subaru-outback-radio/uninstall-front.jpg
        :alt: Front view of my uninstalled 2005 Subaru Outback stereo.

    .. image:: /thumbnails/subaru-outback-radio/uninstall-right_small.jpg
        :target: {static}/images/subaru-outback-radio/uninstall-right.jpg
        :alt: Right view of my uninstalled 2005 Subaru Outback stereo.

    .. image:: /thumbnails/subaru-outback-radio/uninstall-back_small.jpg
        :target: {static}/images/subaru-outback-radio/uninstall-back.jpg
        :alt: Back view of my uninstalled 2005 Subaru Outback stereo.

    A few images of the uninstalled stereo before any disassembly. (So I could
    remember how to reassemble it!)

I wouldn't say that this modification was extremely difficult, but it does
involve:

* Soldering to surface mount components (I'm not awesome a soldering, but I have
  had a good amount of experience).
* The willingness to potentially trash a radio.
* Basic understanding of electrical diagrams and how switches work.
* A lot of time! I spent ~13 hours total working on this.

Total cost of components, however, was < $5.00 (and that's probably
overestimating.) Really the only component I didn't have was the `switching
audio jack`_, which I got at my local RadioShack for $2.99. (I also picked up
wire, heatshrink, etc. so...$5.00 sounded reasonable.) The actual list of parts
and tools I used was:

* 1/8" Stereo Panel-Mount Phone Jack [$2.99, RadioShack #274-246]
* ~2 feet of each of green and red 22 gauge wire, ~1 foot of black 22 gauge
  wire.
* Soldering iron / Solder
* 3 x Alligator clip testing wires (1 black, 1 red, 1 green)
* Multimeter
* Hot glue gun / Hot glue
* Various sizes of flat/slotted and Phillips head screw drivers
* `Wire strippers`_
* Wire cutter
* Needle nosed pliers
* Flashlight_
* Drill with 1/4" drill bit and a 1/2" spade bit (plus some smaller sized drill
  bits for pilot holes)

Anyway, once you have the radio out you can disassemble it down to it's bare
components. (It is held together with a bunch of screws and tabs, I took
pictures along each step of the way to ensure I could put it back together.)

.. center::

    .. image:: /thumbnails/subaru-outback-radio/disassembly-front_small.jpg
        :target: {static}/images/subaru-outback-radio/disassembly-front.jpg
        :alt: The front of the stereo after removing the control unit.

    .. image:: /thumbnails/subaru-outback-radio/disassembly-front-reverse_small.jpg
        :target: {static}/images/subaru-outback-radio/disassembly-front-reverse.jpg
        :alt: The reverse of the control unit.

    .. image:: /thumbnails/subaru-outback-radio/disassembly-top_small.jpg
        :target: {static}/images/subaru-outback-radio/disassembly-top.jpg
        :alt: The top of the unit with the cover removed showing the CD drive.

    The initial steps of disassembly: the front after removing the controls, the
    reverse of the control unit, a top-down view after removing the top of the
    unit [#]_.

.. center::

    .. image:: /thumbnails/subaru-outback-radio/disassembly-motherboard_small.jpg
        :target: {static}/images/subaru-outback-radio/disassembly-motherboard.jpg
        :alt: The main circuit board of the unit.

    .. image:: /thumbnails/subaru-outback-radio/disassembly-motherboard-reverse_small.jpg
        :target: {static}/images/subaru-outback-radio/disassembly-motherboard-reverse.jpg
        :alt: The reverse of the main circuit board of the unit.

    The actual circuit board of the stereo unit. You can see the radio module on
    the left.

The radio module connects to the motherboard with a 36-pin connector. Pin 31 is
the right audio channel and pin 32 is left audio channel. I verified this by
connected the disassembled radio to the car and testing with alligator clips
hooked up to my phones audio output [#]_. I already knew these were the pins
from the directions, but I verified by completing the circuit to these pins and
ensuring I heard mixed audio with my phone and the radio.

The direction suggested cutting the pin and bending it up to solder to it. I
didn't have any cutting tool small enough to get in between the pins...so I
flipped the board over and did sketchier things. I scored the board to remove
the traces [#]_ that connected the radio module to the rest of the board. I then
soldered on either side of this connection to put it through the audio
connector.

.. center::

    .. image:: /thumbnails/subaru-outback-radio/soldered-connections_small.jpg
        :target: {static}/images/subaru-outback-radio/soldered-connections.jpg
        :alt: Soldered leads to the bottom of the stereo board.

    .. image:: /thumbnails/subaru-outback-radio/soldered-ground_small.jpg
        :target: {static}/images/subaru-outback-radio/soldered-ground.jpg
        :alt: Soldered ground to the top of the radio unit.

    Five soldered connections are required, four to the bottom of the board [#]_
    and one to the ground at the top of the unit.

Now, the way that this works is that the audio connector output (pins 2 and 5)
is *always* connected. If nothing is in the jack, it is connected as a
passthrough to the inputs (pins 3 and 4, respectively). If an audio connector is
plugged in, input redirects to the jack. (Pin 1 is ground.) For reference, red
is right audio and green is left audio (black is ground).

.. center::

    .. image:: /thumbnails/subaru-outback-radio/diagrams_medium.jpg
        :target: {static}/images/subaru-outback-radio/diagrams.jpg
        :alt: Wiring diagrams of the connections.

    A few of the diagrams necessary to do this. The top two diagrams are simply
    the connector's two states: no plug and plug. The bottom two diagrams are a
    normal 1/8" audio plug and the physical pin-out and measurements of the
    jack.

    To reiterate, pins 2 and 5 connect to the "stereo side" of the scored pins
    31 and 32 of the radio module. (I.e. They are the output from the connector
    back to what will be played by the stereo.) Pins 3 and 4 are the inputs from
    the radio module side of pins 31 and 32 to the connector.


So after soldering for connections (and some hot glue), we have the ability to
intercept the signal. At this point I took the bare motherboard and tested this
in my car with alligator clips to ensure the radio still worked, I then
connected the alligator clips to a cut audio plug to ensure everything worked.

.. center::

    .. image:: /thumbnails/subaru-outback-radio/hot-glued-connections_small.jpg
        :target: {static}/images/subaru-outback-radio/hot-glued-connections.jpg
        :alt: Hot glued wires to the board as strain relief.

    .. image:: /thumbnails/subaru-outback-radio/testing-alligator-clips_small.jpg
        :target: {static}/images/subaru-outback-radio/testing-alligator-clips.jpg
        :alt: Testing with alligator clips. (after reassembly).

    The wires were also hot glued to the circuit board as strain relief. After
    reassembly I tested again with alligator clips.

At this point, I reassembled the radio case and ran the wires out through holes
in the side / bottom toward the front of the unit. I noticed there was an empty
spot in the top left of the unit which looked like it would fit the panel mount
audio jack. After doing some measurements I deemed my chances good enough to
drill a hole here for the connector. Some tips on drilling plastic, if you
haven't done it much: use the lowest speed you can; start with very small bits
and work your way up (I used 4 stages of bits); and cover both sides in masking
tape to avoid scratches.

.. center::

    .. image:: /thumbnails/subaru-outback-radio/drilled-setup_small.jpg
        :target: {static}/images/subaru-outback-radio/drilled-setup.jpg
        :alt: Taped and measurements for drilling the hole from the front.

    .. image:: /thumbnails/subaru-outback-radio/drilled-setup-reverse_small.jpg
        :target: {static}/images/subaru-outback-radio/drilled-setup-reverse.jpg
        :alt: Taped and measurements for drilling the hole from the reverse.

    Another benefit of tape is you can write anywhere you want. These
    measurements were taken initially on the back and transcribed to the front
    (where I drilled from).

The plastic was actually too think for the panel mount connector to reach
through, which is where the 1/2" spade bit came in handy. I use it to drill
through roughly half the thickness of the plastic (a little at a time with lots
of testing). The connector was able to nestle inside the thinner plastic and
reach all the way through.

.. center::

    .. image:: /thumbnails/subaru-outback-radio/drilled-hole_small.jpg
        :target: {static}/images/subaru-outback-radio/drilled-hole.jpg
        :alt: The 1/4" hole drilled through the plastic.

    .. image:: /thumbnails/subaru-outback-radio/drilled-hole-reverse_small.jpg
        :target: {static}/images/subaru-outback-radio/drilled-hole-reverse.jpg
        :alt: The thinning of the plastic from the 1/2" spade bit.

    .. image:: /thumbnails/subaru-outback-radio/drilled-hole-assembly_small.jpg
        :target: {static}/images/subaru-outback-radio/drilled-hole-assembly.jpg
        :alt: The assembled connector in the hole

    After the initial hole was drilled, the tape on the back was removed to thin
    the plastic.

The last bit was soldering the five connections onto the audio connector,
applying a coating of hot glue (for strain relief and to avoid shorts). Once
the connector was soldered, the front panel was carefully reassembled. Finally,
the completed unit was reinstalled back into the car and voila, I now have an
auxiliary audio input! Can't wait to test it out on a long car trip.

.. center::

    .. image:: /thumbnails/subaru-outback-radio/soldered-switch_small.jpg
        :target: {static}/images/subaru-outback-radio/soldered-switch.jpg
        :alt: The soldered jack.

    .. image:: /thumbnails/subaru-outback-radio/hot-glued-switch_small.jpg
        :target: {static}/images/subaru-outback-radio/hot-glued-switch.jpg
        :alt: The hot-glued jack.

    The soldered and hot-glued audio jack.

.. center::

    .. image:: /thumbnails/subaru-outback-radio/install-1_small.jpg
        :target: {static}/images/subaru-outback-radio/install-1.jpg
        :alt: The installed unit.

    .. image:: /thumbnails/subaru-outback-radio/install-2_small.jpg
        :target: {static}/images/subaru-outback-radio/install-2.jpg
        :alt: Close-up of the new jack.

    The final installed stereo unit.

One caveat of doing this (and I'm unsure if this is because I didn't cut the
pins as suggested or if this is just a fact of doing it this way...). If you
have an auxiliary input device playing AND play a CD, the audio mixes instead of
being replaced by the auxiliary device. It works fine on radio though, so just
remember to set the stereo to FM.

.. [#]  The head unit of the stereo is directly built into the dashboard and
        includes the heat / air conditioning controls. People_ do sell kits to
        convert the dash into one that can accept an aftermarket radio...but
        where's the fun in that?
.. [#]  The 2007 edition had an option for a stereo with satellite radio and an
        AUX input. I probably could have bought this stereo and installed it,
        but I was quoted $285 last time I asked about changing my radio.
.. [#]  You can see I actually had a CD in the CD player when I removed the
        radio. Oops! Luckily it was just a copy of one of my CDs (I never take
        originals in my car). I didn't end up scratching it or anything either!
.. [#]  Playing one of my favorite albums: |No Control|_ by `Bad Religion`_
.. [#]  This might seem insane, but I was fairly certain I'd be able to solder a
        jumper back into place if everything didn't work, so I actually felt
        more comfortable doing this than cutting the pin.
.. [#]  Please don't judge my soldering! Two of the four connections were a
        little sloppy (I had to add solder to those instead of just tinning the
        wires). I did ensure there were no shorts with a multimeter (and had to
        resolder one connection).

.. _2005 (fourth generation) Subaru Outback: http://en.wikipedia.org/wiki/Subaru_Legacy#Fourth_generation_.282003.E2.80.932009.29_-_BL.2C_BP
.. _involved always playing a silent CD: http://www.jazzyengineering.com/product_info.php?cPath=21&products_id=28
.. _came across: http://snackeyes.blogspot.com/2011/06/2005-subaru-outback-aux-in-hack-via.html
.. _Someone else: http://www.subaruoutback.org/forums/69-audio-video-security-navigation/36606-2005-outback-aux-hack-via-radio-module-success.html
.. _two: https://www.youtube.com/watch?v=7W7otDaBwJk
.. _videos: https://www.youtube.com/watch?v=EzoGJBNMwmU
.. _PDF: http://www.metraonline.com/files/products/INST99-8901.pdf
.. _switching audio jack: http://www.radioshack.com/product/index.jsp?productId=2103451
.. _Wire strippers: http://en.wikipedia.org/wiki/File:Wire_stripper.jpg
.. _Flashlight: http://www.streamlight.com/product/product.aspx?pid=133
.. _people: http://www.metraonline.com/part/Subaru_Legacy_Dash_kit_99-8901
.. |No Control| replace:: *No Control*
.. _No Control: http://en.wikipedia.org/wiki/No_Control_%28Bad_Religion_album%29
.. _Bad Religion: http://en.wikipedia.org/wiki/Bad_Religion
