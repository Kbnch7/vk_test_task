import uuid

from sqlalchemy import UUID, Column, DateTime, ForeignKey, String, text
from sqlalchemy.orm import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()

class BaseTable(Base):
    __abstract__ = True

class Env(Base):
    __tablename__ = 'env'

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        index=True,
        default=uuid.uuid4,
        server_default=text("gen_random_uuid()")
    )
    name = Column(String(20), unique=True, nullable=False)


class Domain(Base):
    __tablename__ = 'domain'

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        index=True,
        server_default=text("gen_random_uuid()")
    )
    name = Column(String(20), unique=True, nullable=False)


class Project(Base):
    __tablename__ = 'project'

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        index=True,
        server_default=text("gen_random_uuid()")
    )
    name = Column(String(20), unique=True, nullable=False)


class User(Base):
    __tablename__ = 'users'

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        index=True,
        default=uuid.uuid4,
        server_default=text("gen_random_uuid()")
    )
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    login = Column(String, index=True, nullable=False, unique=True)
    password = Column(String, nullable=False)
    project_id = Column(UUID(as_uuid=True), ForeignKey('project.id'))
    env_id = Column(UUID(as_uuid=True), ForeignKey('env.id'))
    domain_id = Column(UUID(as_uuid=True), ForeignKey('domain.id'))
    locktime = Column(DateTime(timezone=True), server_default=func.now())
