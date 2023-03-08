import pulsar
from pulsar.schema import *

from warehouse_ms.seedwork.infrastructure import utils

from warehouse_ms.modules.outbounds.infrastructure.mappers import OutboundEventsMapper

class Dispatcher:
    def __init__(self):
        self.mapper = OutboundEventsMapper()

    def _publish_message(self, message, topic, schema):
        client = pulsar.Client(f'pulsar://{utils.broker_host()}:6650')
        publisher = client.create_producer(topic, schema=schema)
        publisher.send(message)
        client.close()

    def publish_event(self, event, topic):
        event = self.mapper.entity_to_dto(event)
        self._publish_message(event, topic, AvroSchema(event.__class__))
