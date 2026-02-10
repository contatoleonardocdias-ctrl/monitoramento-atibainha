import requests
import os
from datetime import datetime

# ================= CONFIGURAÇÕES =================
LOCAL = "Barragem Atibainha - Nazaré Paulista - SP"
LAT = -23.175636433765057
LON = -46.3934164213567

LIMITE_ATENCAO = 2.0  # mm

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = "2038317249"


def enviar_telegram(msg):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    requests.post(url, data={
        "chat_id": CHAT_ID,
        "text": msg
    })


def verificar_chuva():
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": LAT,
        "longitude": LON,
        "current": "rain",
        "timezone": "America/Sao_Paulo"
    }

    r = requests.get(url, timeout=10)
    data = r.json()

    chuva = data["current"]["rain"]
    horario = datetime.now().strftime("%d/%m/%Y %H:%M")

    if chuva >= LIMITE_ATENCAO:
        msg = (
            "🟡 ATENÇÃO – CHUVA\n"
            f"📍 {LOCAL}\n"
            f"🌧️ Chuva: {chuva} mm\n"
            f"🕒 {horario}"
        )
        enviar_telegram(msg)
        print("Alerta enviado")
    else:
        print(f"[{horario}] Normal ({chuva} mm)")


verificar_chuva()
