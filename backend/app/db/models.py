from sqlalchemy import Column, Integer, String, Text
from .database import Base


class SalesData(Base):
    __tablename__ = "sales"

    id = Column(Integer, primary_key=True)
    date = Column(String)
    category = Column(String)
    quantity = Column(Integer)


class ModelMetadata(Base):
    __tablename__ = "model_metadata"

    id = Column(Integer, primary_key=True)
    key = Column(String, unique=True, index=True)
    value = Column(Text)