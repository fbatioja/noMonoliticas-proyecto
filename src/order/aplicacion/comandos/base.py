from order.seedwork.aplicacion.comandos import ComandoHandler
from order.infraestructura.fabricas import FabricaRepositorio
from order.dominio.fabricas import FabricaOrden

class CrearOrdenBaseHandler(ComandoHandler):
    def __init__(self):
        self._fabrica_repositorio: FabricaRepositorio = FabricaRepositorio()
        self._fabrica_orden: FabricaOrden = FabricaOrden()

    @property
    def fabrica_repositorio(self):
        return self._fabrica_repositorio
    
    @property
    def fabrica_orden(self):
        return self._fabrica_orden
    