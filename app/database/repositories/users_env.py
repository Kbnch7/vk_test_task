"""
Модуль для создания репозитория env
"""
from app.database.models import Env
from app.database.repositories.base_repo import BaseResourceRepo

env_repo = BaseResourceRepo(Env)
