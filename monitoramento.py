import requests
import os
from datetime import datetime

# ==================== CONFIGURAÇÕES ====================
# Coordenadas da Barragem Atibainha
LATITUDE = -23.175636
LONGITUDE = -46.393416

# Pega as chaves que você configurou no GitHub Secrets
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

def verificar_chuva():
    # Consulta a API de previsão do tempo (Open-Meteo)
    url = f"https://api.open-meteo.com/v1/forecast?latitude={LATITUDE}&longitude={LONGITUDE}&hourly=precipitation&forecast_days=1"
    
    try:
        response = requests.get(url)
        data = response.json()
        
        # Pega a chuva prevista para a hora atual
        chuva_prevista = data['hourly']['precipitation'][0]
        agora = datetime.now().strftime('%d/%m/%Y %H:%M')
        
        # Monta a mensagem base
        mensagem = f"📊 *Monitoramento Atibainha*\nData: {agora}\nPrevisão: {chuva_prevista}mm"

        # Correção da Linha 31: Se houver previsão de chuva, adiciona o Alerta
        if chuva_prevista > 0:
            mensagem += "\n\n⚠️ *ALERTA:* Chuva detectada!"
            enviar_telegram(mensagem)
        
        print(f"Executado com sucesso: {mensagem}")

    except Exception as e:
        print(f"Erro ao processar dados: {e}")

def enviar_telegram(mensagem):
    # Só tenta enviar se o Token e o ID existirem nos Secrets
    if TELEGRAM_TOKEN and CHAT_ID:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        payload = {
            "chat_id": CHAT_ID, 
            "text": mensagem, 
            "parse_mode": "Markdown"
        }
        try:
            requests.post(url, json=payload)
        except Exception as e:
            print(f"Erro ao enviar para o Telegram: {e}")
    else:
        print("Aviso: TELEGRAM_TOKEN ou CHAT_ID não configurados nos Secrets.")

if __name__ == "__main__":
    verificar_chuva()
