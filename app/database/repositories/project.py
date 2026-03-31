from app.database.models import Project
from app.database.repositories.base_repo import BaseResourceRepo
from app.schemas.project import ProjectCreate

project_repo = BaseResourceRepo(Project, ProjectCreate)
