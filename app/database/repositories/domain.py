"""
Модуль для создания репозитория доменов
"""
from app.database.models import Domain
from app.database.repositories.base_repo import BaseResourceRepo

domain_repo = BaseResourceRepo(Domain)
