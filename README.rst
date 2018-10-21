This is the source to my website (https://patrick.cloke.us). It is built using
`Pelican <http://pelican.readthedocs.io/>`_, a static site generator written in
Python.

Development notes
=================

To setup and run, first install the requirements:

.. code-block:: bash

    pip install -r requirements.txt

Common tasks are handled via `Invoke <http://www.pyinvoke.org/>`_, you can see
all tasks with ``inv -l``. A normal workflow might be:

.. code-block:: bash

    # Continually regenerate output files as changes are made.
    inv regenerate
    # Serve the blog on localhost.
    inv serve
