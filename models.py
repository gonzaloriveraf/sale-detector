from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey
from database import Base

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

class Alerta(Base):
    __tablename__ = "alertas"

    id            = Column(Integer, primary_key=True)
    usuario_id    = Column(Integer, ForeignKey("usuarios.id"))
    producto_id   = Column(Integer, ForeignKey("productos.id"))
    initial_price = Column(Integer)
    timestamp     = Column(DateTime)
    active        = Column(Boolean, default=True)

class Notificacion(Base):
    __tablename__ = "notificaciones"

    id                = Column(Integer, primary_key=True)
    alerta_id         = Column(Integer, ForeignKey("alertas.id"))
    usuario           = Column(Integer, ForeignKey("usuarios.id"))
    producto          = Column(Integer, ForeignKey("productos.id"))
    precio_notificado = Column(Integer)
    created_at        = Column(DateTime)


