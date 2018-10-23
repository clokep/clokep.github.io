Compare some ways to call Celery tasks from Twisted.

To run this, ensure you have a RabbitMQ server running on localhost:

.. code-block:: bash

    rabbitmq-server

And start a Celery worker.

.. code-block:: bash

    celery -A tasks worker --loglevel=INFO -Q celery --without-gossip --without-mingle

Then run what you want to test, e.g.:

.. code-block:: bash

    python inital.py
    python wrapper.py
    python threads.py
