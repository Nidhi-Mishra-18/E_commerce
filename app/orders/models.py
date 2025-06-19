from datetime import datetime
from sqlalchemy import Column, DateTime, Enum, Float, ForeignKey, Integer
from sqlalchemy.orm import relationship

from app.core.database import Base
from app.auth.models import User
from app.products.models import Products

import enum

# Enum for order status
class OrderStatus(str,enum.Enum):
    pending="pending"
    paid="paid"
    cancelled="cancelled"


# SQLAlchemy model for Orders table
class Orders(Base):
    __tablename__="orders"

    id = Column(Integer,primary_key=True,index=True)
    user_id = Column(Integer,ForeignKey("users.id"))
    total_amount = Column(Float, nullable=False)
    status = Column(Enum(OrderStatus,name="order_status"),nullable=False,default="pending")
    created_at = Column(DateTime,default=datetime.utcnow)

    user = relationship("User", back_populates="orders")
    items = relationship("OrderItem", back_populates="order")


# SQLAlchemy model for OrderItem table
class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    quantity = Column(Integer, nullable=False)
    price_at_purchase = Column(Float, nullable=False)

    order = relationship("Orders", back_populates="items")
    product = relationship("Products")
        

