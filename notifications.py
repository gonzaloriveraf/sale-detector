import os

RESEND_API_KEY = os.getenv("RESEND_API_KEY")

def send_noti(email: str):
    resend.api_key = RESEND_API_KEY
    resend.Emails.send({
        "from": "onboarding@resend.dev",
        "to": email,
        "subject": f"🔥 Bajó el precio: test",
        "html": f"""
            <h2>producto test</h2>
            <p>Precio anterior: $...</p>
            <p>Precio nuevo: $ ... </p>
            <p><a href="#">Ver producto</a></p>
        """
    })