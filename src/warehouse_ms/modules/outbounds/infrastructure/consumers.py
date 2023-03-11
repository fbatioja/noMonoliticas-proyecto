import pulsar,_pulsar  
from pulsar.schema import *

import logging
import traceback
import uuid

from warehouse_ms.modules.outbounds.infrastructure.schema.v1.events import CreatedOrderEvent, EventoOrdenCreada
from warehouse_ms.modules.outbounds.infrastructure.projections import OrderCreatedProjection
from warehouse_ms.seedwork.infrastructure.projections import execute_projection
from warehouse_ms.seedwork.infrastructure import utils

client_connection = f'pulsar://{utils.broker_host()}:6650'

def subscribe_to_created_order_event(app=None):
    _subscribe_to_events(app, 'order-created', 'eds-sub-events', EventoOrdenCreada)

def _subscribe_to_events(app, topic, subscription_name, schema):
    try:
        client = pulsar.Client(client_connection)
        consumer = client.subscribe(topic, consumer_type=_pulsar.ConsumerType.Shared, subscription_name=subscription_name, schema=AvroSchema(schema))

        while True:
            message = consumer.receive()
            data = message.value().data
            print(f'Received event: {data}')

            execute_projection(OrderCreatedProjection(uuid.uuid4(), data.products, data.destiny), app=app)

            consumer.acknowledge(message)

        client.close()
    except:
        logging.error('ERROR: Event topic subscription!')
        traceback.print_exc()
        if client:
            client.close()