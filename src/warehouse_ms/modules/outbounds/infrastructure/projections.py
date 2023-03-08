from warehouse_ms.seedwork.infrastructure.projections import Projection, ProjectionHandler
from warehouse_ms.seedwork.infrastructure.projections import execute_projection as projection
from warehouse_ms.modules.outbounds.infrastructure.factories import RepositoryFactory
from warehouse_ms.modules.outbounds.infrastructure.repositories import OutboundsRepository, WarehouseProductsRepository
from warehouse_ms.modules.outbounds.domain.entities import Outbound
import warehouse_ms.modules.outbounds.domain.value_objects as vo
from warehouse_ms.modules.outbounds.infrastructure.dto import Outbound as OutboundDTO

from warehouse_ms.seedwork.infrastructure.utils import millis_to_datetime
import datetime
import logging
import traceback
from abc import ABC, abstractmethod

class OutboundsProjection(Projection, ABC):
    @abstractmethod
    def execute(self):
        ...

class OutboundProjectionHandler(ProjectionHandler):
    
    def handle(self, projection: OutboundsProjection):

        from warehouse_ms.config.db import db

        projection.execute(db=db)

class OrderCreatedProjection(OutboundsProjection):
    def __init__(self, order_id, product_order, destination):
        self.outbound_id = id
        self.order_id = order_id
        self.product_order = product_order
        self.destination = vo.Location(destination)
    
    def execute(self, db=None):
        if not db:
            logging.error('ERROR: app DB cannot be null')
            return
        
        # outbound creation
        repository_factory = RepositoryFactory()
        repository = repository_factory.create_object(OutboundsRepository)

        outbound= Outbound(
                id=str(self.outbound_id), 
                order_id=str(self.order_id), 
                product_order=self.product_order,
                destination=self.destination)

        outbound.create_outbound()

        repository.add(outbound)

        # warehouse product updating
        product_repository = repository_factory.create_object(WarehouseProductsRepository)

        for order_product in outbound.product_order:
            product = product_repository.find_by_id(order_product.productReference)
            product.order_stock(order_product.amount)
            product_repository.update(product)

@projection.register(OrderCreatedProjection)
def execute_outbound_projection(projection, app=None):
    if not app:
        logging.error('ERROR: app context cannot be null')
        return
    try:
        with app.app_context():
            handler = OutboundProjectionHandler()
            handler.handle(projection)
            
    except:
        traceback.print_exc()
        logging.error('ERROR: Saving!')