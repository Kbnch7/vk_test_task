import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_healthchecks.api.router import HealthcheckRouter, Probe
from fastapi_healthchecks.checks.postgres import PostgreSqlCheck

from app.api.api_router import router

from .config import (
    DATABASE_HOST,
    DATABASE_NAME,
    DATABASE_PORT,
    POSTGRES_PASSWORD,
    POSTGRES_USER,
    setup_logger,
)

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
app.include_router(router, prefix="/api")
app.include_router(
    HealthcheckRouter(
        Probe(
            name="readiness",
            checks=[
                PostgreSqlCheck(
                    host=DATABASE_HOST,
                    username=POSTGRES_USER,
                    password=POSTGRES_PASSWORD,
                    port=DATABASE_PORT,
                    database=DATABASE_NAME
                ),
            ],
        ),
        Probe(
            name="liveness",
            checks=[]
        ),
    ),
    prefix="/health",
)
