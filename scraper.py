import requests
from bs4 import BeautifulSoup
import json

def scrape_falabella(url: str):
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        return {"error": f"Status {response.status_code}"}

    soup = BeautifulSoup(response.text, "lxml")
    next_data = soup.find("script", id="__NEXT_DATA__")

    if not next_data:
        return {"error": "No se encontró __NEXT_DATA__"}

    data = json.loads(next_data.string)
    product = data["props"]["pageProps"]["productData"]

    title = product.get("name", "No encontrado")

    # Toma el precio de la primera variante disponible
    precio_raw = None
    for variant in product.get("variants", []):
        prices = variant.get("prices", [])
        if prices:
            precio_raw = prices[0]["price"][0]  # ej: "69.990"
            break

    # Convierte a entero limpio
    precio = int(precio_raw.replace(".", "")) if precio_raw else None

    return {
        "url": url,
        "title": title,
        "precio": precio
    }