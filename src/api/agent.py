from fastapi import APIRouter, Depends, UploadFile, status, HTTPException, File
from src.services.agent import AgentService
from models.schemas.agent.agent_request import AgentRequest
from typing import List


router = APIRouter(
    prefix='/agent',
    tags=['agent'],
)


@router.post("/inputCSV", status_code=status.HTTP_200_OK, name="Ввод данных формата csv")
async def input_data(file: UploadFile, methods_service: AgentService = Depends()):
    return await methods_service.insert(file.file)

@router.get("/collections/get")
async def read_collections():
    try:
        result = await AgentService.get_collections()
        collections = [row.collection_name for row in result.scalars()]
        return {"collections": collections}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/agents/get")
async def read_agents():
    try:
        result = await AgentService.get_agents()
        collections = [row.collection_name for row in result.scalars()]
        return {"collections": collections}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.post("/agents/create")
async def create_agent_endpoint(agent_data: AgentRequest):
    try:
        # Вызываем асинхронную функцию для создания агента
        await AgentService.create_agent(
            agent_name=agent_data.agent_name,
            agent_prompt=agent_data.agent_prompt,
            collection_name=agent_data.collection_name
        )
        return {"message": "Agent created successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/answer/")
async def get_answer_endpoint(agent_name: str, user_question: str):
    try:
        # Вызываем асинхронную функцию для получения ответа
        answer = await AgentService.get_answer(agent_name=agent_name, user_question=user_question)
        return {"answer": answer}
    except Exception as e:
        # В случае ошибки возвращаем HTTP 500
        raise HTTPException(status_code=500, detail=str(e))
    
@router.post("/collections/create")
async def create_collection_endpoint(
    collection_name: str,
    files: List[UploadFile] = File(...)  # Принимаем список файлов
):
    try:
        for file in files:
            if not file.filename.endswith('.pdf'):
                raise HTTPException(status_code=400, detail="Неподдерживаемый формат файла. Поддерживаются только PDF файлы.")

        await AgentService.create_collection(collection_name=collection_name, input_files=files)
        return {"message": f"Коллекция '{collection_name}' успешно создана"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
