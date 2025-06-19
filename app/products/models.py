from sqlalchemy import Column, String, Integer,Float

from app.core.database import Base

# SQLAlchemy model for Products table
class Products(Base):
    __tablename__="products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String)
    price = Column(Float, nullable=False)
    stock = Column(Integer, nullable=False)
    category = Column(String)
    image_url = Column(String)