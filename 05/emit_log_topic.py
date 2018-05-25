# the direct exchange has limitations - it can't do routing based on multiple criteria.

# Messages sent to a topic exchange can't have an arbitrary routing_key - it must be a list of words, delimited by dots.
# There can be as many words in the routing key as you like, up to the limit of 255 bytes.

# The binding key must also be in the same form.
# The logic behind the topic exchange is similar to a direct one
# - a message sent with a particular routing key will be delivered to all the queues
# that are bound with a matching binding key. 
# However there are two important special cases for binding keys:
# * (star) can substitute for exactly one word.
# # (hash) can substitute for zero or more words.

# When a queue is bound with "#" (hash) binding key - it will receive all the messages, regardless of the routing key - like in fanout exchange.
# When special characters "*" (star) and "#" (hash) aren't used in bindings, the topic exchange will behave just like a direct one.

import pika, sys
from settings import exchange, exchange_type

connection = pika.BlockingConnection(
    pika.ConnectionParameters('localhost')
)
channel = connection.channel()

channel.exchange_declare(exchange=exchange,
                         exchange_type=exchange_type) 

routing_key = sys.argv[1] if len(sys.argv) > 2 else 'anonymous.info'
message = ' '.join(sys.argv[2:]) or 'Hello World!'

channel.basic_publish(exchange=exchange,
                      routing_key=routing_key,
                      body=message)

print(f" [x] Sent {routing_key}:{message}")
connection.close()

