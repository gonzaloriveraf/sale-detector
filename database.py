import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = os.getenv("DATABASE_URL")

Base = declarative_base()

engine = None
SessionLocal = None

def get_engine():
    global engine
    if engine is None:
        if not DATABASE_URL:
            raise RuntimeError("DATABASE_URL no está configurada")
        engine = create_engine(
            DATABASE_URL,
            connect_args={"sslmode": "require"},
            pool_pre_ping=True,
            pool_recycle=300
        )
    return engine

def get_session():
    global SessionLocal
    if SessionLocal is None:
        SessionLocal = sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=get_engine()
        )
    return SessionLocal

def get_db():
    db = get_session()()
    try:
        yield db
    finally:
        db.close()