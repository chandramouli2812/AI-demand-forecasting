from sqlalchemy import Column, Integer, Float, String, Date
from .database import Base

class SalesData(Base):
    __tablename__ = "sales"

    id = Column(Integer, primary_key=True)
    date = Column(Date)
    category = Column(String)
    quantity = Column(Integer)