# Projeto Integrador

Base inicial do sistema de mapeamento hídrico para cidades. Neste estágio, o repositório contém a configuração do projeto Django, do Tailwind CSS, do gerenciamento de dependências com UV e das validações de pre-commit.

As decisões de padrões e arquitetura já registradas permanecem em [DOCS.md](DOCS.md). Este arquivo explica como preparar e executar o projeto.

## Tecnologias

| Tecnologia | Uso no projeto |
| --- | --- |
| Python 3.12+ | Linguagem da aplicação. |
| Django 6.1.1 | Framework web e estrutura do backend. |
| SQLite | Banco de dados de desenvolvimento padrão. |
| Tailwind CSS | Estilização das páginas, integrado por `django-tailwind`. |
| django-browser-reload | Atualização automática do navegador durante o desenvolvimento. |
| UV | Gerenciamento do Python, do ambiente virtual e das dependências. |
| Ruff e ruff-format | Lint e formatação de código Python. |
| pre-commit | Execução automática de verificações antes dos commits. |
| Honcho | Execução conjunta dos processos Django e Tailwind quando desejado. |

As dependências do projeto são declaradas em `pyproject.toml` e têm versões reproduzíveis em `uv.lock`. Use esses dois arquivos com o UV; embora o repositório também contenha `requirements.txt`, ele não é o fluxo de instalação recomendado.

## Pré-requisitos

- Git instalado para clonar o repositório.
- Acesso à internet na primeira instalação, para que o UV obtenha o Python 3.12 e as dependências.
- Um terminal: Terminal no macOS/Linux ou PowerShell no Windows.

## Primeira execução

Siga todos os passos da seção correspondente ao seu sistema operacional. Os comandos abaixo pressupõem um clone novo do repositório.

### macOS

1. Instale o UV:

   ```sh
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

2. Feche e abra o Terminal para que o comando `uv` entre no `PATH`. Confirme a instalação:

   ```sh
   uv --version
   ```

3. Clone o repositório e entre na pasta do projeto. Substitua a URL pelo endereço real do repositório:

   ```sh
   git clone https://github.com/Projeto-Integrador-SIGRAH/projeto-integrador.git
   cd projeto-integrador
   ```

4. Instale o Python 3.12 pelo UV e crie o ambiente virtual local em `.venv`:

   ```sh
   uv python install 3.12
   uv venv --python 3.12
   ```

5. Instale exatamente as dependências travadas no repositório:

   ```sh
   uv sync --locked
   ```

6. Instale o hook de pre-commit no clone local:

   ```sh
   uvx pre-commit install
   ```

7. Aplique as migrações iniciais do Django:

   ```sh
   uv run python manage.py migrate
   ```

### Linux

1. Instale o UV:

   ```sh
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

2. Abra um novo terminal e verifique a instalação:

   ```sh
   uv --version
   ```

3. Clone o repositório e entre na pasta do projeto:

   ```sh
   git clone https://github.com/Projeto-Integrador-SIGRAH/projeto-integrador.git
   cd projeto-integrador
   ```

4. Instale o Python 3.12 e crie o ambiente virtual:

   ```sh
   uv python install 3.12
   uv venv --python 3.12
   ```

5. Sincronize as dependências definidas no lockfile:

   ```sh
   uv sync --locked
   ```

6. Instale o hook de pre-commit e aplique as migrações:

   ```sh
   uvx pre-commit install
   uv run python manage.py migrate
   ```

### Windows (PowerShell)

1. Instale o UV no PowerShell:

   ```powershell
   powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
   ```

2. Feche e abra o PowerShell para atualizar o `PATH`. Confirme a instalação:

   ```powershell
   uv --version
   ```

3. Clone o repositório e entre na pasta do projeto:

   ```powershell
   git clone https://github.com/Projeto-Integrador-SIGRAH/projeto-integrador.git
   Set-Location projeto-integrador
   ```

4. Instale o Python 3.12 e crie o ambiente virtual:

   ```powershell
   uv python install 3.12
   uv venv --python 3.12
   ```

5. Instale as dependências travadas e configure o pre-commit:

   ```powershell
   uv sync --locked
   uvx pre-commit install
   ```

6. Aplique as migrações iniciais:

   ```powershell
   uv run python manage.py migrate
   ```

> O UV executa os comandos com o ambiente `.venv` automaticamente através de `uv run`; portanto, não é necessário ativá-lo. Caso prefira ativá-lo para usar `python` diretamente, execute `source .venv/bin/activate` no macOS/Linux ou `.venv\Scripts\Activate.ps1` no PowerShell.

## Executando no desenvolvimento

Após a primeira configuração, abra dois terminais na raiz do projeto.

No primeiro, inicie o Django:

```sh
uv run python manage.py runserver
```

No segundo, inicie o observador do Tailwind:

```sh
uv run python manage.py tailwind start
```

Abra [http://127.0.0.1:8000/](http://127.0.0.1:8000/) no navegador. O processo do Tailwind deve continuar aberto durante o desenvolvimento para recompilar o CSS quando os arquivos monitorados mudarem.

Como alternativa aos dois terminais, use o `Procfile.tailwind` já existente para iniciar os dois processos em conjunto:

```sh
uv run honcho -f Procfile.tailwind start
```

No Windows, os mesmos comandos funcionam no PowerShell com `uv run`.

## Comandos úteis

| Objetivo | Comando |
| --- | --- |
| Verificar a configuração do Django | `uv run python manage.py check` |
| Criar migrações após alterar modelos | `uv run python manage.py makemigrations` |
| Aplicar migrações | `uv run python manage.py migrate` |
| Executar testes | `uv run python manage.py test` |
| Executar todas as verificações de pre-commit | `uvx pre-commit run --all-files` |
| Sincronizar dependências após atualizar o repositório | `uv sync --locked` |
| Atualizar dependências de propósito | `uv lock --upgrade` seguido de `uv sync` |

`uvx pre-commit run --all-files` pode corrigir automaticamente problemas de Ruff e formatação. Revise as alterações antes de incluí-las em um commit.

## Convenções já configuradas

Antes de cada commit, o pre-commit verifica espaços em branco, YAML, arquivos grandes, conflitos de merge, chaves privadas e tentativas de commit direto em `main`, `master`, `develop` ou branches `release/*`. Também executa Ruff com correções automáticas e `ruff-format`.

Para preservar um ambiente reproduzível, não instale dependências diretamente com `pip`. Ao adicionar ou remover um pacote, use `uv add <pacote>` ou `uv remove <pacote>` e inclua as mudanças de `pyproject.toml` e `uv.lock` no mesmo commit.
