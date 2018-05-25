import pika, sys
from settings import exchange, exchange_type

connection = pika.BlockingConnection(
    pika.ConnectionParameters('localhost')
)
channel = connection.channel()

channel.exchange_declare(exchange=exchange,
                         exchange_type=exchange_type)

# create the fresh queue with random name
# exclusive=True means once the consumer connection is closed, the queue should be deleted
# https://www.rabbitmq.com/queues.html
result = channel.queue_declare(exclusive=True)
queue_name = result.method.queue

binding_keys = sys.argv[1:]
if not binding_keys:
    sys.stderr.write(f"Usage: {sys.argv[0]} [binding_key]...\n")
    sys.exit(1)
# A binding is a relationship between an exchange and a queue. 
# This can be simply read as: the queue is interested in messages from this exchange.
for binding_key in binding_keys:
    channel.queue_bind(exchange=exchange,
                       queue=queue_name,
                       routing_key=binding_key)

print(' [*] Waiting for logs. To exit press CTRL+C')

def callback(ch, method, properties, body):
    print(f" [x] {method.routing_key}:{body}")

channel.basic_consume(callback,
                      queue=queue_name,
                      no_ack=True)

channel.start_consuming()