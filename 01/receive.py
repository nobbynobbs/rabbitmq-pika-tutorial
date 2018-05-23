import pika

connection = pika.BlockingConnection(
    pika.ConnectionParameters('localhost')
)
channel = connection.channel()

# Creating a queue using queue_declare is idempotent ‒ we can run the command as many times as we like,
# and only one will be created.

# You may ask why we declare the queue again ‒ we have already declared it in our previous code.
# We could avoid that if we were sure that the queue already exists.
# For example if send.py program was run before. But we're not yet sure which program to run first.
# In such cases it's a good practice to repeat declaring the queue in both programs.

channel.queue_declare(queue='hello')

def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)


# no_ack=True - turn off manual message acknowledgments
channel.basic_consume(callback, queue='hello', no_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
