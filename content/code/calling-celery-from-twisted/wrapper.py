from twisted.internet import defer, task

from txcelery.defer import DeferredTask

from tasks import add, sleep


@defer.inlineCallbacks
def main(reactor):
    # Send the message.
    print("Sending task(s)")
    result = DeferredTask(sleep.delay(2))
    result2 = DeferredTask(add.delay(1, 2))
    result = yield result  # This *could* block the reactor.
    result2 = yield result2
    print("Got results: ", result, result2)


if __name__ == '__main__':
    task.react(main)
