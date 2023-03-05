from warehouse_ms.seedwork.domain.repositories import Mapper
from warehouse_ms.seedwork.infrastructure.utils import unix_time_millis
from warehouse_ms.modules.outbounds.domain.value_objects import Amount, Location, Reference, WarehouseProduct, OutboundProduct, WarehouseOrder, ProductOrder
from warehouse_ms.modules.outbounds.domain.entities import Warehouse, Product, Outbound
from warehouse_ms.modules.outbounds.domain.events import OrderCreated, OrderCanceled, OutboundCreated, OutboundCanceled, OutboundEvent

from .dto import Warehouse as WarehouseDTO
from .dto import WarehouseProduct as WarehouseProductDTO
from .dto import Product as ProductDTO
from .dto import Outbound as OutboundDTO
from .exceptions import ImplementationDoesNotExistsForFactoryTypeException
from pulsar.schema import *

class WarehouseMapper(Mapper):

    def get_type(self) -> type:
        return Warehouse.__class__

    def entity_to_dto(self, entity: Warehouse) -> WarehouseDTO:
        warehouse_dto = WarehouseDTO()
        warehouse_dto.id = str(entity.id)
        warehouse_dto.created_date = entity.created_date
        warehouse_dto.modification_date = entity.modification_date
        warehouse_dto.address = entity.location.address

        return warehouse_dto

    def dto_to_entity(self, dto: WarehouseDTO) -> Warehouse:
        location = Location(dto.address)

        warehouse = Warehouse(dto.id, dto.created_date, dto.modification_date, location)
        
        return warehouse

class WarehouseProductMapper(Mapper):

    def get_type(self) -> type:
        return Product.__class__

    def entity_to_dto(self, entity: Product) -> WarehouseProductDTO:
        product_dto = WarehouseProductDTO()
        product_dto.id = str(entity.id)
        product_dto.created_date = entity.created_date
        product_dto.modification_date = entity.modification_date
        product_dto.reference = entity.warehouse_product.reference.productReference
        product_dto.warehouse_id = str(entity.warehouse_id)
        product_dto.available = entity.available
        product_dto.reserved = entity.reserved

        return product_dto

    def dto_to_entity(self, dto: WarehouseProductDTO) -> Product:
        reference = Reference(dto.reference)
        warehouse_product = WarehouseProduct(reference)

        product = Product(dto.id, dto.created_date, dto.modification_date, warehouse_product, dto.warehouse_id, dto.available, dto.reserved)
        
        return product
    
class OutboundMapper(Mapper):

    def get_type(self) -> type:
        return Outbound.__class__
    
    def _process_order_products_dto(self, products_dto: list[ProductDTO]) -> WarehouseOrder:
        products = list()
        warehouse_order = WarehouseOrder()

        for product_dto in products_dto:
            reference = Reference(product_dto.reference)
            amount = Amount(product_dto.amount)
            product = OutboundProduct(reference, amount)
            
            products.append(product)

        warehouse_order.products = products
        return warehouse_order
    
    def _process_order_products(self, order: ProductOrder) -> list[ProductDTO]:
        products_dto = list()

        for product in order:
            product_dto = ProductDTO()
            product_dto.reference = product.productReference
            product_dto.amount = product.amount

            products_dto.append(product_dto)

        return products_dto
    
    def entity_to_dto(self, entity: Outbound) -> OutboundDTO:
        outbound_dto = OutboundDTO()
        outbound_dto.id = str(entity.id)
        outbound_dto.created_date = entity.created_date
        outbound_dto.modification_date = entity.modification_date
        outbound_dto.order_id = str(entity.order_id)
        outbound_dto.destination = str(entity.destination.address)

        products_dto = list()
        products_dto.extend(self._process_order_products(entity.product_order))
            
        outbound_dto.products = products_dto

        return outbound_dto
    
    def dto_to_entity(self, dto: OutboundDTO) -> Outbound:
        destination = Location(dto.destination)
        outbound = Outbound(id=dto.id, created_date=dto.created_date, modification_date=dto.modification_date, order_id=dto.order_id, destination=destination)

        outbound.product_order = self._process_order_products_dto(dto.products)
        
        return outbound

class OutboundEventsMapper(Mapper):

    # Versiones aceptadas
    versions = ('v1',)

    LATEST_VERSION = versions[0]

    def __init__(self):
        self.router = {
            OrderCreated: self._entity_to_created_order,
            OrderCanceled: self._entity_to_canceled_order,
            OutboundCreated: self._entity_to_created_outbound,
            OutboundCanceled: self._entity_to_canceled_outbound
        }

    def get_type(self) -> type:
        return OutboundEvent.__class__

    def is_valid_version(self, version):
        for v in self.versions:
            if v == version:
                return True
        return False

    def _entity_to_created_order(self, entity: OrderCreated, version=LATEST_VERSION):
        def v1(event):
            from .schema.v1.events import CreatedOrderPayload, CreatedOrderEvent

            payload = CreatedOrderPayload(
                order_id=str(event.order_id), 
                products=str(event.products), 
                destination=str(event.destination), 
                created_date=int(unix_time_millis(event.created_date))
            )
            evento_integracion = CreatedOrderEvent(id=str(event.id))
            evento_integracion.id = str(event.id)
            evento_integracion.time = int(unix_time_millis(event.fecha_creacion))
            evento_integracion.specversion = str(version)
            evento_integracion.type = 'OrderCreated'
            evento_integracion.datacontenttype = 'AVRO'
            evento_integracion.service_name = 'eds'
            evento_integracion.data = payload

            return evento_integracion
                    
        if not self.is_valid_version(version):
            raise Exception(f'Unknown implementation of version {version}')

        if version == 'v1':
            return v1(entity)       

    def _entity_to_canceled_order(self, entity: OrderCanceled, version=LATEST_VERSION):
        # TODO
        raise NotImplementedError
    
    def _entity_to_created_outbound(self, entity: OutboundCreated, version=LATEST_VERSION):
        # TODO
        raise NotImplementedError
    
    def _entity_to_canceled_outbound(self, entity: OutboundCanceled, version=LATEST_VERSION):
        # TODO
        raise NotImplementedError

    def entity_to_dto(self, entity: OutboundEvent, version=LATEST_VERSION) -> OutboundDTO:
        if not entity:
            raise ImplementationDoesNotExistsForFactoryTypeException
        func = self.router.get(entity.__class__, None)

        if not func:
            raise ImplementationDoesNotExistsForFactoryTypeException

        return func(entity, version=version)

    def dto_to_entity(self, dto: OutboundDTO, version=LATEST_VERSION) -> Outbound:
        raise NotImplementedError