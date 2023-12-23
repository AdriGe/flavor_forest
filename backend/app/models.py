from sqlalchemy import create_engine, Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from pydantic import BaseModel
from datetime import datetime

SQLALCHEMY_DATABASE_URL = "postgresql://username:password@db_postgres/flavor_forest"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    role = Column(String, default="user")


class RefreshToken(Base):
    __tablename__ = "refresh_tokens"
    id = Column(Integer, primary_key=True, index=True)
    jti = Column(String, index=True)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    revoked = Column(Boolean, default=False)
    expires_at = Column(DateTime)


class UserCreate(BaseModel):
    username: str
    email: str
    password: str


class RefreshTokenRequest(BaseModel):
    refresh_token: str


Base.metadata.create_all(bind=engine)
