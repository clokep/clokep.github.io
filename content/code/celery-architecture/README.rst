To run this, ensure you have a RabbitMQ server running on localhost:

.. code-block:: bash

    rabbitmq-server

And start a Celery worker.

.. code-block:: bash

    celery -A my_app worker --loglevel=INFO -Q celery --without-gossip --without-mingle

Then run your client:

.. code-block:: bash

    python my_app.py
