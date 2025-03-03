from sqlalchemy import Column, String, ForeignKey, Integer
from sqlalchemy.orm import relationship
from src.models.base import Base

from src.models.agent import Agent
from src.models.collection import Collection


class AgentCollection(Base):
    __tablename__ = 'agent_collection'
    agent_id = Column(Integer, ForeignKey('agent.agent_id'), primary_key=True)
    collection_id = Column(Integer, ForeignKey('collection.collection_id'), primary_key=True)

    agent = relationship('Agent', back_populates='collections')
    collection = relationship('Collection', back_populates='agents')
