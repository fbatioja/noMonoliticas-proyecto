import time
import typing
import strawberry
import requests
import os
import uuid
from pulsar.schema import *

from bff_web import utils
from bff_web.despachadores import Despachador
from strawberry.types import Info

@strawberry.type
class Producto:
    productReference: str
    amount: str

@strawberry.type
class Orden:
    orderId: str
    products: typing.List[Producto]
    destiny: str

@strawberry.type
class OrdenRespuesta:
    mensaje: str
    codigo: int


@strawberry.input
class ProductoInput:
    productReference: str
    amount: int

@strawberry.input
class OrdenInput:
    orderId: str
    products: typing.List[ProductoInput]
    destiny: str


EDA_HOST = os.getenv("EDA_ADDRESS", default="localhost:5000")

def obtener_ordenes(root) -> typing.List["Orden"]:
    ordenes_json = requests.get(f'http://{EDA_HOST}/orden-query').json()
    ordenes = []

    for orden in ordenes_json:
        productos = []
        for producto in orden.get('products', []):
            
            productos.append(Producto(productReference=producto.get('product_reference'), amount=producto.get('quantity')))

        ordenes.append(
            Orden(
                orderId=orden.get('order_id'), 
                destiny=orden.get('destiny', ''),
                products=productos
            )
        )

    return ordenes

def obtener_ordenes_asincrono(info: Info) -> OrdenRespuesta:
    comando = dict(
        id = str(uuid.uuid4()),
        time=utils.time_millis(),
        specversion = "v1",
        type = "QueryGenerarListadoOrdenes",
        ingestion=utils.time_millis(),
        datacontenttype="AVRO",
        service_name = "BFF Web",
        data = ''
    )
    despachador = Despachador()
    info.context["background_tasks"].add_task(despachador.publicar_mensaje, comando, "listado-ordenes-generado-comando", "public/default/listado-ordenes-generado-comando")
    
    return OrdenRespuesta(mensaje="Procesando Mensaje", codigo=203)
