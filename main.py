from fastapi import FastAPI
from pydantic import BaseModel
from scraper import scrape_falabella
from database import get_db
from fastapi import Depends
from sqlalchemy.orm import Session

app = FastAPI()

class ScrapeRequest(BaseModel):
    url: str

@app.get("/")
def root():
    return {"status": "ok"}

@app.get("/db-test")
def db_test(db: Session = Depends(get_db)):
    result = db.execute("SELECT 1").fetchone()
    return {"db": "conectada", "result": result[0]}


@app.post("/scrape")
def scrape(request: ScrapeRequest):
    return scrape_falabella(request.url)




