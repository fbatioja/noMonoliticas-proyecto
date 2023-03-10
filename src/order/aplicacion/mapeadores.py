from order.seedwork.aplicacion.dto import Mapeador as AppMap
from order.seedwork.dominio.repositorios import Mapeador as RepMap
from order.dominio.entidades import Orden, Producto
from order.dominio.objetos_valor import Direccion, EstadoOrden
from .dto import OrderDTO,ProductDTO

from datetime import datetime

class MapeadorOrdenDTOJson(AppMap):
    def _procesar_orden(self, orden: dict) -> OrderDTO:
        productos_dto: list[ProductDTO] = list()
        return OrderDTO(productos_dto)

    def _procesar_producto(self, producto: dict) -> ProductDTO:
        productos_dto: list[ProductDTO] = list()
        return OrderDTO(productos_dto)
    
    def externo_a_dto(self, externo: dict) -> OrderDTO:
        
        productos: list[ProductDTO] = list()
        for item in externo.get('products', list()):
            producto:Producto = Producto(referencia=item.get('productReference'),cantidad=item.get('amount'))
            productos.append(producto)  
        
        orden_dto = OrderDTO(destiny=externo.get('destiny'), products=productos)
        return orden_dto

    def dto_a_externo(self, dto: OrderDTO) -> dict:
        return dto.__dict__


class MapeadorOrden(RepMap):
    _FORMATO_FECHA = '%Y-%m-%dT%H:%M:%SZ'

    def _procesar_orden(self, orden_dto: OrderDTO) -> Orden:
        productos = list()

        for product_dto in orden_dto.products:
            
            producto:Producto = Producto(referencia=product_dto.product_reference,cantidad=product_dto.quantity)
            productos.append(producto)   
                   
        return Orden(productos)

    def obtener_tipo(self) -> type:
        return Orden.__class__

    def dto_a_entidad(self, dto: OrderDTO) -> Orden:
        orden = Orden(destino=Direccion(dto.destiny), estado=EstadoOrden.ENPROCESO, productos=dto.products)
        return orden

    def entidad_a_dto(self, entidad: Orden) -> OrderDTO:

        state = entidad.estado
        destiny = entidad.destino
        order_id = str(entidad.id)
        products = list()

        for item in entidad.productos:
            product_reference =item.referencia 
            quantity = item.cantidad
            producto_dto = ProductDTO(product_reference=product_reference, quantity=quantity)
            products.append(producto_dto)
        
        return OrderDTO(state, order_id, destiny, products)

