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

channel.exchange_declare(exchange='direct_logs',
                         exchange_type='direct') # changed!


severity = sys.argv[1] if len(sys.argv) > 2 else 'info'
message = ' '.join(sys.argv[2:]) or 'Hello World!'

channel.basic_publish(exchange='direct_logs',
                      routing_key=severity,
                      body=message)

print(f" [x] Sent {severity}:{message}")
connection.close()




