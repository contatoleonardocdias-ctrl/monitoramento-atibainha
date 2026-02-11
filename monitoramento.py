import requests
import os
from datetime import datetime, timedelta

# ==================== CONFIGURAÇÕES ====================
LATITUDE = -23.175636
LONGITUDE = -46.393416

# Busca os valores nos Secrets do GitHub
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

def verificar_chuva():
    # URL para tempo real e previsão
    url = f"https://api.open-meteo.com/v1/forecast?latitude={LATITUDE}&longitude={LONGITUDE}&current=precipitation&hourly=precipitation&forecast_days=1"
    
    try:
        response = requests.get(url)
        data = response.json()
        
        chuva_agora = data['current']['precipitation']
        chuva_prevista = data['hourly']['precipitation'][0]
        
        # AJUSTE DE HORÁRIO: UTC para São Paulo (-3 horas)
        fuso_horario = timedelta(hours=-3)
        agora_sp = datetime.now() + fuso_horario
        data_formatada = agora_sp.strftime('%d/%m/%Y %H:%M')
        
        # IMPORTANTE: Mude para 'if True:' se quiser forçar um teste agora
        if true:
            mensagem = f"⚠️ *ALERTA DE CHUVA - ATIBAINHA*\n\n"
            
            if chuva_agora > 0:
                mensagem += f"🌧 *Tempo Real:* Está chovendo {chuva_agora}mm agora!\n"
            
            if chuva_prevista > 0:
                mensagem += f"📅 *Previsão:* Esperado {chuva_prevista}mm para a próxima hora.\n"
                
            mensagem += f"\n⏰ Horário de Brasília: {data_formatada}"
            
            enviar_telegram(mensagem)
            print(f"Alerta enviado! {data_formatada}")
        else:
            print(f"Céu limpo em Atibainha às {data_formatada}. Sem chuva registrada.")

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
