from notifiers.notifier_discord import DiscordNotifier
from notifiers.notifier_telegram import TelegramNotifier
from notifiers.notifier_slack import SlackNotifier

class NotificationManager:
    def __init__(self, platform):
        self.notifiers = {
            "discord": DiscordNotifier,
            "telegram": TelegramNotifier,
            "slack": SlackNotifier
        }
        if platform not in self.notifiers:
            raise ValueError(f"Plataforma desconhecida: {platform}. Escolha entre {list(self.notifiers.keys())}")
        self.notifier = self.notifiers[platform]()

    def send(self, titulo, descricao, grupo=""):
        self.notifier.enviar_mensagem(titulo, descricao, grupo)