#!/usr/bin/env python
import pika
import uuid
import sys

# Our RPC will work like this:

# When the Client starts up, it creates an anonymous exclusive callback queue.
# For an RPC request, the Client sends a message with two properties:
# reply_to, which is set to the callback queue and correlation_id,
# which is set to a unique value for every request.

# The request is sent to an rpc_queue queue.
# The RPC worker (aka: server) is waiting for requests on that queue.
# When a request appears, it does the job and sends a message with the result back to the Client,
# using the queue from the  reply_to field.
# The client waits for data on the callback queue. When a message appears,
# it checks the correlation_id property. If it matches the value from the request it returns the response to the application.

class FibonacciRpcClient(object):
    def __init__(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(
                host='localhost'))

        self.channel = self.connection.channel()

        result = self.channel.queue_declare(exclusive=True)
        self.callback_queue = result.method.queue

        self.channel.basic_consume(self.on_response, no_ack=True,
                                   queue=self.callback_queue)


    # We're going to set correlation_id to a unique value for every request.
    # Later, when we receive a message in the callback queue we'll look at this property,
    # and based on that we'll be able to match a response with a request.
    # If we see an unknown correlation_id value,
    # we may safely discard the message - it doesn't belong to our requests.
    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body

    def call(self, n):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(exchange='',
                                   routing_key='rpc_queue',
                                   properties=pika.BasicProperties(
                                        # In general doing RPC over RabbitMQ is easy.
                                        # A client sends a request message and a server replies with a response message.
                                        # In order to receive a response the client needs to send 
                                        # a 'callback' queue address with the request
                                        reply_to = self.callback_queue,
                                        correlation_id = self.corr_id,
                                        ),
                                   body=str(n))
        while self.response is None:
            self.connection.process_data_events()
        return int(self.response)

fibonacci_rpc = FibonacciRpcClient()

try:
    n = int(sys.argv[1])
except IndexError:
    n = 30
    
print(f" [x] Requesting fib({n})")
response = fibonacci_rpc.call(n)
print(f" [.] Got {response!r}" )
