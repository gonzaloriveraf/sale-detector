import os
import resend

RESEND_API_KEY = os.getenv("RESEND_API_KEY")

def send_noti(email: str, title: str, precio_actual: int, initial_pric:int,url:str,):
    resend.api_key = RESEND_API_KEY
    resend.Emails.send({
 "from": "onboarding@resend.dev",
        "to": email,
        "subject": f"🔥 Bajó el precio: {title}",
        "html": f"""
            <h2>{title}</h2>
            <p>Precio inicial: ${initial_price:,}</p>
            <p>Precio actual: ${precio_actual:,}</p>
            <p><a href="{url}">Ver producto</a></p>
        """
    })