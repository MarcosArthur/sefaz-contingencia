import requests
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID

from notifiers.base import BaseNotifier


class TelegramNotifier(BaseNotifier):
    def __init__(self):
        self.enabled = bool(TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID)
        self.url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"

    def enviar_mensagem(self, titulo, descricao, grupo=""):
        if not self.enabled:
            print("Envio para Telegram ignorado: configuração ausente.")
            return
        message = f"{titulo}\n{descricao}"
        if grupo:
            message = f"{grupo}\n{message}"
        payload = {
            "chat_id": TELEGRAM_CHAT_ID,
            "text": message
        }
        requests.post(self.url, data=payload)