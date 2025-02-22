from urllib.request import urlopen
from urllib.error import URLError
import logging

# Configuração básica de logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

class SEFAZContigenciaChecker:
    """
    Classe responsável por verificar e notificar sobre contingências na SEFAZ.

    Attributes:
        url (str): URL da página da SEFAZ a ser verificada.
        parser (HTMLTableParser): Parser para extrair dados da tabela HTML.
        contigencias_manager (ContigenciasManager): Gerenciador de contingências.
        contigencia_ativa (bool): Estado atual da contingência (True se ativa).
        uf_full (str): Nome completo da unidade federativa.
        info_contigencia (str): Informações da contingência atual.
        informacoes_contigencia (str): Informações persistidas da contingência.
    """

    def __init__(self, url, parser, contigencias_manager):
        """
        Inicializa o verificador de contingências da SEFAZ.

        Args:
            url (str): URL da página da SEFAZ.
            parser (HTMLTableParser): Instância do parser HTML.
            contigencias_manager (ContigenciasManager): Instância do gerenciador de contingências.
        """
        self.url = url
        self.parser = parser
        self.contigencias_manager = contigencias_manager

        self.contigencia_ativa = False
        self.uf_full = ""
        self.info_contigencia = ""
        self.informacoes_contigencia = ""

    def check(self):
        """
        Verifica o estado de contingências na SEFAZ a partir da URL fornecida.

        Faz uma requisição HTTP, analisa o conteúdo HTML com o parser e atualiza
        as contingências no gerenciador se houver mudanças.
        """
        try:
            with urlopen(self.url, timeout=30) as response:
                html_content = response.read().decode("utf-8")
                self.parser.feed(html_content)
        except URLError as e:
            logger.error(f"Erro ao acessar a URL {self.url}: {e}")
            return
        except Exception as e:
            logger.error(f"Erro inesperado ao processar a requisição: {e}")
            return

        if not self.parser.table_data:
            logger.warning("Nenhum dado de tabela encontrado na resposta.")
            return

        # Remove o cabeçalho da tabela, se presente
        del self.parser.table_data[0]

        contigencias = self.contigencias_manager.load_contigencias()
        if contigencias is None:
            logger.error("Falha ao carregar contingências existentes.")
            return

        for row in self.parser.table_data:
            try:
                self._process_row(row, contigencias)
            except IndexError as e:
                logger.warning(f"Dados de linha inválidos: {e}. Linha: {row}")
                continue

        try:
            self.contigencias_manager.save_contigencias(contigencias)
            logger.info("Contingências atualizadas com sucesso.")
        except Exception as e:
            logger.error(f"Erro ao salvar contingências: {e}")

    def _process_row(self, row, contigencias):
        """
        Processa uma linha da tabela e atualiza as informações de contingência.

        Args:
            row (list): Linha da tabela com dados da SEFAZ.
            contigencias (dict): Dicionário de contingências carregado.
        """
        self.uf_full = row[1]
        uf_abbr = self.uf_full.split()[0]
        self.info_contigencia = row[4]
        self.contigencia_ativa = "Ativada" in self.info_contigencia

        if uf_abbr in contigencias:
            contigencia_atual = contigencias[uf_abbr]["contigencia_ativa"]
            if self.contigencia_ativa != contigencia_atual:
                contigencias[uf_abbr]["contigencia_ativa"] = self.contigencia_ativa
                contigencias[uf_abbr]["informacoes_contigencia"] = self.info_contigencia
                self.informacoes_contigencia = contigencias[uf_abbr]["informacoes_contigencia"]
                logger.info(f"Contingência atualizada para {uf_abbr}: {'Ativada' if self.contigencia_ativa else 'Desativada'}")
        else:
            contigencias[uf_abbr] = {
                "contigencia_ativa": self.contigencia_ativa,
                "informacoes_contigencia": self.info_contigencia
            }
            logger.info(f"Nova contingência registrada para {uf_abbr}: {'Ativada' if self.contigencia_ativa else 'Desativada'}")

    def notify(self, notification_manager):
        """
        Envia uma notificação sobre o estado da contingência usando o gerenciador fornecido.

        Args:
            notification_manager (NotificationManager): Instância do gerenciador de notificações.
        """
        if not self.uf_full or not self.info_contigencia:
            logger.warning("Nenhuma informação de contingência disponível para notificação.")
            return

        if self.contigencia_ativa:
            titulo = f"CONTINGÊNCIA ATIVADA PARA {self.uf_full}"
            descricao = self.info_contigencia
        else:
            titulo = f"CONTINGÊNCIA DESATIVADA PARA {self.uf_full}"
            descricao = self.informacoes_contigencia or self.info_contigencia

        try:
            notification_manager.send(titulo, descricao)
            logger.info(f"Notificação enviada: {titulo}")
        except Exception as e:
            logger.error(f"Erro ao enviar notificação: {e}")