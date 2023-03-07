
from order.config.db import db
from order.dominio.eventos import OrdenCreada
from order.seedwork.dominio.repositorios import Mapeador
from order.seedwork.infraestructura.utils import unix_time_millis
from order.dominio.objetos_valor import EstadoOrden, Direccion
from order.dominio.entidades import Producto, Orden

from .dto import Order as OrdenDTO
from .dto import Product as ProductoDTO
from .excepciones import NoExisteImplementacionParaTipoFabricaExcepcion

from pulsar.schema import *

class MapadeadorEventosOrden(Mapeador):

    # Versiones aceptadas
    versions = ('v1',)

    LATEST_VERSION = versions[0]

    def __init__(self):
        self.router = {
            Orden: self._entidad_a_orden_creada,
        }

    def obtener_tipo(self) -> type:
        return OrdenCreada.__class__

    def es_version_valida(self, version):
        for v in self.versions:
            if v == version:
                return True
        return False

    def _entidad_a_orden_creada(self, entidad: OrdenCreada, version=LATEST_VERSION):
        def v1(evento):
            from .schema.v1.eventos import EventoOrdenCreada, OrdenCreadaPayload, ProductoPayload

            productsPayload = []
            for producto in evento.productos:
                productoPayload = ProductoPayload(
                    amount=int(producto.cantidad),
                    productReference=str(producto.referencia)
                )
                productsPayload.append(productoPayload)

            payload = OrdenCreadaPayload( 
                destiny=str(evento.destino.direccion), 
                products=productsPayload, 
            )

            evento_integracion = EventoOrdenCreada(id=str(evento.id))
            evento_integracion.id = str(evento.id)
            evento_integracion.time = int(unix_time_millis(evento.fecha_creacion))
            evento_integracion.specversion = str(version)
            evento_integracion.type = 'OrdenCreada'
            evento_integracion.datacontenttype = 'AVRO'
            evento_integracion.service_name = 'orden'
            evento_integracion.data = payload

            return evento_integracion
                    
        if not self.es_version_valida(version):
            raise Exception(f'No se sabe procesar la version {version}')

        if version == 'v1':
            return v1(entidad)

    def entidad_a_dto(self, entidad: OrdenCreada, version=LATEST_VERSION) -> OrdenDTO:
        if not entidad:
            raise NoExisteImplementacionParaTipoFabricaExcepcion
        func = self.router.get(entidad.__class__, None)
        if not func:
            raise NoExisteImplementacionParaTipoFabricaExcepcion

        return func(entidad, version=version)

    def dto_a_entidad(self, dto: OrdenDTO, version=LATEST_VERSION) -> Orden:
        raise NotImplementedError


class MapeadorOrden(Mapeador):
    def obtener_tipo(self) -> type:
        return Orden.__class__

    def entidad_a_dto(self, entidad: Orden) -> OrdenDTO:
        
        orden_dto = OrdenDTO()
        orden_dto.creationDate = entidad.fecha_creacion
        orden_dto.destiny = entidad.destino.direccion
        orden_dto.state = entidad.estado.value
        
        productos_dto = []
        for producto in entidad.productos:
            producto_dto = ProductoDTO(quantity=producto.cantidad, reference=producto.referencia)
            productos_dto.append(producto_dto)

        orden_dto.products = productos_dto

        return orden_dto

    def dto_a_entidad(self, dto: OrdenDTO) -> Orden:
        orden = Orden(destino=dto.destiny, fecha_creacion=dto.creationDate, estado=dto.state)
        orden.productos = list()
        productos = []
        for producto_dto in dto.products:
            producto = Producto(cantidad=producto_dto.quantity, referencia=producto_dto.reference)
            productos.append(producto)

        orden.productos = productos
        return orden