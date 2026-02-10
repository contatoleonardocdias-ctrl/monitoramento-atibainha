import requests
from datetime import datetime
import os

# ================= CONFIGURAÇÕES =================
LATITUDE = -23.175636
LONGITUDE = -46.393416
LOCAL = "Barragem Atibainha - Nazaré Paulista - São Paulo"

LIMITE_ATENCAO = 2.0  # mm de chuva

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

def verificar_chuva():
    url = (
        "https://api.open-meteo.com/v1/forecast"
        f"?latitude={LATITUDE}&longitude={LONGITUDE}"
        "&current=rain"
        "&timezone=America/Sao_Paulo"
    )

    r = requests.get(url, timeout=10)
    data = r.json()

    chuva = data["current"]["rain"]
    horario = datetime.now().strftime("%d/%m/%Y %H:%M")

    if chuva >= LIMITE_ATENCAO:
        msg = (
            "🟡 *ALERTA*

