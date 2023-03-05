from .entidades import Orden
from .excepciones import TipoObjetoNoExisteEnDominioOrdenesExcepcion
from order.seedwork.dominio.repositorios import Mapeador, Repositorio
from order.seedwork.dominio.fabricas import Fabrica
from order.seedwork.dominio.entidades import Entidad
from order.seedwork.dominio.eventos import EventoDominio
from dataclasses import dataclass

@dataclass
class FabricaOrden(Fabrica):
    def crear_objeto(self, obj: any, mapeador: Mapeador) -> any:
        if isinstance(obj, Entidad) or isinstance(obj, EventoDominio):
            return mapeador.entidad_a_dto(obj)
        else:
            orden: Orden = mapeador.dto_a_entidad(obj)            
            return orden