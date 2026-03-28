from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api.v1 import users_router


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(users_router, prefix='/users')
