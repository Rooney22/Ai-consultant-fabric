from fastapi import FastAPI

from src.api.base_router import router

from fastapi.middleware.cors import CORSMiddleware

origins = [
   '*'
]
tags_dict = [
    {
        'name': 'agent',
        'description': 'Работа с сервисом по созданию AI-агентов',
    },
]

app = FastAPI(
    title="AI-consultant-service",
    description="Лучший в мире сервис по созданию AI-агентов",
    version="3.2.2",
    openapi_tags=tags_dict,
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)
