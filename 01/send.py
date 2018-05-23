#!/usr/bin/python3

# RabbitMQ, and messaging in general, uses some jargon.

# Producing means nothing more than sending. A program that sends messages is a producer

# A queue is the name for a post box which lives inside RabbitMQ.
# Although messages flow through RabbitMQ and your applications,
# they can only be stored inside a queue. A queue is only bound by the host's memory & disk limits,
# it's essentially a large message buffer. Many producers can send messages that go to one queue,
# and many consumers can try to receive data from one queue. 

# Consuming has a similar meaning to receiving. A consumer is a program that mostly waits to receive messages

import pika

# establish a connection with RabbitMQ server
connection = pika.BlockingConnection(
    pika.ConnectionParameters('localhost')
)
channel = connection.channel()

# before sending we need to make sure the recipient queue exists
# If we send a message to non-existing location, RabbitMQ will just drop the message.
# Let's create a hello queue to which the message will be delivered

channel.queue_declare(queue='hello')

# !!! In RabbitMQ a message can never be sent directly to the queue, it always needs to go through an exchange.
# default exchange identified by an empty string
# This exchange is special ‒ it allows us to specify exactly to which queue the message should go.
# The queue name needs to be specified in the routing_key parameter

channel.basic_publish(exchange='',
                      routing_key='hello',
                      body='Hello World!')
print(" [x] Sent 'Hello World!'")

connection.close()
