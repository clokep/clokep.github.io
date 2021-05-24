celery-batches 0.5 released!
############################
:date: 2021-05-24 16:56
:author: Patrick Cloke
:tags: celery, celery-batches
:slug: celery-batches-0.5-released

A `new version (v0.5)`_ of `celery-batches`_ is available which adds support for
Celery 5.1 and fixes storing of results when using the `RPC result backend`_.

As `explored previously`_, the RPC result backend works by having a results queue
per client, unfortunately celery-batches was attempting to store the results in
a queue named after the task ID instead of the client ID (Celery internally calls
this the "correlation ID") [#]_.

This unfortunately requires a change to client code to pass the batched request
into the ``mark_as_done`` method, using the example `from the documnation`_ with
the changed line highlighted:

.. code-block:: python
    :hl_lines: 16

    import requests
    from urlparse import urlparse

    from celery_batches import Batches

    wot_api_target = 'https://api.mywot.com/0.4/public_link_json'

    @app.task(base=Batches, flush_every=100, flush_interval=10)
    def wot_api(requests):
        sig = lambda url: url
        reponses = wot_api_real(
            (sig(*request.args, **request.kwargs) for request in requests)
        )
        # use mark_as_done to manually return response data
        for response, request in zip(reponses, requests):
            app.backend.mark_as_done(request.id, response, request=request)


    def wot_api_real(urls):
        domains = [urlparse(url).netloc for url in urls]
        response = requests.get(
            wot_api_target,
            params={'hosts': ('/').join(set(domains)) + '/'}
        )
        return [response.json[domain] for domain in domains]

.. [#] The RPC backend has `code which pulls out the correlation ID`_, but falls
       back to the task ID if not given. This is called via an
       |override of the store_result method|_.

.. _new version (v0.5): https://pypi.org/project/celery-batches/0.5/
.. _celery-batches: https://github.com/clokep/celery-batches/
.. _RPC result backend: https://docs.celeryproject.org/en/v5.1.0/userguide/tasks.html#rpc-result-backend-rabbitmq-qpid
.. _explored previously: {filename}/articles/celery-amqp-backends.rst
.. _from the documnation: https://celery-batches.readthedocs.io/en/v0.5/
.. _code which pulls out the correlation ID: https://github.com/celery/celery/blob/v5.1.0/celery/backends/rpc.py#L166
.. |override of the store_result method| replace:: override of the ``store_result`` method
.. _override of the store_result method: https://github.com/celery/celery/blob/v5.1.0/celery/backends/rpc.py#L198-L200
