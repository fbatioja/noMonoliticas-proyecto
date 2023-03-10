from order.dominio.entidades import Orden, Producto
from order.infraestructura.schema.v1.comandos import ComandoCrearOrden
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
    destiny: str
    products: list[ProductDTO]

class CrearOrdenHandler(CrearOrdenBaseHandler):

    def handle(self, comando: CrearOrden):
        
        order_dto = OrderDTO(
                state = EstadoOrden.ENPROCESO
            ,   destiny=comando.destiny
            ,   products=comando.products)            
        
        orden: Orden = self.fabrica_orden.crear_objeto(order_dto, MapeadorOrden())
        orden.crear_orden(orden)

        repositorio = self.fabrica_repositorio.crear_objeto(RepositorioOrdenes)
        repositorio.agregar(orden)

@comando.register(ComandoCrearOrden)
def ejecutar_comando_crear_orden(comando):
    handler = CrearOrdenHandler()
    productos: list[Producto] = list()
    for item in comando.data.products:
        producto:Producto = Producto(referencia=item.productReference,cantidad=item.amount)
        productos.append(producto)  

    data = CrearOrden(
        destiny=comando.data.destiny,
        products=productos
    )
    handler.handle(data)
    