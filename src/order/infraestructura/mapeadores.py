
from order.seedwork.dominio.repositorios import Mapeador
from order.seedwork.infraestructura.utils import unix_time_millis
from order.dominio.objetos_valor import EstadoOrden, Direccion
from order.dominio.entidades import Producto, Orden
#from aeroalpes.modulos.vuelos.dominio.eventos import ReservaAprobada, ReservaCancelada, ReservaAprobada, ReservaPagada, ReservaCreada, EventoReserva

from .dto import Order as OrdenDTO
from .dto import Product as ProductoDTO
from .excepciones import NoExisteImplementacionParaTipoFabricaExcepcion

class MapeadorOrden(Mapeador):
    _FORMATO_FECHA = '%Y-%m-%dT%H:%M:%SZ'

    def obtener_tipo(self) -> type:
        return Orden.__class__

    def entidad_a_dto(self, entidad: Orden) -> OrdenDTO:
        
        orden_dto = OrdenDTO()
        orden_dto.creationDate = entidad.fecha_creacion
        orden_dto.destiny = entidad.destino.direccion
        orden_dto.state = entidad.estado.value
        
        #TODO guardar productos
        orden_dto.products = []

        return orden_dto

    def dto_a_entidad(self, dto: OrdenDTO) -> Orden:
        orden = Orden(destino=dto.destiny, fecha_creacion=dto.creationDate, estado=dto.state)
        orden.productos = list()

        productos_dto: list[ProductoDTO] = dto.products

        # TODO: Agregar manejo de productos
        #orden.productos.extend(self._procesar_itinerario_dto(productos_dto))
        
        return orden