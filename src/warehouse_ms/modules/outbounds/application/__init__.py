from pydispatch import dispatcher

from .handlers import OutboundIntegrationHandler

from warehouse_ms.modules.outbounds.domain.events import OrderCreated, OrderCanceled, OutboundCreated, OutboundCanceled

dispatcher.connect(OutboundIntegrationHandler.handle_created_order, signal=f'{OrderCreated.__name__}Integration')
dispatcher.connect(OutboundIntegrationHandler.handle_canceled_order, signal=f'{OrderCanceled.__name__}Integration')
dispatcher.connect(OutboundIntegrationHandler.handle_created_outbound, signal=f'{OutboundCreated.__name__}Integration')
dispatcher.connect(OutboundIntegrationHandler.handle_canceled_outbound, signal=f'{OutboundCanceled.__name__}Integration')