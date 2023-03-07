from order.dominio.entidades import Orden
from order.seedwork.aplicacion.comandos import Comando
from order.aplicacion.dto import OrderDTO, ProductDTO
from .base import CrearOrdenBaseHandler
from dataclasses import dataclass, field
from order.seedwork.aplicacion.comandos import ejecutar_commando as comando
from order.dominio.objetos_valor import EstadoOrden
from order.infraestructura.fabricas import FabricaRepositorio
from order.aplicacion.mapeadores import MapeadorOrden
from order.dominio.fabricas import FabricaOrden
from order.dominio.repositorios import RepositorioOrdenes

@dataclass
class CrearOrden(Comando):
    state: str
    orderId: str
    destiny: str
    products: list[ProductDTO]

class CrearOrdenHandler(CrearOrdenBaseHandler):

   
    def handle(self, comando: CrearOrden):
        
        order_dto = OrderDTO(
                state = EstadoOrden.ENPROCESO
            ,   order_id=comando.orderId
            ,   destiny=comando.destiny
            ,   products=comando.products)            
        
        orden: Orden = self.fabrica_orden.crear_objeto(order_dto, MapeadorOrden())
        orden.crear_orden(orden)

        repositorio = self.fabrica_repositorio.crear_objeto(RepositorioOrdenes)
        repositorio.agregar(orden)
        
        #UnidadTrabajoPuerto.registrar_batch(repositorio.agregar, reserva)
        #UnidadTrabajoPuerto.savepoint()
        #UnidadTrabajoPuerto.commit()
        


@comando.register(CrearOrden)
def ejecutar_comando_crear_orden(comando: CrearOrden):
    handler = CrearOrdenHandler()
    handler.handle(comando)
    