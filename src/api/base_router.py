from fastapi import APIRouter

from src.api import agent

from src.api import collection

router = APIRouter()

router.include_router(agent.router)

router.include_router(collection.router)
