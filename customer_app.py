from types import SimpleNamespace
import pika
import json
from db_and_event_definitions import CustomerEvent
import time
import logging

from xprint import xprint


class CustomerEventConsumer:

    def __init__(self, customer_id):
        # Do not edit the init method.
        # Set the variables appropriately in the methods below.
        self.customer_id = customer_id
        self.connection = None
        self.channel = None
        self.temporary_queue_name = None
        self.customer_events = []
        self.customer_events_exchange = "customer_events_exchange"

    def initialize_rabbitmq(self):
        # To implement - Initialize the RabbitMq connection, channel, exchange and queue here
        xprint("CustomerEventConsumer {}: initialize_rabbitmq() called".format(self.customer_id))
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost'))
        self.channel = self.connection.channel()
        self.channel.exchange_declare(exchange=self.customer_events_exchange, exchange_type='topic')

        self.temporary_queue_name = self.channel.queue_declare(queue='', exclusive=True).method.queue
        self.channel.queue_bind(exchange=self.customer_events_exchange, queue=self.temporary_queue_name, routing_key=self.customer_id)
        self.channel.basic_consume(queue=self.temporary_queue_name, on_message_callback=self.handle_event, auto_ack=True)

    def handle_event(self, ch, method, properties, body):
        # To implement - This is the callback that is passed to "on_message_callback" when a message is received
        xprint("CustomerEventConsumer {}: handle_event() called".format(self.customer_id))
        # Handle the application logic here
        customer_event = CustomerEvent(**json.loads(body))
        self.customer_events.append(customer_event)

    def start_consuming(self):
        # To implement - Start consuming from Rabbit
        xprint("CustomerEventConsumer {}: start_consuming() called".format(self.customer_id))
        self.channel.basic_consume(queue=self.temporary_queue_name, on_message_callback=self.handle_event, auto_ack=True)
        self.channel.start_consuming()

    def close(self):
        # Do not edit this method
        try:
            if self.channel is not None:
                print("CustomerEventConsumer {}: Closing".format(self.customer_id))
                self.channel.stop_consuming()
                time.sleep(1)
                self.channel.close()
            if self.connection is not None:
                self.connection.close()
        except Exception as e:
            print("CustomerEventConsumer {}: Exception {} on close()"
                  .format(self.customer_id, e))
            pass
