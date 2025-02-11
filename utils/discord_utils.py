from discord import SyncWebhook, Embed

from config import URL_WEBHOOK_DISCORD

def enviar_mensagem(titulo, descricao, grupo = ""):
    webhook = SyncWebhook.from_url(URL_WEBHOOK_DISCORD)
    embed = Embed(title=titulo, description=descricao)
    webhook.send(embed=embed, content=grupo)
