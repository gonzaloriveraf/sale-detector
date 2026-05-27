from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy import text
from scraper import scrape_falabella
from database import get_db
from crud import save_producto, get_productos, get_producto_by_url, get_or_create_usuario, save_alerta
from cronjob import run_cronjob
from models import Alerta


app = FastAPI()

class ScrapeRequest(BaseModel):
    url: str

class AlertaRequest(BaseModel):
    email: str
    urls: list[str] 


@app.get("/")
def root():
    return {"status": "ok"}

@app.get("/health")
def health(db: Session = Depends(get_db)):
    result = db.execute(text("SELECT 1")).fetchone()
    return {"db": "conectada", "result": result[0]}

@app.get("/productos")
def list_productos(db: Session = Depends(get_db)):
    return get_productos(db)

@app.get("/run-cronjob")
def trigger_cronjob():
    result = run_cronjob()
    return result

@app.post("/scrape")
def scrape(request: ScrapeRequest, db: Session = Depends(get_db)):
    data = scrape_falabella(request.url)
    if "error" in data:
        raise HTTPException(status_code=400, detail=data["error"])
    producto = save_producto(db, data)
    return data

@app.post("/alerta")
def crear_alerta(request: AlertaRequest, db: Session = Depends(get_db)):
    usuario = get_or_create_usuario(db, request.email)
    alertas_creadas = []

    for url in request.urls: 
        data = scrape_falabella(url)
        if "error" in data:
            continue
        save_producto(db, data)
        producto = get_producto_by_url(db, url)
        alerta = save_alerta(db, usuario.id, producto.id, data["precio"])
        alertas_creadas.append(
            { "alerta_id" : alerta.id, 
            "producto": producto.title
            })

    return {"alertas": alertas_creadas, "usuario": request.email}


@app.put("/alerta/{alerta_id}/desactivar")
def desactivar_alerta(alerta_id: int, db: Session = Depends(get_db)):
    alerta = db.query(Alerta).filter(Alerta.id == alerta_id).first()
    if not alerta:
        raise HTTPException(status_code=404, detail="Alerta no encontrada")
    alerta.active = False
    db.commit()
    return {"alerta_id": alerta_id, "active": False}