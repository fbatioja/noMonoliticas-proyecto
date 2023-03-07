from order.config.db import db
from order.dominio.eventos import OrdenCreada
from order.dominio.repositorios import RepositorioOrdenes
from order.dominio.objetos_valor import Direccion, EstadoOrden
from order.dominio.entidades import Orden, Producto
from order.dominio.fabricas import FabricaOrden
from order.dominio.entidades import Orden
from order.dominio.fabricas import FabricaOrden
from .dto import Order as OrdenDTO, Product
from .mapeadores import MapeadorOrden
from uuid import UUID
from pulsar.schema import *
from pydispatch import dispatcher

class RepositorioOrdenesSQLAlchemy(RepositorioOrdenes):

    def __init__(self):
        self._fabrica_ordenes: FabricaOrden = FabricaOrden()

    @property
    def fabrica_ordenes(self):
        return self._fabrica_ordenes

    def obtener_por_id(self, id: Integer) -> Orden:
        orden_dto = db.session.query(OrdenDTO).filter_by(id=str(id)).one()
        return self.fabrica_ordenes.crear_objeto(orden_dto, MapeadorOrden())

    def obtener_todos(self) -> list[Orden]:
        ordenes_dto = db.session.query(OrdenDTO).all()
        return [self.fabrica_ordenes.crear_objeto(orden_dto, MapeadorOrden()) for orden_dto in ordenes_dto]

    def agregar(self, orden: Orden):
        orden_dto = self.fabrica_ordenes.crear_objeto(orden, MapeadorOrden())
        db.session.add(orden_dto)
        db.session.commit()
        try:
            self._publicar_eventos_post_commit(orden)
        except Exception as e:
            print("Error al publicar el evento: ", e)

    def actualizar(self, orden: Orden):
        # TODO
        raise NotImplementedError

    def eliminar(self, orden_id: UUID):
        # TODO
        raise NotImplementedError
    
    def _publicar_eventos_post_commit(self, evento):
        dispatcher.send(signal=f'{OrdenCreada.__name__}Integracion', evento=evento)