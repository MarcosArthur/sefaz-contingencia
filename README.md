# SEFAZ Contingência

Este projeto monitora e notifica sobre contingências na SEFAZ, enviando alertas para plataformas configuráveis como Discord, Telegram ou Slack.

## Tecnologias Utilizadas
- Python 3.10
- Poetry (gerenciador de dependências)
- Requests (para chamadas HTTP)
- Discord Webhooks (para notificações no Discord)
- Telegram Bot API (para notificações no Telegram)
- Slack Webhooks (para notificações no Slack)

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

3. Configure as variáveis no `config.py` (veja a seção "Configuração de Notificações" abaixo).

## Configuração de Notificações
O projeto suporta notificações em múltiplas plataformas. Edite o arquivo `config.py` para configurar as credenciais da plataforma desejada:
- **Discord**:
- `URL_WEBHOOK_DISCORD`: URL do webhook do Discord (ex.: `https://discord.com/api/webhooks/123/abc`).
- **Telegram**:
- `TELEGRAM_BOT_TOKEN`: Token do bot obtido via BotFather (ex.: `123456:ABC-DEF`).
- `TELEGRAM_CHAT_ID`: ID do chat onde as mensagens serão enviadas (ex.: `-123456789`).
- **Slack**:
- `SLACK_WEBHOOK_URL`: URL do webhook do Slack (ex.: `https://hooks.slack.com/services/T000/B000/XXX`).

Se uma plataforma não for configurada (ou seja, suas credenciais estiverem vazias), as mensagens para essa plataforma serão ignoradas, e uma mensagem de aviso será exibida no console.

## Uso
Execute o script principal, especificando a plataforma de notificação como argumento:

- Para Discord:
```bash
poetry run python main.py discord
```

- Para Telegram:
```bash
poetry run python main.py telegram
```

- Para Slack:
```bash
poetry run python main.py slack
```

Se nenhum argumento for fornecido, o padrão será "discord".

### Exemplo de Saída
- Configuração ausente:
```bash
$ poetry run python main.py discord
Discord não configurado: URL_WEBHOOK_DISCORD não informada.
Envio para Discord ignorado: configuração ausente.
```

- Configuração válida:
```bash
$ poetry run python main.py discord
Mensagem enviada ao Discord com sucesso
```

## Estrutura do Projeto
- `main.py`: Ponto de entrada do sistema.
- `config.py`: Configurações do projeto, incluindo URLs e credenciais das plataformas.
- `parsers/`: Módulos para análise de dados (ex.: `html_table_parser.py`).
- `managers/`: Gerenciamento de contingências (ex.: `contigencias_manager.py`).
- `services/`: Serviços principais, incluindo verificação da SEFAZ (ex.: `sefaz_checker.py`).
- `notifiers/`: Módulos para envio de notificações:
   - `notifier/base.py`: Classe base para notificadores.
   - `notifier/manager.py`: Gerenciador de notificações agnóstico.
   - `notifier/notifier.py`: Função de envio de mensagens (wrapper para o gerenciador).
   - `notifier_discord.py`: Notificador para Discord.
   - `notifier_slack.py`: Notificador para Slack.
   - `notifier_telegram.py`: Notificador para Telegram.

## Contribuição
Sinta-se à vontade para abrir issues e pull requests! Para adicionar uma nova plataforma de notificação:
1. Crie uma nova classe em `notifiers/` herdando de `BaseNotifier`.
2. Adicione as credenciais necessárias em `config.py`.
3. Registre a nova plataforma em `NotificationManager`.

## Licença
Este projeto está sob a licença MIT.