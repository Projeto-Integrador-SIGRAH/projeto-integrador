# Fluxo de trabalho

## Ambiente e dependências

- Use `uv run ...` para executar comandos do projeto. Ele usa o ambiente `.venv` local e o lockfile.
- Em um clone novo, use `uv sync --locked`; isso garante as versões presentes em `uv.lock`.
- Para adicionar ou remover dependências, use `uv add` ou `uv remove`. Versione sempre `pyproject.toml` e `uv.lock` juntos.
- Não use `pip install` nem altere manualmente o diretório `.venv`.
- Não atualize todas as dependências, versões do Python ou ferramentas de lint sem pedido explícito. Essas mudanças têm impacto amplo.

## Execução local

```sh
uv run python manage.py migrate
uv run python manage.py runserver
uv run python manage.py tailwind start
```

O servidor Django e o watcher do Tailwind podem rodar juntos com:

```sh
uv run honcho -f Procfile.tailwind start
```

## Git e revisão

- Comece com `git status --short` e não descarte mudanças que não foram produzidas pela tarefa atual.
- Faça commits pequenos e focados somente se a solicitação incluir criar um commit.
- O hook de pre-commit protege `main`, `master`, `develop` e `release/*` contra commits diretos; não ignore ou desative esses hooks para contornar uma falha.
- Revise o diff antes de concluir. Não inclua arquivos gerados, caches, banco SQLite local, ambiente virtual ou credenciais.
- Ao encontrar uma configuração insegura, uma inconsistência ou uma melhoria fora do escopo, não a altere por iniciativa própria: informe o local, o impacto e a sugestão ao solicitante.
