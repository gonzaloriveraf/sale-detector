from sqlalchemy.orm import Session
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy import func
from models import Producto, Precio, Consulta

def save_producto(db: Session, data: dict):
    producto = db.query(Producto).filter(Producto.url == data["url"]).first()

    if producto:
        # Solo guarda en precios si cambió
        if producto.precio_actual != data["precio"]:
            db.add(Precio(
                producto_id=producto.id,
                precio=data["precio"],
                timestamp=func.now()
            ))
            producto.precio_anterior = producto.precio_actual
            producto.precio_actual = data["precio"]
        
        producto.title = data["title"]
        producto.updated_at = func.now()
    else:
        producto = Producto(
            url=data["url"],
            title=data["title"],
            precio_actual=data["precio"],
        )
        db.add(producto)
        db.flush()

        # Primera vez siempre guarda
        db.add(Precio(
            producto_id=producto.id,
            precio=data["precio"],
            timestamp=func.now()
        ))

    db.commit()
    return data
    
    # 1. Busca si ya existe
    producto = db.query(Producto).filter(Producto.url == data["url"]).first()

    if producto:
        # Guarda precio anterior antes de actualizar
        precio_anterior = producto.precio_actual
        producto.precio_anterior = precio_anterior
        producto.precio_actual = data["precio"]
        producto.title = data["title"]
        producto.updated_at = func.now()
    else:
        producto = Producto(
            url=data["url"],
            title=data["title"],
            precio_actual=data["precio"],
        )
        db.add(producto)

    db.flush()  # para obtener producto.id si es nuevo

    # 2. Registra en histórico de precios
    db.add(Precio(
        producto_id=producto.id,
        precio=data["precio"],
        timestamp=func.now()
    ))

    db.commit()
    return producto


def get_productos(db: Session, skip: int = 0, limit: int = 50):
    return db.query(Producto).offset(skip).limit(limit).all()


def get_producto_by_url(db: Session, url: str):
    return db.query(Producto).filter(Producto.url == url).first()


def get_historial_precios(db: Session, producto_id: int):
    return (
        db.query(Precio)
        .filter(Precio.producto_id == producto_id)
        .order_by(Precio.timestamp.desc())
        .all()
    )


def save_consulta(db: Session, usuario_id: int, producto_id: int):
    consulta = Consulta(
        usuario_id=usuario_id,
        producto_id=producto_id,
        timestamp=func.now()
    )
    db.add(consulta)
    db.commit()
    return consulta