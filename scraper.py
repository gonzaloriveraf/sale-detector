import requests
from bs4 import BeautifulSoup

def scrape_falabella(url: str):
    headers = {"User-Agent": "Mozilla/5.0"}
    
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        return {"error": f"Status {response.status_code}"}
    
    soup = BeautifulSoup(response.text, "lxml")
    
    title_tag = soup.find("h1")
    title = title_tag.text.strip() if title_tag else "No encontrado"
    
     precio comentado hasta encontrar el selector correcto
     price_container = soup.find("li", attrs={"data-internet-price": True})
     if price_container:
         raw_price = price_container["data-internet-price"]
         price = int(raw_price.replace(".", ""))
    
    return {
        "url": url,
        "title": title,
        "precio": precio
    }