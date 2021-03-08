JavaScript typed arrays pain
############################
:date: 2012-11-28 23:11
:author: Patrick Cloke
:tags: Instantbird, Mozilla, OSCAR, Thunderbird, Wat
:slug: javascript-typed-arrays-pain

If you've ever tried to deal with binary data in JavaScript you know
it isn't much fun and you usually resort to using strings lots of
charCodeAt and related functions. `Typed arrays`_ are supposed to solve
this though! The typed array API consists of creating a buffer of bytes
(called an `ArrayBuffer`_) and then manipulating those bytes via
different views (`ArrayBufferView`_\ s). You can have multiple views of
the same buffer, starting at different offsets, of different lengths and
types...which is all neat from a technical point of view, but is it
really useful? It is kind of nice working with the views as if they
were normal arrays though.

I've been playing with these ArrayBuffers quite a bit as I'm working
on an implementation of the `OSCAR protocol`_ (used for `AOL Instant
Messenger`_ and `ICQ`_) in the chat backend (for Instantbird /
Thunderbird). (As an aside, the OSCAR protocol Wikipedia page has
surprisingly good documentation of some of the underlying data
structures of the protocol...) I started by writing some test code
using ArrayBuffers and views, which have been around a while: since
Gecko 2.0 in fact! I quickly ran into some tedious issues with
repetitive code such as:

.. code-block:: javascript

    /*
     * A TLV (Type, Length and Value) data structure:
     *  Unsigned Short  type    Describes what the value represents.
     *  Unsigned Short  length  The length of the data block.
     *  Bytes           value   The raw payload.
     *
     * The overall length of a TlvBlock is length + 4.
     *
     * The inputs to this are:
     *  aType    The type of the TLV Block.
     *  aValue   An ArrayBuffer containing the data.
     */
    function TlvBlock(aType, aValue) {
      let data = new ArrayBuffer(aValue.byteLength + 4);
      // The first two bytes are unsigned shorts.
      let view = new Uint16Array(data, 0, 2);
      view[0] = aType;
      view[1] = aValue.byteLength;

      // The rest just gets the data copied into it.
      view = new Uint8Array(data, 4);
      view.set(new Uint8Array(aValue));

      return data;
    }


This actually illustrates two annoying issues I have:

#. I end up with extra lines of code defining a new view every time I
   switch data types.
#. There's no simple way to copy an ArrayBuffer into a part of an
   ArrayBuffer. In the above example I create a Uint8Array view of the
   target location, a Uint8Array view of the source location and then
   set the source to the target. Seems simple once you figure it out,
   but it took a while to figure out.

(As an aside, some of you might find the following function helpful,
it is essentially a `memcpy`_ for ArrayBuffers...this isn't really
tested heavily at all, however.)

.. code-block:: javascript

    /*
     * aTarget / aSource are ArrayBuffers
     */
    function copyBytes(aTarget, aSource, aTargetOffset = 0, aSourceOffset = 0, aLength = aSource.byteLength) {
      // The rest just gets the data copied into it.
      let view = new Uint8Array(aTarget, aTargetOffset);
      view.set(new Uint8Array(aSource, aSourceOffset, aLength));
    }

OK, so typed arrays seem good, but kind of annoying, right?
Wrong...the OSCAR protocol is a "network order" protocol (aka it is big
endian). At this point you're probably thinking "OK, so the ArrayBuffer
constructor must take an endianess flag!" Wrong, it does no such
thing. "Hmmm...Well do the ArrayBufferViews take an endianess flag?"
Nope, wrong again. The only way to specify the endianess of the data is
to use a `DataView`_, a slightly different interface to the underlying
bytes. It offers an API to individually set different data elements via
their offset and endianess. (If you're too lazy to read the
documentation all the way through, DataView assumes big endian: makes my
life easier!)

For the curious, JavaScript typed arrays use the system endianess,
which in my opinion is pretty much useless (at least if you plan on
sharing data) since you can never guarantee the endianess to be either
big or little endian. (The fun part is that this isn't even documented,
I found it on `Stack Overflow`_ and verified.)

So, in summary...if you plan on networking at all with ArrayBuffers,
don't use ArrayBufferViews, use DataViews. (Although Uint8Arrays and
Int8Arrays should work fine!)

And to not rant the *entire* time, working with typed arrays certainly
does beat strings + charCodeAt!

.. _Typed arrays: https://developer.mozilla.org/en-US/docs/JavaScript_typed_arrays
.. _ArrayBuffer: https://developer.mozilla.org/en-US/docs/JavaScript_typed_arrays/ArrayBuffer
.. _ArrayBufferView: https://developer.mozilla.org/en-US/docs/JavaScript_typed_arrays/ArrayBufferView
.. _OSCAR protocol: http://en.wikipedia.org/wiki/OSCAR_protocol
.. _AOL Instant Messenger: http://en.wikipedia.org/wiki/AOL_Instant_Messenger
.. _ICQ: http://en.wikipedia.org/wiki/ICQ
.. _memcpy: http://en.cppreference.com/w/cpp/string/byte/memcpy
.. _DataView: https://developer.mozilla.org/en-US/docs/JavaScript_typed_arrays/DataView
.. _Stack Overflow: http://stackoverflow.com/questions/7869752/javascript-typed-arrays-and-endianness
