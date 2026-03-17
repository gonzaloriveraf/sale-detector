from fastapi import FastAPI
from bs4 import BeautifulSoup
import requests

app = FastAPI()

@app.get("/")
def root():
    return {"status": "ok"}

@app.get("/scrape")
def scrape(url: str):
    headers = {"User-Agent": "Mozilla/5.0"}
    
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        return {"error": f"Status {response.status_code}"}
    
    soup = BeautifulSoup(response.text, "lxml")
    
    title_tag = soup.find("h1")
    title = title_tag.text.strip() if title_tag else "No encontrado"
    
    return {
        "url": url,
        "title": title,
        "status_code": response.status_code
    }