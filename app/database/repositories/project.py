"""
Модуль для создания репозитория проектов
"""
from app.database.models import Project
from app.database.repositories.base_repo import BaseResourceRepo

project_repo = BaseResourceRepo(Project)
