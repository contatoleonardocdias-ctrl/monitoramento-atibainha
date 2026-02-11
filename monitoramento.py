import requests
import os
from datetime import datetime

# ==================== CONFIGURAÇÕES ====================
LATITUDE = -23.175636
LONGITUDE = -46.393416

# O código busca os valores que você salvou nas "etiquetas" do GitHub
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

        # TESTE: Alterado para True para forçar o envio da notificação agora
        if True:
            mensagem += "\n\n🚀 *TESTE DE SISTEMA:* O robô está funcionando!"
            enviar_telegram(mensagem)
        
        print(f"Sucesso: {mensagem}")

    except Exception as e:
        print(f"Erro ao verificar: {e}")

def enviar_telegram(mensagem):
    if TELEGRAM_TOKEN and CHAT_ID:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        payload = {
            "chat_id": CHAT_ID,
            "text": mensagem,
            "parse_mode": "Markdown"
        }
        response = requests.post(url, json=payload)
        if response.status_code != 200:
            print(f"Erro no Telegram: {response.text}")
    else:
        print("Erro: TELEGRAM_TOKEN ou CHAT_ID não encontrados nos Secrets!")

if __name__ == "__main__":
    verificar_chuva()
