from fastapi import APIRouter, Depends, UploadFile, status, HTTPException, File, Form
from src.services.agent import AgentService
from src.models.schemas.agent.agent_request import AgentRequest
from typing import List


router = APIRouter(
    prefix='/collection',
    tags=['collection'],
)

@router.get("/get")
async def read_collections():
    result = await AgentService.get_collections()
    collections = [{"collection_id": row.collection_id, "collection_name": row.collection_name, 'collection_description': row.collection_description} for row in result]
    return collections
    
@router.post("/create")
async def create_collection_endpoint(
    collection_name: str = Form(...),  # Указываем, что это часть тела запроса
    collection_description: str = Form(...),  # Указываем, что это часть тела запроса
    files: List[UploadFile] = File(...)  # Файлы также часть тела запроса
):
        for file in files:
            if not file.filename.endswith('.pdf'):
                raise HTTPException(status_code=400, detail="Неподдерживаемый формат файла. Поддерживаются только PDF файлы.")

        await AgentService.create_collection(collection_name=collection_name, input_files=files, collection_description=collection_description)
        return {"message": f"Коллекция '{collection_name}' успешно создана"}
