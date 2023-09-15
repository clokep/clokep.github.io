## What is Celery?

> Celery is an asynchronous task queue/job queue based on distributed message
> passing. It is focused on real-time operation, but supports scheduling as
> well.

## When do you use Celery?

* Delaying running something
* Periodic tasks
* Background jobs
* Message passing

## How does Celery work?

Producers, consumers, broker, etc.

What happens when you call delay on a task?
* Sends serialized meta-data and args/kwargs to broker
* Parent process deserializes the data
* passes it to a child process to handle

Diagram of how a task flows and becomes a result.

## Under the hood (a bit)

Repository structure, ensure to pin celery and kombu close to each other (e.g. a.b.c and a.b.d).

## Important settings

Task protocol
Serialization
Queues & exchanges (& routing)
Timeouts (broker & backend)
Queue expiration times
Result expiration times

## Workers



## Writing tasks

Ignore results

## Advanced topics

Broadcast queues
Using with Twisted
Batch processing

## Running a broker

RabbitMQ -> Hosted in CloudAMQP
RabbitMQ clusters are hard to run (many ports open, beam, need to upgrade all at the same time, service discovery / load balancing, etc.)

## Production hardening

Have you tested what happens if your producers can't connect to your broker? Your consumers?
Do you have results that are unused?

https://www.cloudamqp.com/docs/celery.html

## What queues are created and named?

UUIDs, bcast.UUID, how do they hook to exchanges
