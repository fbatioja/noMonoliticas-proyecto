import pulsar,_pulsar  
from pulsar.schema import *

import logging
import traceback
import uuid

from warehouse_ms.modules.outbounds.infrastructure.schema.v1.events import CanceledOrderEvent, CreatedOrderEvent
from warehouse_ms.modules.outbounds.infrastructure.projections import OrderCreatedProjection, OrderCanceledProjection
from warehouse_ms.seedwork.infrastructure.projections import execute_projection
from warehouse_ms.seedwork.infrastructure import utils

client_connection = f'pulsar://{utils.broker_host()}:6650'

def subscribe_to_created_order_event(app=None):
    _subscribe_to_events(app, 'order-created', 'eds-sub-events', CreatedOrderEvent, _execute_created_order)

def _execute_created_order(data, app):
    return execute_projection(OrderCreatedProjection(data.order_id, data.products, data.destiny), app=app)

def subscribe_to_canceled_order_event(app=None):
    _subscribe_to_events(app, 'order-canceled', 'eds-sub-events', CanceledOrderEvent, _execute_canceled_order)

def _execute_canceled_order(data, app):
    return execute_projection(OrderCanceledProjection(data.order_id, data.products, data.destiny), app=app)

def _subscribe_to_events(app, topic, subscription_name, schema, projection):
    try:
        client = pulsar.Client(client_connection)
        consumer = client.subscribe(topic, consumer_type=_pulsar.ConsumerType.Shared, subscription_name=subscription_name, schema=AvroSchema(schema))

        while True:
            message = consumer.receive()
            event = message.value()
            data = event.data
            print(f'Received event: {event}')

            projection(data, app)

            consumer.acknowledge(message)

        client.close()
    except:
        logging.error('ERROR: Event topic subscription!')
        traceback.print_exc()
        if client:
            client.close()