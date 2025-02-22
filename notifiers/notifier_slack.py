import requests
from config import SLACK_WEBHOOK_URL

from notifiers.base import BaseNotifier


class SlackNotifier(BaseNotifier):
    def __init__(self):
        self.enabled = bool(SLACK_WEBHOOK_URL)
        self.webhook_url = SLACK_WEBHOOK_URL

    def enviar_mensagem(self, titulo, descricao, grupo=""):
        if not self.enabled:
            print("Envio para Slack ignorado: configuração ausente.")
            return
        message = f"*{titulo}*\n{descricao}"
        if grupo:
            message = f"{grupo}\n{message}"
        payload = {
            "text": message
        }
        requests.post(self.webhook_url, json=payload)