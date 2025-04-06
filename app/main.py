from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.endpoints import search

app = FastAPI()

origins = [
    "http://localhost:3000",  # フロントエンドのオリジン (開発環境)
    "*",  # 開発中はすべてのオリジンを許可することも可能
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(search.router, prefix="/api")