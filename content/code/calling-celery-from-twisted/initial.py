from twisted.internet import defer, task

from txcelery.defer import DeferredTask

from tasks import add, sleep


@defer.inlineCallbacks
def main(reactor):
    # This yield is useless.
    yield

    # Send the message.
    print("Sending task(s)")
    result = sleep.delay(2)
    result2 = add.delay(1, 2)
    result = result.get()  # This blocks the reactor.
    result2 = result2.get()  # This blocks the reactor.
    print("Got results: ", result, result2)


if __name__ == '__main__':
    task.react(main)
