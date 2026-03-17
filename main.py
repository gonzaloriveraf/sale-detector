from fastapi import FastAPI
from pydantic import BaseModel
from scraper import scrape_falabella

app = FastAPI()

class ScrapeRequest(BaseModel):
    url: str

@app.get("/")
def root():
    return {"status": "ok"}

@app.post("/scrape")
def scrape(request: ScrapeRequest):
    return scrape_falabella(request.url)