import pika, sys

connection = pika.BlockingConnection(
    pika.ConnectionParameters('localhost')
)
channel = connection.channel()

channel.exchange_declare(exchange='direct_logs',
                         exchange_type='direct')

# create the fresh queue with random name
# exclusive=True means once the consumer connection is closed, the queue should be deleted
# https://www.rabbitmq.com/queues.html
result = channel.queue_declare(exclusive=True)
queue_name = result.method.queue

severities = sys.argv[1:]
if not severities:
    sys.stderr.write(f"Usage: {sys.argv[0]} [info] [warning] [error]\n")
    sys.exit(1)
# A binding is a relationship between an exchange and a queue. 
# This can be simply read as: the queue is interested in messages from this exchange.
for severity in severities:
    channel.queue_bind(exchange='direct_logs',
                       queue=queue_name,
                       routing_key=severity)

print(' [*] Waiting for logs. To exit press CTRL+C')

def callback(ch, method, properties, body):
    print(f" [x] {method.routing_key}:{body}")

channel.basic_consume(callback,
                      queue=queue_name,
                      no_ack=True)

channel.start_consuming()