
from pydantic import BaseModel


class AgentRequest(BaseModel):
    agent_name: str
    agent_prompt: str
    collection_name: str