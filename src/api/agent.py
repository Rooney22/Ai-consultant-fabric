from fastapi import APIRouter, Depends, UploadFile, status, HTTPException, File
from src.services.agent import AgentService
from src.models.schemas.agent.agent_request import AgentRequest
from typing import List


router = APIRouter(
    prefix='/agent',
    tags=['agent'],
)


@router.get("/collections/get")
async def read_collections():
    result = await AgentService.get_collections()
    collections = [row for row in result.scalars()]
    return {"collections": collections}

    

@router.get("/agents/get")
async def read_agents():
    result = await AgentService.get_agents()
    agents = [row for row in result.scalars()]
    return {"agents": agents}

    
@router.post("/agents/create")
async def create_agent_endpoint(agent_data: AgentRequest):
    print(agent_data)
    await AgentService.create_agent(
        agent_name=agent_data.agent_name,
        agent_prompt=agent_data.agent_prompt,
        collection_name=agent_data.collection_name
    )
    return {"message": "Agent created successfully"}

@router.get("/answer/")
async def get_answer_endpoint(agent_name: str, user_question: str):
    try:
        answer = await AgentService.get_answer(agent_name=agent_name, user_question=user_question)
        return {"answer": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.post("/collections/create")
async def create_collection_endpoint(
    collection_name: str,
    collection_description: str,
    files: List[UploadFile] = File(...)
):
        for file in files:
            if not file.filename.endswith('.pdf'):
                raise HTTPException(status_code=400, detail="Неподдерживаемый формат файла. Поддерживаются только PDF файлы.")

        await AgentService.create_collection(collection_name=collection_name, input_files=files, collection_description=collection_description)
        return {"message": f"Коллекция '{collection_name}' успешно создана"}
