from warehouse_ms.seedwork.domain.rules import BusinessRule
from warehouse_ms.modules.outbounds.domain.value_objects import WarehouseOrder, ProductOrder, Location

class ValidAvailableStock(BusinessRule):

    available_stock: int

    def __init__(self, available_stock, message='Stock available units must be equals or greather than zero'):
        super().__init__(message)
        self.available_stock = available_stock

    def is_valid(self) -> bool:
        return self.available_stock >= 0

class ValidReservedStock(BusinessRule):

    reserved_stock: int

    def __init__(self, reserved_stock, message='Stock reserverd units must be equals or greather than zero'):
        super().__init__(message)
        self.reserved_stock = reserved_stock

    def is_valid(self) -> bool:
        return self.reserved_stock >= 0

class ValidWarehouseOrder(BusinessRule):

    warehouse_order: WarehouseOrder

    def __init__(self, warehouse_order, message='Invalid products quantity'):
        super().__init__(message)
        self.warehouse_order = warehouse_order

    def is_valid(self) -> bool:
        return self.warehouse_order.has_products()

class ValidProductOrder(BusinessRule):

    product_order: ProductOrder

    def __init__(self, product_order, message='Invalid products quantity'):
        super().__init__(message)
        self.product_order = product_order

    def is_valid(self) -> bool:
        return self.product_order.has_products()

class ValidLocation(BusinessRule):

    location: Location

    def __init__(self, location, message='Invalid location address'):
        super().__init__(message)
        self.location = location

    def is_valid(self) -> bool:
        return self.location != ""