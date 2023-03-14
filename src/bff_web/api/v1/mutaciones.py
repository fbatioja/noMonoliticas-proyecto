import uuid
import strawberry
import typing

from strawberry.types import Info
from bff_web import utils
from bff_web.despachadores import Despachador

from .esquemas import *

@strawberry.type
class Mutation:

    @strawberry.mutation
    async def crear_orden(self, orden: OrdenInput, info: Info) -> OrdenRespuesta:
        print(f"Orden {orden.orderId} con destino {orden.destiny}")
        productosPayload = []
        for producto in orden.products:
            productosPayload.append(dict(amount=10, productReference=producto.productReference))

        payload = dict(
            destiny=orden.destiny,
            products=productosPayload
        )
        comando = dict(
            id = str(uuid.uuid4()),
            time=utils.time_millis(),
            specversion = "v1",
            type = "ComandoCrearOrden",
            ingestion=utils.time_millis(),
            datacontenttype="AVRO",
            service_name = "BFF Web",
            data = payload
        )
        despachador = Despachador()
        info.context["background_tasks"].add_task(despachador.publicar_mensaje, comando, "crear-orden-comando", "public/default/crear-orden-comando")
        
        return OrdenRespuesta(mensaje="Procesando Mensaje", codigo=203)