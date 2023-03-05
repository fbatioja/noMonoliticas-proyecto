from order.config.db import db
from order.dominio.repositorios import RepositorioOrdenes
from order.dominio.objetos_valor import Direccion, EstadoOrden
from order.dominio.entidades import Orden, Producto
from order.dominio.fabricas import FabricaOrden
from order.dominio.entidades import Orden
from order.dominio.fabricas import FabricaOrden
from .dto import Order as OrdenDTO
from .mapeadores import MapeadorOrden
from uuid import UUID
from pulsar.schema import *

class RepositorioOrdenesSQLAlchemy(RepositorioOrdenes):

    def __init__(self):
        self._fabrica_ordenes: FabricaOrden = FabricaOrden()

    @property
    def fabrica_ordenes(self):
        return self._fabrica_ordenes

    def obtener_por_id(self, id: UUID) -> Orden:
        orden_dto = db.session.query(OrdenDTO).filter_by(id=str(id)).one()
        return self.fabrica_ordenes.crear_objeto(orden_dto, MapeadorOrden())

    def obtener_todos(self) -> list[Orden]:
        # TODO
        raise NotImplementedError

    def agregar(self, orden: Orden):
        orden_dto = self.fabrica_ordenes.crear_objeto(orden, MapeadorOrden())
        db.session.add(orden_dto)
        db.session.commit()

    def actualizar(self, orden: Orden):
        # TODO
        raise NotImplementedError

    def eliminar(self, orden_id: UUID):
        # TODO
        raise NotImplementedError