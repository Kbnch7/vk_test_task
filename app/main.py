import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_healthchecks.api.router import HealthcheckRouter, Probe
from fastapi_healthchecks.checks.postgres import PostgreSqlCheck

from .api.v1 import users_router
from .config import POSTGRES_USER, POSTGRES_PASSWORD, DATABASE_HOST, DATABASE_NAME, DATABASE_PORT, setup_logger

setup_logger()
logger = logging.getLogger("my_app")

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(users_router, prefix='/users')
app.include_router(
    HealthcheckRouter(
        Probe(
            name="readiness",
            checks=[
                PostgreSqlCheck(host=DATABASE_HOST, username=POSTGRES_USER, password=POSTGRES_PASSWORD, port=DATABASE_PORT, database=DATABASE_NAME),
            ],
        ),
        Probe(
            name="liveness",
            checks=[]
        ),
    ),
    prefix="/health",
)