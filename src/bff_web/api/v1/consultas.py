
import strawberry
from .esquemas import *

@strawberry.type
class Query:
    ordenes: typing.List[Orden] = strawberry.field(resolver=obtener_ordenes)

    @strawberry.field
    def ordenes_asincrono(info: Info) -> OrdenRespuesta:
        return obtener_ordenes_asincrono(info)