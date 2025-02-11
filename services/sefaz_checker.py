from urllib.request import urlopen
from urllib.error import URLError
import utils.discord_utils as discord_utils

class SEFAZContigenciaChecker:
    def __init__(self, url, parser, contigencias_manager):
        self.url = url
        self.parser = parser
        self.contigencias_manager = contigencias_manager

    def check_and_notify(self):
        try:
            response = urlopen(self.url, timeout=30)
            html_content = response.read().decode('utf-8')
            self.parser.feed(html_content)
        except URLError as e:
            print(f"Erro ao acessar a URL: {e}")
            return

        if self.parser.table_data:
            del self.parser.table_data[0]

        contigencias = self.contigencias_manager.load_contigencias()

        for row in self.parser.table_data:
            uf_full = row[1]
            uf_abbr = uf_full.split()[0]
            info_contigencia = row[4]
            contigencia_ativa = "Ativada" in info_contigencia

            if uf_abbr in contigencias:
                contigencia_atual = contigencias[uf_abbr]["contigencia_ativa"]
                informacoes_contigencia = contigencias[uf_abbr]["informacoes_contigencia"]

                if contigencia_ativa != contigencia_atual:
                    contigencias[uf_abbr]["contigencia_ativa"] = contigencia_ativa
                    contigencias[uf_abbr]["informacoes_contigencia"] = info_contigencia

                    if contigencia_ativa:
                        discord_utils.enviar_mensagem(
                            titulo=f"CONTINGÊNCIA ATIVADA PARA {uf_full}",
                            descricao=info_contigencia
                        )
                    else:
                        discord_utils.enviar_mensagem(
                            titulo=f"CONTINGÊNCIA DESATIVADA PARA {uf_full}",
                            descricao=informacoes_contigencia
                        )


            else:
                contigencias[uf_abbr] = {
                    "contigencia_ativa": contigencia_ativa,
                    "informacoes_contigencia": info_contigencia
                }

        self.contigencias_manager.save_contigencias(contigencias)
