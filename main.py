from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy import text
from scraper import scrape_falabella
from database import get_db
from crud import save_producto, get_productos

app = FastAPI()

class ScrapeRequest(BaseModel):
    url: str

@app.get("/")
def root():
    return {"status": "ok"}

@app.get("/health")
def health(db: Session = Depends(get_db)):
    result = db.execute(text("SELECT 1")).fetchone()
    return {"db": "conectada", "result": result[0]}

@app.post("/scrape")
def scrape(request: ScrapeRequest, db: Session = Depends(get_db)):
    data = scrape_falabella(request.url)
    if "error" in data:
        raise HTTPException(status_code=400, detail=data["error"])
    producto = save_producto(db, data)
    return data

@app.get("/productos")
def list_productos(db: Session = Depends(get_db)):
    return get_productos(db)