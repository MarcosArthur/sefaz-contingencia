from discord import SyncWebhook, Embed
from config import URL_WEBHOOK_DISCORD

from notifiers.base import BaseNotifier


class DiscordNotifier(BaseNotifier):
    def __init__(self):
        self.enabled = bool(URL_WEBHOOK_DISCORD)
        if self.enabled:
            self.webhook = SyncWebhook.from_url(URL_WEBHOOK_DISCORD)
        else:
            self.webhook = None

    def enviar_mensagem(self, titulo, descricao, grupo = ""):
        if not self.enabled:
            print("Envio para Discord ignorado: configuração ausente.")
            return
        embed = Embed(title=titulo, description=descricao)
        self.webhook.send(embed=embed, content=grupo)
