import pika, time, random

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

channel.queue_declare(queue='task_queue', durable=True)

def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)
    time.sleep(random.randint(0,5))
    print(" [x] Done")
    ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_qos(prefetch_count=1)
channel.basic_consume(callback,
                queue='task_queue')

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()


# Using message acknowledgments and prefetch_count you can set up a work queue.
# The durability options let the tasks survive even if RabbitMQ is restarted.
