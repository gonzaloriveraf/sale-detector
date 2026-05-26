from sqlalchemy.orm import Session
from sqlalchemy import func
from models import Producto, Precio, Alerta, Notificacion, Usuario

def save_producto(db: Session, data: dict):
    producto = db.query(Producto).filter(Producto.url == data["url"]).first()

    if producto:
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
        db.add(Precio(
            producto_id=producto.id,
            precio=data["precio"],
            timestamp=func.now()
        ))

    db.commit()
    return data


def get_productos(db: Session, skip: int = 0, limit: int = 50):
    return db.query(Producto).offset(skip).limit(limit).all()


def get_alertas_activas(db: Session):
    return (
        db.query(Alerta, Producto, Usuario)
        .join(Producto, Producto.id == Alerta.producto_id)
        .join(Usuario, Usuario.id == Alerta.usuario_id)
        .filter(Alerta.active == True)
        .all()
    )


def get_ultima_notificacion(db: Session, alerta_id: int):
    return (
        db.query(Notificacion)
        .filter(Notificacion.alerta_id == alerta_id)
        .order_by(Notificacion.created_at.desc())
        .first()
    )


def save_notificacion(db: Session, alerta_id: int, usuario_id: int, producto_id: int, precio: int):
    noti = Notificacion(
        alerta_id=alerta_id,
        usuario=usuario_id,
        producto=producto_id,
        precio_notificado=precio,
        created_at=func.now()
    )
    db.add(noti)
    db.commit()
    return noti

def get_producto_by_url(db: Session, url: str):
    return db.query(Producto).filter(Producto.url == url).first()


def get_or_create_usuario(db: Session, email: str):
    usuario = db.query(Usuario).filter(Usuario.email == email).first()
    if not usuario:
        usuario = Usuario(email=email)
        db.add(usuario)
        db.flush()
    return usuario


def save_alerta(db: Session, usuario_id: int, producto_id: int, initial_price: int):
    alerta = Alerta(
        usuario_id=usuario_id,
        producto_id=producto_id,
        initial_price=initial_price,
        active=True,
        timestamp=func.now()
    )
    db.add(alerta)
    db.commit()
    return alerta