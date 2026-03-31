from app.database.models import Env
from app.database.repositories.base_repo import BaseResourceRepo
from app.schemas.env import EnvCreate

env_repo = BaseResourceRepo(Env, EnvCreate)
