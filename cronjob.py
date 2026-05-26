from database import get_session
from crud import get_alertas_activas, get_ultima_notificacion, save_notificacion
from scraper import scrape

def run_cronjob():
    db = get_session()()
    resultados = []

    try:
        alertas = get_alertas_activas(db)

        for alerta, producto, usuario in alertas:
            data = scrape(producto.url)

            if "error" in data:
                continue

            precio_actual = data["precio"]

            ultima_noti = get_ultima_notificacion(db, alerta.id)
            last_notified_price = ultima_noti.precio_notificado if ultima_noti else alerta.initial_price

            notificado = False
            if precio_actual < alerta.initial_price and precio_actual != last_notified_price:
                send_noti(usuario.email, producto.title, precio_actual, alerta.initial_price, producto.url)
                save_notificacion(db, alerta.id, usuario.id, producto.id, precio_actual)
                notificado = True

            resultados.append({
                "alerta_id": alerta.id,
                "producto": producto.title,
                "precio_actual": precio_actual,
                "initial_price": alerta.initial_price,
                "notificado": notificado
            })

    finally:
        db.close()

    return resultados


if __name__ == "__main__":
    run_cronjob()