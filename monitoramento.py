import requests
import os
from datetime import datetime

# ==================== CONFIGURAÇÕES ====================
LATITUDE = -23.17564739275283
LONGITUDE = -46.39341450241913

# Busca os valores nos Secrets do GitHub
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

def verificar_chuva():
    # URL atualizada para pegar tempo real (current) e previsão (hourly)
    url = f"https://api.open-meteo.com/v1/forecast?latitude={LATITUDE}&longitude={LONGITUDE}&current=precipitation&hourly=precipitation&forecast_days=1"
    
    try:
        response = requests.get(url)
        data = response.json()
        
        # 1. Chuva acontecendo AGORA (Tempo Real)
        chuva_agora = data['current']['precipitation']
        
        # 2. Chuva prevista para a PRÓXIMA HORA
        chuva_prevista = data['hourly']['precipitation'][0]
        
       url = (
    "https://api.open-meteo.com/v1/forecast"
    f"?latitude={LATITUDE}&longitude={LONGITUDE}"
    "&current=rain"
    "&timezone=America/Sao_Paulo"
)
        
        # Se estiver chovendo agora OU houver previsão de chuva
        if chuva_agora > 0 or chuva_prevista > 0:
            mensagem = f"⚠️ *ALERTA DE CHUVA - ATIBAINHA*\n\n"
            
            if chuva_agora > 0:
                mensagem += f"🌧 *Tempo Real:* Está chovendo {chuva_agora}mm agora!\n"
            
            if chuva_prevista > 0:
                mensagem += f"📅 *Previsão:* Esperado {chuva_prevista}mm para a próxima hora.\n"
                
            mensagem += f"\n⏰ Verificação: {agora}"
            
            enviar_telegram(mensagem)
            print(f"Alerta enviado! Real: {chuva_agora}mm / Previsto: {chuva_prevista}mm")
        else:
            print(f"Céu limpo em Atibainha ({agora}). Sem chuva no momento ou na previsão.")

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
        requests.post(url, json=payload)
    else:
        print("Erro: Verifique seus Secrets (TELEGRAM_TOKEN e CHAT_ID).")

if __name__ == "__main__":
    verificar_chuva()
