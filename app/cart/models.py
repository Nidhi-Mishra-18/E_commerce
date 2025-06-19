from sqlalchemy import Column, ForeignKey, Integer

from sqlalchemy.orm import relationship

from app.core.database import Base

from app.products.models import Products
from app.auth.models import User

# SQLAlchemy model representing the Cart table
class Cart(Base):
    __tablename__ = "cart"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    quantity = Column(Integer, nullable=False)

    user = relationship("User", back_populates="cart_items")
    product = relationship("Products")

