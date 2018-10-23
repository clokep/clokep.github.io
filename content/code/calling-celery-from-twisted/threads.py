from twisted.internet import defer, task

from threadedcelery import send_task

from tasks import app

@defer.inlineCallbacks
def main(reactor):
    # Send the message.
    print("Sending task(s)")
    result = send_task(app, 'tasks.sleep', args=(2,))
    result2 = send_task(app, 'tasks.add', args=(1, 2))
    result = yield result
    result2 = yield result2
    print("Got results: ", result, result2)


if __name__ == '__main__':
    task.react(main)
