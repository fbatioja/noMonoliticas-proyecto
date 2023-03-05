from click import DateTime
from order.config.db import db
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, ForeignKey, Integer, String, Table

import uuid

Base = db.declarative_base()

class Order(db.Model):
    __tablename__ = 'order'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    creationDate = db.Column(db.DateTime, nullable=False)
    state = db.Column(db.String(50), nullable=False)
    destiny = db.Column(db.String(50), nullable=False)
    products = db.relationship('Product', back_populates='order')

class Product(db.Model):
    __tablename__ = 'product'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    reference = db.Column(db.String(40), nullable=False)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    order =  db.relationship('Order', back_populates='products')
    quantity = db.Column(db.Integer, nullable=False)
