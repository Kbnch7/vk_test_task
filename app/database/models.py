from sqlalchemy import Column, String, DateTime, ForeignKey, UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Env(Base):
    __tablename__ = 'env'
    
    id = Column(UUID(as_uuid=True), primary_key=True)
    name = Column(String(20), unique=True, nullable=False)


class Domain(Base):
    __tablename__ = 'domain'
    
    id = Column(UUID(as_uuid=True), primary_key=True)
    name = Column(String(20), unique=True, nullable=False)


class Project(Base):
    __tablename__ = 'project'
    
    id = Column(UUID(as_uuid=True), primary_key=True)
    name = Column(String(20), unique=True, nullable=False)


class User(Base):
    __tablename__ = 'user'
    
    id = Column(UUID(as_uuid=True), primary_key=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    login = Column(String, index=True, nullable=False, unique=True)
    password = Column(String, nullable=False)
    project_id = Column(UUID(as_uuid=True), ForeignKey('project.id'), nullable=True)
    env_id = Column(UUID(as_uuid=True), ForeignKey('env.id'))
    domain_id = Column(UUID(as_uuid=True), ForeignKey('domain.id'))
    locktime = Column(DateTime(timezone=True), server_default=func.now())
