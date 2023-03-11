from warehouse_ms.modules.outbounds.infrastructure.schema.v1.events import CreatedOrderEvent, CanceledOrderEvent, CreatedOutboundEvent, CanceledOutboundEvent
from warehouse_ms.modules.outbounds.infrastructure.dispatchers import Dispatcher
from warehouse_ms.seedwork.application.handlers import Handler

class OutboundIntegrationHandler(Handler):

    @staticmethod
    def handle_created_order(event: CreatedOrderEvent):
        dispatcher = Dispatcher()
        dispatcher.publish_event(event, 'order-created')

    @staticmethod
    def handle_canceled_order(event: CanceledOrderEvent):
        dispatcher = Dispatcher()
        dispatcher.publish_event(event, 'order-canceled')

    @staticmethod
    def handle_created_outbound(event: CreatedOutboundEvent):
        dispatcher = Dispatcher()
        dispatcher.publish_event(event, 'outbound-created')

    @staticmethod
    def handle_canceled_outbound(event: CanceledOutboundEvent):
        dispatcher = Dispatcher()
        dispatcher.publish_event(event, 'outbound-canceled')