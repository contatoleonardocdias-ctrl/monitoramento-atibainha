import requests
import os
from datetime import datetime, timedelta

# ==================== CONFIGURAÇÕES ====================
LATITUDE = -23.175636
LONGITUDE = -46.393416

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

def verificar_chuva():
    # Adicionei 'timezone=America/Sao_Paulo' na URL para a API já resolver o fuso
    url = f"https://api.open-meteo.com/v1/forecast?latitude={LATITUDE}&longitude={LONGITUDE}&current=precipitation&hourly=precipitation&timezone=America%2FSao_Paulo&forecast_days=1"
    
    try:
        response = requests.get(url)
        response.raise_for_status() # Garante que o script pare se a API cair
        data = response.json()
        
        chuva_agora = data['current']['precipitation']
        
        # Pega a hora atual para encontrar o índice correto na lista 'hourly'
        hora_atual_iso = datetime.now().strftime('%Y-%m-%dT%H:00')
        indices = data['hourly']['time']
        
        try:
            idx = indices.index(hora_atual_iso)
            chuva_proxima_hora = data['hourly']['precipitation'][idx + 1] if idx + 1 < len(indices) else 0
        except ValueError:
            chuva_proxima_hora = 0

        # Horário para o log/mensagem
        data_formatada = datetime.now().strftime('%d/%m/%Y %H:%M')
        
        if chuva_agora > 0 or chuva_proxima_hora > 0:
            mensagem = f"⚠️ *ALERTA DE CHUVA - ATIBAINHA*\n\n"
            
            if chuva_agora > 0:
                mensagem += f"🌧 *Tempo Real:* Está chovendo {chuva_agora}mm agora!\n"
            
            if chuva_proxima_hora > 0:
                mensagem += f"📅 *Previsão:* Esperado {chuva_proxima_hora}mm para a próxima hora.\n"
                
            enviar_telegram(mensagem)           
            print(f"Alerta enviado! {data_formatada}")
                
            mensagem += f"\n⏰ Atualizado em: {data_formatada}"
            
            enviar_telegram(mensagem)
            print(f"Alerta enviado! {data_formatada}")
        else:
            print(f"Céu limpo em Atibainha às {data_formatada}.")

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
        print("Erro: Verifique seus Secrets.")

if __name__ == "__main__":
    verificar_chuva()
