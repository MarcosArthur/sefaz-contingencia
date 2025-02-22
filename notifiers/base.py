from abc import ABC, abstractmethod


class BaseNotifier(ABC):
    @abstractmethod
    def enviar_mensagem(self, titulo, descricao, grupo=""):
        pass