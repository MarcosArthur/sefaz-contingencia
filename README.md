# SEFAZ Contingência

Este projeto monitora e notifica sobre contingências na SEFAZ, enviando alertas via Discord.

## Tecnologias Utilizadas
- Python 3.10
- Poetry (gerenciador de dependências)
- Requests (para chamadas HTTP)
- Discord Webhooks (para notificações)

## Instalação
1. Clone o repositório:
   ```bash
   git clone git@github.com:MarcosArthur/sefaz-contingencia.git
   cd sefaz_contigencia
   ```
2. Instale as dependências com Poetry:
   ```bash
   poetry install
   ```
3. Configure as variáveis no `config.py`.

## Uso
Execute o script principal:
```bash
poetry run python main.py
```

## Estrutura do Projeto
- `main.py`: Ponto de entrada do sistema.
- `config.py`: Configurações do projeto.
- `parsers/`: Módulos para análise de dados.
- `managers/`: Gerenciamento de contingências.
- `services/`: Serviços principais, incluindo verificação da SEFAZ.
- `utils/`: Funções auxiliares (ex.: envio de notificações no Discord).

## Contribuição
Sinta-se à vontade para abrir issues e pull requests!

## Licença
Este projeto está sob a licença MIT.

