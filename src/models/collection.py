from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from src.models.base import Base

class Collection(Base):
    __tablename__ = 'collection'

    collection_id = Column(Integer, primary_key=True, autoincrement=True)
    collection_name = Column(String(50), nullable=False)
    collection_description = Column(String)
