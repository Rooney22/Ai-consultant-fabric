from fastapi import APIRouter, Depends, UploadFile, status, HTTPException, File
from src.services.agent import AgentService
from src.models.schemas.agent.agent_request import AgentRequest
from src.models.agent import Agent
from typing import List


router = APIRouter(
    prefix='/agent',
    tags=['agent'],
)

@router.get("/get")
async def read_agents():
    result = await AgentService.get_agents()
    agents = [{"agent_id": row.agent_id, "agent_name": row.agent_name, 'agent_prompt': row.agent_prompt} for row in result]
    return agents

    
@router.post("/create")
async def create_agent_endpoint(agent_data: AgentRequest):
    await AgentService.create_agent(
        agent_name=agent_data.agent_name,
        agent_prompt=agent_data.agent_prompt,
        collection_name=agent_data.collection_name
    )
    return {"message": "Agent created successfully"}

@router.get("/answer")
async def get_answer_endpoint(agent_name: str, user_question: str):
    try:
        answer = await AgentService.get_answer(agent_name=agent_name, user_question=user_question)
        return {"answer": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/update_prompt")
async def update_prompt(
    agent_id: int,
    new_prompt: str,
):
    updated_agent = await AgentService.update_agent_prompt(agent_id, new_prompt)

    if not updated_agent:
        raise HTTPException(status_code=404, detail="Агент с указанным ID не найден")
    return {"message": "prompt changed successfully"}
