"""
Пакет для уровня репозиториев (Repository Layer) в Layer Architecture

Пакет содержит модули для:
- Создания базового репозитория (Паттерн фабрика)
- Создания репозитория для пользователей (наследование от базового репозитория)
- Создания репозитория для домен (наследование от базового репозитория)
- Создания репозитория для env (наследование от базового репозитория)
- Создания репозитория для проектов (наследование от базового репозитория)
- Создания репозитория для проектов (наследование от базового репозитория)
"""
from .base_repo import BaseResourceRepo as BaseResourceRepo
from .domain import domain_repo as domain_repo
from .project import project_repo as project_repo
from .users import users_repo as users_repo
from .users_env import env_repo as env_repo
