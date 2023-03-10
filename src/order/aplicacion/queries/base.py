from order.infraestructura.fabricas import FabricaRepositorio
from order.seedwork.aplicacion.queries import QueryHandler
from order.dominio.fabricas import FabricaOrden

class OrdenQueryBaseHandler(QueryHandler):
    def __init__(self):
        self._fabrica_repositorio: FabricaRepositorio = FabricaRepositorio()
        self._fabrica_vuelos: FabricaOrden = FabricaOrden()
    
    @property
    def fabrica_vuelos(self):
        return self._fabrica_vuelos
    
    @property
    def fabrica_repositorio(self):
        return self._fabrica_repositorio
    