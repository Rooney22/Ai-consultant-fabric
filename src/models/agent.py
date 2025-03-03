from sqlalchemy import Column, String, ForeignKey, Integer
from sqlalchemy.orm import relationship
from src.models.base import Base


class Agent(Base):
    __tablename__ = 'agent'
    agent_id = Column(Integer, primary_key=True)
    agent_name = Column(String(50))
    agent_prompt = Column(String(255))
