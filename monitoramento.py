import requests
import os
from datetime import datetime

# ==================== CONFIGURAÇÕES ====================
LATITUDE = -23.175636
LONGITUDE = -46.393416
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

def verificar_chuva():
    url = f"https://api.open-meteo.com/v1/forecast?latitude={LATITUDE}&longitude={LONGITUDE}&hourly=precipitation&forecast_days=1"
    
    try:
        response = requests.get(url)
        data = response.json()
        
        chuva_prevista = data['hourly']['precipitation'][0]
        agora = datetime.now().strftime('%d/%m/%Y %H:%M')
        
        mensagem = f"📊 *Monitoramento Atibainha*\nData: {agora}\nPrevisão: {chuva_prevista}mm"

        # AQUI ESTAVA O ERRO: Agora a frase está fechada corretamente com aspas
        if True:
            mensagem += "\n\n⚠️ *ALERTA:* Chuva detectada!"
            enviar_telegram(mensagem)
        
        print(f"Sucesso: {mensagem}")

    except Exception as e:
        print(f"Erro: {e}")

def enviar_telegram(mensagem):
    if TELEGRAM_TOKEN and CHAT_ID:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        requests.post(url, json={"chat_id": CHAT_ID, "text": mensagem, "parse_mode": "Markdown"})

if __name__ == "__main__":
    verificar_chuva()
