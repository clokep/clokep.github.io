import time

from celery import Celery

app = Celery(broker='amqp://guest:guest@127.0.0.1:5672//', backend='rpc')


@app.task
def sleep(n):
    time.sleep(n)
    return n


@app.task
def add(a, b):
    return a + b
