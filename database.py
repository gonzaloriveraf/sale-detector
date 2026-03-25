import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

load_dotenv()

# 1. Recuperamos la URL
DATABASE_URL = os.getenv("DATABASE_URL")

# 2. Configuramos el Engine con parámetros de red para la nube
engine = create_engine(
    DATABASE_URL,
    # SSL es obligatorio para conectar desde GCP a Supabase de forma segura
    connect_args={"sslmode": "require"}, 
    # Verifica si la conexión está viva antes de usarla (evita errores tras inactividad)
    pool_pre_ping=True,
    # Recicla las conexiones cada 5 minutos para evitar bloqueos del pooler
    pool_recycle=300
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()