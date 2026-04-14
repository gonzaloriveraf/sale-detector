from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from db import Base

class Usuario(Base):
    __tablename__ = "usuarios"

    id         = Column(Integer, primary_key=True)
    email      = Column(String)
    created_at = Column(DateTime)

class Producto(Base):
    __tablename__ = "productos"

    id              = Column(Integer, primary_key=True)
    url             = Column(Text)
    title           = Column(String)
    precio_actual   = Column(Integer)
    precio_anterior = Column(Integer)
    created_at      = Column(DateTime)
    updated_at      = Column(DateTime)

class Precio(Base):
    __tablename__ = "precios"

    id          = Column(Integer, primary_key=True)
    producto_id = Column(Integer, ForeignKey("productos.id"))
    precio      = Column(Integer)
    timestamp   = Column(DateTime)

class Consulta(Base):
    __tablename__ = "consultas"

    id          = Column(Integer, primary_key=True)
    usuario_id  = Column(Integer, ForeignKey("usuarios.id"))
    producto_id = Column(Integer, ForeignKey("productos.id"))
    timestamp   = Column(DateTime)