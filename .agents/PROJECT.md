# Contexto técnico atual

## Escopo conhecido

O projeto é a base de um sistema de mapeamento hídrico para cidades. Não há requisitos funcionais, telas, entidades de domínio ou integrações definidos neste repositório além da estrutura inicial; não deduza essas definições.

## Stack confirmada

- Python 3.12 ou superior, gerenciado por UV.
- Django 6.1.1.
- SQLite como banco de desenvolvimento configurado.
- Tailwind CSS por `django-tailwind`, no app `theme`.
- `django-browser-reload` habilitado somente quando `DEBUG` está ativo.
- Ruff, `ruff-format` e pre-commit para qualidade de código.

`pyproject.toml` e `uv.lock` são a fonte de verdade de dependências. O repositório também contém `requirements.txt`; não o altere ou use como fonte primária sem uma decisão explícita do time.

## Estrutura relevante

- `core/`: configurações, URLs raiz e pontos ASGI/WSGI do Django.
- `theme/`: app do Tailwind; o CSS-fonte está em `theme/static_src/src/styles.css`.
- `user/`: app Django já criado, com URLs, views, modelos, testes e templates próprios.
- `Procfile.tailwind`: processos de desenvolvimento para Django e o watcher do Tailwind.
- `DOCS.md`: decisões de padrões e arquitetura registradas pelo time. Preserve-o a menos que uma solicitação peça sua alteração.

O Tailwind examina arquivos `html`, `py` e `js` sob o projeto, conforme `@source` em `theme/static_src/src/styles.css`. Ao criar novos locais com classes Tailwind fora desse alcance, atualize a fonte somente quando isso fizer parte da solicitação.
