from notifiers.manager import NotificationManager


notifier = NotificationManager()  # Por padrão, Discord

def enviar_mensagem(titulo, descricao, grupo=""):
    notifier.send(titulo, descricao, grupo)