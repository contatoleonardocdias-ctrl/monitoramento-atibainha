import requests
import os
from datetime import datetime

# ==================== CONFIGURAÇÕES ====================
LATITUDE = -23.175636
LONGITUDE = -46.393416
LOCAL = "Barragem Atibainha - Nazaré Paulista - São Paulo"
LIMITE_ATENCAO = 2.0  # mm de chuva

# Pega as chaves que você salvou no GitHub Secrets
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

def verificar_chuva():
    # Consulta a API de previsão do tempo
    url = f"https://api.open-meteo.com/v1/forecast?latitude={LATITUDE}&longitude={LONGITUDE}&hourly=precipitation&forecast_days=1"
    
    try:
        response = requests.get(url)
        data = response.json()
        
        # Pega a chuva prevista para a próxima hora
        chuva_prevista = data['hourly']['precipitation'][0]
        agora = datetime.now().strftime('%d/%m/%Y %H:%M')

        mensagem = f"📊 *Monitoramento Atibainha*\nData: {agora}\nPrevisão: {chuva_prevista}mm"

        if chuva_prevista >= LIMITE_ATENCAO:
            mensagem += f"\n\n⚠️ *ALERTA:* Chuva acima de {LIMITE_ATENCAO}mm esperada!"
        
        enviar_telegram(mensagem)
        print(f"Sucesso: {mensagem}")

    except Exception as e:
        print(f"Erro ao consultar API: {e}")

def enviar_telegram(mensagem):
    if not TELEGRAM_TOKEN or not CHAT_ID:
        print("Erro: TELEGRAM_TOKEN ou CHAT_ID não configurados nos Secrets.")
        return

    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": mensagem, "parse_mode": "Markdown"}
    
    try:
        requests.post(url, json=payload)
    except Exception as e:
        print(f"Erro ao enviar Telegram: {e}")

if __name__ == "__main__":
    verificar_chuva()
