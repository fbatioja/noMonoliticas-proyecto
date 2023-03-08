from warehouse_ms.config.db import db
import uuid

Base = db.declarative_base()

class Warehouse(db.Model):
    __tablename__ = "warehouses"
    id = db.Column(db.String(40), primary_key=True, default=str(uuid.uuid4()))
    created_date = db.Column(db.Date)
    modification_date = db.Column(db.Date)
    address = db.Column(db.String(100), nullable=False)

class WarehouseProduct(db.Model):
    __tablename__ = "warehouse_products"
    id = db.Column(db.String(40), primary_key=True, default=str(uuid.uuid4()))
    created_date = db.Column(db.Date)
    modification_date = db.Column(db.Date)
    reference = db.Column(db.String(40), nullable=False)
    warehouse_id = db.Column(db.String(40), db.ForeignKey("warehouses.id"))
    available = db.Column(db.Integer(), nullable=False)
    reserved = db.Column(db.Integer(), nullable=False)

class Product(db.Model):
    __tablename__ = "products"
    id = db.Column(db.String(40), primary_key=True, default=str(uuid.uuid4()))
    reference = db.Column(db.String(40), nullable=False)
    amount = db.Column(db.Integer(), nullable=False)
    outbound_id = db.Column(db.String(40), db.ForeignKey("outbounds.id"))

class Outbound(db.Model):
    __tablename__ = "outbounds"
    id = db.Column(db.String(40), primary_key=True, default=str(uuid.uuid4()))
    created_date = db.Column(db.Date)
    modification_date = db.Column(db.Date)
    order_id = db.Column(db.String(40), nullable=False)
    products = db.relationship('Product', backref='outbound')
    destination = db.Column(db.String(100), nullable=False)

class OutboundEvents(db.Model):
    __tablename__ = "outbound_events"
    id = db.Column(db.String(40), primary_key=True, default=str(uuid.uuid4()))
    entity_id = db.Column(db.String(40), nullable=False)
    event_datetime = db.Column(db.DateTime, nullable=False)
    version = db.Column(db.String(10), nullable=False)
    event_type = db.Column(db.String(100), nullable=False)
    content_type = db.Column(db.String(10), nullable=False)
    service_name = db.Column(db.String(40), nullable=False)
    content = db.Column(db.Text, nullable=False)