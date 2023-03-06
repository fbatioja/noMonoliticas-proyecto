from dataclasses import dataclass, field
from order.seedwork.aplicacion.dto import DTO

@dataclass(frozen=True)
class ProductDTO(DTO):
    product_reference: str = field(default_factory=str)
    quantity: int = field(default_factory=int)


@dataclass(frozen=True)
class OrderDTO(DTO):
    state: str = field(default_factory=str)
    order_id: str = field(default_factory=str)
    destiny: str = field(default_factory=str)
    products: list[ProductDTO] = field(default_factory=list)



