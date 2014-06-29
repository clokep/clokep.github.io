Extending JavaScript Maps (or other built-in objects)
#####################################################
:date: 2014-04-27 17:46
:author: Patrick Cloke
:tags: IM, Instantbird, programming, specifications, Thunderbird, Wat
:slug: extending-javascript-maps-or-other-built-in-objects

Finally another technical post, this one is about my adventures in
attempting to extend the built-in `Map`_ object in JavaScript to extend
the functionality. As background, there are two reasons we'd want this:

#. In the chat backend we currently use JavaScript `objects`_ (``{}``) as
   hashes/maps to keep track of various things (i.e. there's a `hash of
   conversations`_ which map from conversation name to prplIConversation
   objects in the IRC code). Whenever checking to see if something is in
   this map we have to use `hasOwnProperty`_. This has to be the
   `version from Object.prototype`_ in case the map has a conversation
   named hasOwnProperty. This is `super simple code`_, but annoying:

    .. code-block:: javascript

        // Similar to Object.hasOwnProperty, but doesn't fail if the object
        // has a hasOwnProperty property set.
        function hasOwnProperty(aObject, aPropertyName)
          Object.prototype.hasOwnProperty.call(aObject, aPropertyName)

   `Replacing these custom objects with a Map`_ would alleviate this
   funky dance.

#. Frequently in the chat backend we have to "normalize" [#]_ strings
   (e.g. #INsTanTBIrd and #instantbird are the same on IRC [#]_). This is
   almost always done for sane storage of data received from the network
   (or from the user). I figured it'd be great if, instead of having to
   `manually`_ `handle`_ `this`_ normalization each time we tried to
   access data, the keys were magically normalized when accessing the
   data.
   (Note that although normalization is generally more complicated, just
   consider to be `String.prototype.toLowerCase()`_ for the rest of this
   post!)

This has been explored before by `others`_, but generally in the
context of web sites / cross browser compatibility. Which are concerns
that don't really limit us for backend code.

Goals
=====

#. Replace objects with Maps for safe access. This is pretty easily
   fixed by switching all ``obj["foo"]`` calls to ``obj.get("foo")`` (or the
   appropriate other method: set, delete, etc.)
#. Automatically "normalize" keys in the some user defined way, e.g.
   such that ``obj.get("foo")`` and ``obj.get("FoO")`` return the same value.

First Approach (setting \_\_proto\_\_ to Map.prototype)
=======================================================

My first naive approach was to create an object with ``__proto__`` set
to Map.prototype and overwrite anything that uses keys to appropriately
call a normalization function.

.. code-block:: javascript

    function NormalizedMap() { }
    NormalizedMap.prototype = {
        __proto__: Map.prototype,
        _normalize: function(aStr) aStr.toLowerCase(),

        get: function(aStr) Map.prototype.get.call(this, this._normalize(aStr)),
        set: function(aStr, aVal) Map.prototype.set.call(this, this._normalize(aStr), aVal)
    };

    let m = new NormalizedMap();
    m.set("foo", 1) // Throws TypeError: set method called on incompatible Object
    m instanceof Map; // true . . . wat . . .

This throws an error and does not work. Apparently there are plans to
`support something like this`_. The totally fun thing, in my opinion, is
that m is an instance of a Map!

Second Approach (modifying \_\_proto\_\_ after instance creation)
=================================================================

My second approach was to generate a real Map and then override the
``__proto__`` to give it the properties I wanted:

.. code-block:: javascript

    function NormalizedMap() {
        let m = new Map();  m.__proto__ = NormalizedMap.prototype;
        return m;
    }
    NormalizedMap.prototype = {
        __proto__: Map.prototype,
        _normalize: function(aStr) aStr.toLowerCase(),
        get: function(aStr) Map.prototype.get.call(this, this._normalize(aStr)),
        set: function(aStr, aVal) Map.prototype.set.call(this, this._normalize(aStr), aVal)
    };
    let m = new NormalizedMap();
    m.set("foo", 1)
    m.get("FOO"); // 1
    m instanceof Map; // true

This actually works! But will `throw a warning`_ each time it is
created since changing an objects ``__proto__`` is generally a bad idea.
I also thought of overriding individual methods, but this seemed
cumbersome and would increase the time in the constructor calls. (Which
occur during the start up of each account and is generally a resource
constrained time. No, I didn't profile this, it just seemed like bad
design.)

Solution (wrapping a Map)
=========================

Finally I settled on the simple solution of just wrapping the Map in a
custom object. Initially I thought this would be frustrating to
re-declare every function (and prone to breakage in the future if new
methods are added), but there's a nice magic method
`\_\_noSuchMethod\_\_`_ that fixes this! (Note that this is a
non-standard feature of SpiderMonkey.) ``__noSuchMethod__`` allows an
object to intercept a call to a non-existent method (and in this case
call that same method on the internal Map object).

Below is the final version that seems to act magically like a Map when
necessary (e.g. iterating the map works, all functions and properties
exist, the constructor works [#]_). I need to thank aleth (another chat
developer) who helped out quite a bit with this (and will ultimately be
reviewing this code)!

.. code-block:: javascript

    // A Map that automatically normalizes keys before accessing the values.
    function NormalizedMap(aNormalizeFunction, aIt = []) {
      if (typeof(aNormalizeFunction) != "function")
        throw "NormalizedMap must have a normalize function!";
      this._normalize = aNormalizeFunction;
      this._map = new Map([[this._normalize(key), val] for ([key, val] of aIt)]);
    }
    NormalizedMap.prototype = {
      _map: null,
      // The function to apply to all keys.
      _normalize: null,

      // Anything that accepts a key as an input needs to be manually overridden.
      delete: function(aKey) this._map.delete(this._normalize(aKey)),
      get: function(aKey) this._map.get(this._normalize(aKey)),
      has: function(aKey) this._map.has(this._normalize(aKey)),
      set: function(aKey, aValue) this._map.set(this._normalize(aKey), aValue),

      // Properties must be manually forwarded.
      get size() this._map.size,

      // Here's where the magic happens. If a method is called that isn't defined
      // here, just pass it to the internal _map object.
      __noSuchMethod__: function(aId, aArgs) this._map[aId].apply(this._map, aArgs)
    }

The one downside of see of this is that properties must be declared
manually to forward to the internal ``_map`` object. Maybe there is a
matching ``__noSuchProperty__`` method I'm missing? Overall, I'm happy
with this solution, but please leave a comment if you can think of an
easier / better way to do this! (Or see a glaring way this will break!)

.. [#] This is always a little bit of a sore subject in `#instantbird`_
   since we've had a variety of issues with this over the years. I think
   we've fixed most of them at this point though!
.. [#] As I've `written before`_, IRC tends to have crazy specifications.
   In IRC, `the characters of A-Z[]\\~ are considered the upper case of a-z{}\|^`_
   ("because of IRC's Scandinavian origin"). Oh, also this can
   change based on an `ISUPPORT response`_ from the server to pure ASCII or
   RFC 1459 casemapping (A-Z[]\\ map to a-z{}\|). It seems like this could
   theoretically change at any point on a live server too, although that
   would be INSANE and I hope no one ever does that.
.. [#] I wrote some xpcshell tests to ensure these properties work as
   expected, but they're uhh...not up anywhere yet though. Oops.

.. _Map: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Map
.. _objects: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object
.. _hash of conversations: https://mxr.mozilla.org/comm-central/source/chat/protocols/irc/irc.js#789
.. _hasOwnProperty: https://mxr.mozilla.org/comm-central/source/chat/protocols/irc/irc.js#1509
.. _version from Object.prototype: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object/hasOwnProperty
.. _super simple code: https://mxr.mozilla.org/comm-central/source/chat/modules/imXPCOMUtils.jsm#166
.. _Replacing these custom objects with a Map: https://bugzilla.mozilla.org/show_bug.cgi?id=955366
.. _manually: https://mxr.mozilla.org/comm-central/source/chat/protocols/irc/irc.js#1510
.. _handle: https://mxr.mozilla.org/comm-central/source/chat/protocols/irc/irc.js#1514
.. _this: https://mxr.mozilla.org/comm-central/source/chat/protocols/irc/irc.js#1528
.. _String.prototype.toLowerCase(): https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/String/toLowerCase
.. _others: http://perfectionkills.com/how-ecmascript-5-still-does-not-allow-to-subclass-an-array/
.. _support something like this: https://bugzilla.mozilla.org/show_bug.cgi?id=838540
.. _throw a warning: https://bugzilla.mozilla.org/show_bug.cgi?id=963519
.. _\_\_noSuchMethod\_\_: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object/noSuchMethod
.. _#instantbird: irc://irc.mozilla.org/#instantbird
.. _written before: {filename}/the-so-called-irc-specifications.rst
.. _the characters of A-Z[]\\~ are considered the upper case of a-z{}\|^: https://tools.ietf.org/html/rfc2812#section-2.2
.. _ISUPPORT response: http://tools.ietf.org/html/draft-brocklesby-irc-isupport-03#section-3.1
