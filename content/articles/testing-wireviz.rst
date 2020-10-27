Testing WireViz
###############
:date: 2020-07-14 17:07
:modified: 2020-07-16 16:03
:author: Patrick Cloke
:tags: software, hardware
:slug: testing-wireviz

I wanted to play with the `WireViz`_ Python package, which makes pretty wire
diagrams. Installation was pretty easy, just created a virtualenv and installed
with pip:

.. code-block:: bash

  pip install wireviz

Documentation is pretty limited, but looking through the `tutorials`_ and the
`data models`_ you get a pretty good idea of what's possible.

I'm using the wiring diagrams from my `guide to add an auxiliary audio input to a 2005 Subaru Outback`_,
which is pretty simple, there's an audio jack which connects to the Outback's
motherboard and the Outback's FM audio module (and ground).

The input is a `YAML`_ document with three sections:
* ``connectors`` - A list of connectors and the information about their port.
* ``cables`` - A list of wires (and their information, e.g. gauge).
* ``connections`` - A lists of ports that should be connected via each cable.

I had a pretty simple example, but it ended up being quite a bit of YAML:

.. include:: ../code/testing-wireviz/subaru-wiring.yaml
    :code: yaml
    :class: highlight

:strike:`The only thing I couldn't figure out was how to list two pins with the proper names and pins numbers, but ignore all the other ones. Note a huge deal for a 36-pin connector.`
See the comments below, this is doable, although a little awkward!

It did create a fairly pretty diagram after running ``wireviz subaru-wiring.yaml``
and is certainly easier than directly using `graphviz`_. It ouputs a SVG, PNG,
bill of materials, HTML page (with the bill of materials and image on it).
Overall, I'd use it again if I had a need!

.. center::

  .. image:: {static}/code/testing-wireviz/subaru-wiring.svg
      :target: {static}/code/testing-wireviz/subaru-wiring.svg
      :width: 100%

.. _WireViz: https://github.com/formatc1702/WireViz
.. _tutorials: https://github.com/formatc1702/WireViz/tree/fffb354d7c86cc4f85d1e7e0753a07f7b6a65fa7/tutorial
.. _data models: https://github.com/formatc1702/WireViz/blob/fffb354d7c86cc4f85d1e7e0753a07f7b6a65fa7/src/wireviz/DataClasses.py
.. _guide to add an auxiliary audio input to a 2005 Subaru Outback: {filename}/articles/adding-an-auxiliary-audio-input-to-2005-subaru-outback.rst
.. _YAML: https://yaml.org/
.. _graphviz: https://graphviz.org/
