from dataclasses import dataclass, field
from order.seedwork.dominio.fabricas import Fabrica
from order.seedwork.dominio.repositorios import Repositorio
from order.dominio.repositorios import RepositorioOrdenes
from .repositories import RepositorioOrdenesSQLAlchemy
from .excepciones import ExcepcionFabrica

@dataclass
class FabricaRepositorio(Fabrica):
    def crear_objeto(self, obj: type, mapeador: any = None) -> Repositorio:
        if obj == RepositorioOrdenes:
            return RepositorioOrdenesSQLAlchemy()
        else:
            raise ExcepcionFabrica(f'No existe fábrica para el objeto {obj}')
