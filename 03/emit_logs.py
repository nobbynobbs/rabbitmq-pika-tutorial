# * A producer is a user application that sends messages.
# * A queue is a buffer that stores messages.
# * A consumer is a user application that receives messages.

# ! producer never sends any messages directly to a queue. 

# the producer can only send messages to an exchange.

# There are a few exchange types available: direct, topic, headers and fanout


import pika, sys

connection = pika.BlockingConnection(
    pika.ConnectionParameters('localhost')
)
channel = connection.channel()

channel.exchange_declare(exchange='logs',
                         exchange_type='fanout')

# The fanout exchange is very simple.
# It just broadcasts all the messages it receives to all the queues it knows

message = ' '.join(sys.argv[1:]) or "info: Hello World!"

channel.basic_publish(exchange='logs',
                      routing_key='',
                      body=message)

print(" [x] Sent %r" % message)
connection.close()




