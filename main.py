from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy import text
from scraper import scrape_falabella
from database import get_db
from crud import save_producto, get_productos, get_producto_by_url, get_or_create_usuario, save_alerta
from cronjob import run_cronjob

app = FastAPI()

class ScrapeRequest(BaseModel):
    url: str
    
class AlertaRequest(BaseModel):
    email: str
    url: str



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
    # 1. Raspa y guarda producto
    data = scrape_falabella(request.url)
    if "error" in data:
        raise HTTPException(status_code=400, detail=data["error"])
    save_producto(db, data)
    
    # 2. Busca el producto recién guardado
    producto = get_producto_by_url(db, request.url)
    
    # 3. Busca o crea usuario
    usuario = get_or_create_usuario(db, request.email)
    
    # 4. Crea alerta
    alerta = save_alerta(db, usuario.id, producto.id, data["precio"])
    
    return {"alerta_id": alerta.id, "usuario": usuario.email, "producto": producto.title}
