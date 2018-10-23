from celery import states

from twisted.internet import defer, reactor, threads


def send_task(app, *args, **kwargs):
    # Call the real function via a background thread.
    return threads.deferToThread(app.send_task, *args, **kwargs).addCallback(CeleryDeferred)


class CeleryDeferred(defer.Deferred, object):
    """
    Extension of the Twisted Deferred object that wraps a Celery AsyncResult.

    This Deferred will occasionally poll the Celery task for its status. When
    complete, the Deferred will resolve and any added callbacks will be run.

    Inspired by txCelery: https://github.com/SentimensRG/txCelery/
    """
    CHECK_INTERVAL = 0.25

    def __init__(self, async_result):
        # Deferred is an old-style class
        defer.Deferred.__init__(self, self._canceller)

        self.async_result = async_result
        # Start the monitor loop
        self.check_state()

    def check_state(self):
        """Check the status of the celery task on another thread."""
        threads.deferToThread(self.get_state).addCallbacks(self.state_received, self.errback)

    def get_state(self):
        """Check the status of the celery task directly"""
        return self.async_result.state

    def state_received(self, celery_state):
        """Called when the check_state thread finishes"""
        if celery_state in states.UNREADY_STATES:
            # Schedule another status check, to be run later.
            reactor.callLater(self.CHECK_INTERVAL, self.check_state)
        elif celery_state == states.SUCCESS:
            self.callback(self.async_result.result)
        elif celery_state == states.FAILURE:
            # This will contain the Exception instance if the task raised one
            # http://docs.celeryproject.org/en/latest/reference/celery.result.html
            self.errback(self.async_result.result)
        elif celery_state == states.REVOKED:
            self.errback(defer.CancelledError('Task {0}'.format(self.async_result.id)))
        else:
            # An unknown state was returned.
            self.errback(ValueError('Unknown state: `{}`'.format(celery_state)))

    def _canceller(self):
        # Revoke the celery task
        self.async_result.revoke()
