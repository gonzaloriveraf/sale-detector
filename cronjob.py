import os
import requests

BASE_URL = 'https://sale-detector-674240007272.us-central1.run.app'

def run_cronjob():
    productos = requests.get(f"{BASE_URL}/productos").json()  
    result = []
    
    for producto in productos:
        data = requests.post(f"{BASE_URL}/scrape", json={"url": producto["url"]}.json())
        if 'error' not in data: 
            result.append({
                "title": producto["title"],
                "url": producto["url"],
                "precio_anterior": producto["precio_actual"],
                "precio_nuevo": data["precio"],
                "cambio": data["precio"] - producto["precio_actual"]
                })
    return result