from fastapi import APIRouter

from src.api import agent

router = APIRouter()

router.include_router(agent.router)
