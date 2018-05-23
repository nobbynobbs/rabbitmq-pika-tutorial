#!/usr/bin/python3

import pika, sys

# The main idea behind Work Queues (aka: Task Queues) is to avoid doing a resource-intensive task immediately
# and having to wait for it to complete. Instead we schedule the task to be done later.
# We encapsulate a task as a message and send it to the queue. 
# A worker process running in the background will pop the tasks and eventually execute the job. 
# When you run many workers the tasks will be shared between them.

connection = pika.BlockingConnection(
    pika.ConnectionParameters('localhost')
)
channel = connection.channel()

channel.queue_declare(queue='task_queue', durable=True)

message = ' '.join(sys.argv[1:]) or "Hello World!"

channel.basic_publish(exchange='',
                    routing_key='task_queue',
                    body=message,
                    properties=pika.BasicProperties(
                        delivery_mode = 2, # make message persistent
                    ))
print(" [x] Sent {!r}".format(message))

connection.close()

# Marking messages as persistent doesn't fully guarantee that a message won't be lost.
# Although it tells RabbitMQ to save the message to disk,
# there is still a short time window when RabbitMQ has accepted a message and hasn't saved it yet.
# Also, RabbitMQ doesn't do fsync(2) for every message -- 
# it may be just saved to cache and not really written to the disk. 
# The persistence guarantees aren't strong, but it's more than enough for our simple task queue.
# If you need a stronger guarantee then you can use publisher confirms.

