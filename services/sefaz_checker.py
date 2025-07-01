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
        mudancas_contigencias (list): Lista de mudanças de contingências para notificação.
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
        self.mudancas_contigencias = []

    def check(self):
        """
        Verifica o estado de contingências na SEFAZ a partir da URL fornecida.

        Faz uma requisição HTTP, analisa o conteúdo HTML com o parser e atualiza
        as contingências no gerenciador se houver mudanças.
        """
        # Limpa a lista de mudanças para esta verificação
        self.mudancas_contigencias = []
        
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
        uf_full = row[1]
        uf_abbr = uf_full.split()[0]
        info_contigencia = row[4]
        contigencia_ativa = "Ativada" in info_contigencia

        if uf_abbr in contigencias:
            contigencia_atual = contigencias[uf_abbr]["contigencia_ativa"]
            if contigencia_ativa != contigencia_atual:
                # Houve mudança de estado
                contigencias[uf_abbr]["contigencia_ativa"] = contigencia_ativa
                contigencias[uf_abbr]["informacoes_contigencia"] = info_contigencia
                contigencias[uf_abbr]["notificacao_enviada"] = False
                
                # Adiciona à lista de mudanças para notificação
                self.mudancas_contigencias.append({
                    "uf_full": uf_full,
                    "uf_abbr": uf_abbr,
                    "contigencia_ativa": contigencia_ativa,
                    "info_contigencia": info_contigencia,
                    "informacoes_contigencia": contigencias[uf_abbr]["informacoes_contigencia"]
                })
                
                logger.info(f"Contingência atualizada para {uf_abbr}: {'Ativada' if contigencia_ativa else 'Desativada'}")
        else:
            # Nova contingência
            contigencias[uf_abbr] = {
                "contigencia_ativa": contigencia_ativa,
                "informacoes_contigencia": info_contigencia,
                "notificacao_enviada": False
            }
            
            # Adiciona à lista de mudanças para notificação
            self.mudancas_contigencias.append({
                "uf_full": uf_full,
                "uf_abbr": uf_abbr,
                "contigencia_ativa": contigencia_ativa,
                "info_contigencia": info_contigencia,
                "informacoes_contigencia": info_contigencia
            })
            
            logger.info(f"Nova contingência registrada para {uf_abbr}: {'Ativada' if contigencia_ativa else 'Desativada'}")

    def notify(self, notification_manager):
        """
        Envia notificações sobre todas as mudanças de contingências usando o gerenciador fornecido.

        Args:
            notification_manager (NotificationManager): Instância do gerenciador de notificações.
        """
        if not self.mudancas_contigencias:
            logger.info("Nenhuma mudança de contingência para notificar.")
            return

        for mudanca in self.mudancas_contigencias:
            if mudanca["contigencia_ativa"]:
                titulo = f"CONTINGÊNCIA ATIVADA PARA {mudanca['uf_full']}"
                descricao = mudanca["info_contigencia"]
            else:
                titulo = f"CONTINGÊNCIA DESATIVADA PARA {mudanca['uf_full']}"
                descricao = mudanca["informacoes_contigencia"] or mudanca["info_contigencia"]

            try:
                notification_manager.send(titulo, descricao)
                logger.info(f"Notificação enviada: {titulo}")
                
                # Marca como notificação enviada
                contigencias = self.contigencias_manager.load_contigencias()
                if contigencias and mudanca["uf_abbr"] in contigencias:
                    contigencias[mudanca["uf_abbr"]]["notificacao_enviada"] = True
                    self.contigencias_manager.save_contigencias(contigencias)
                    
            except Exception as e:
                logger.error(f"Erro ao enviar notificação para {mudanca['uf_abbr']}: {e}")

    def check_pending_notifications(self, notification_manager):
        """
        Verifica e envia notificações para contingências ativas que ainda não foram notificadas.
        Útil para casos onde o sistema foi reiniciado e há contingências ativas pendentes.

        Args:
            notification_manager (NotificationManager): Instância do gerenciador de notificações.
        """
        contigencias = self.contigencias_manager.load_contigencias()
        if not contigencias:
            return

        for uf_abbr, contigencia in contigencias.items():
            if (contigencia.get("contigencia_ativa", False) and 
                not contigencia.get("notificacao_enviada", False)):
                
                # Busca o nome completo da UF no arquivo de contingências
                uf_full = self._get_uf_full_name(uf_abbr)
                
                titulo = f"CONTINGÊNCIA ATIVA PARA {uf_full}"
                descricao = contigencia.get("informacoes_contigencia", "Contingência ativa")
                
                try:
                    notification_manager.send(titulo, descricao)
                    logger.info(f"Notificação pendente enviada: {titulo}")
                    
                    # Marca como notificação enviada
                    contigencias[uf_abbr]["notificacao_enviada"] = True
                    self.contigencias_manager.save_contigencias(contigencias)
                    
                except Exception as e:
                    logger.error(f"Erro ao enviar notificação pendente para {uf_abbr}: {e}")

    def _get_uf_full_name(self, uf_abbr):
        """
        Retorna o nome completo da UF baseado na abreviação.
        
        Args:
            uf_abbr (str): Abreviação da UF
            
        Returns:
            str: Nome completo da UF
        """
        uf_names = {
            "AC": "ACRE",
            "AL": "ALAGOAS", 
            "AP": "AMAPÁ",
            "AM": "AMAZONAS",
            "BA": "BAHIA",
            "CE": "CEARÁ",
            "DF": "DISTRITO FEDERAL",
            "ES": "ESPÍRITO SANTO",
            "GO": "GOIÁS",
            "MA": "MARANHÃO",
            "MT": "MATO GROSSO",
            "MS": "MATO GROSSO DO SUL",
            "MG": "MINAS GERAIS",
            "PA": "PARÁ",
            "PB": "PARAÍBA",
            "PR": "PARANÁ",
            "PE": "PERNAMBUCO",
            "PI": "PIAUÍ",
            "RJ": "RIO DE JANEIRO",
            "RN": "RIO GRANDE DO NORTE",
            "RS": "RIO GRANDE DO SUL",
            "RO": "RONDÔNIA",
            "RR": "RORAIMA",
            "SC": "SANTA CATARINA",
            "SP": "SÃO PAULO",
            "SE": "SERGIPE",
            "TO": "TOCANTINS"
        }
        return uf_names.get(uf_abbr, uf_abbr)