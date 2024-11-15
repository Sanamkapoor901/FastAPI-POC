from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Product(Base):
    __tablename__ = "products"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    price = Column(Float)
    quantity = Column(Integer)
    
    # Add the user_id as a foreign key to the User table
    created_by = Column(Integer, ForeignKey("users.id"))
    
    # Define the relationship to the User model
    user = relationship("User", back_populates="products")

