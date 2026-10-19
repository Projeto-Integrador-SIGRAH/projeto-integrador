# Regras de código

## Django e Python

- Siga o estilo e a organização existentes no arquivo que está sendo modificado.
- Mantenha responsabilidades separadas: configurações em `core`, funcionalidades em apps Django e templates junto aos apps quando esse for o padrão local.
- Ao mudar modelos, crie migrações com `uv run python manage.py makemigrations` e revise o arquivo gerado. Nunca edite migrações já aplicadas para alterar seu efeito.
- Acrescente ou ajuste testes para o comportamento novo quando houver comportamento testável.
- Não coloque segredos, tokens ou credenciais em código, configurações versionadas ou logs.
- Não altere configurações de produção, autenticação, permissões ou banco de dados sem uma solicitação explícita e uma decisão documentada.

## Templates e Tailwind

- Reutilize a estrutura de templates e carregue as tags necessárias do Django/Tailwind quando criar um template que precise do CSS.
- Prefira classes Tailwind e o CSS-fonte do tema em vez de estilos inline repetidos.
- Mantenha HTML semântico e acessível: rótulos para campos, texto alternativo útil e controles utilizáveis por teclado.
- Não crie um design, componente ou fluxo de interface por conta própria quando os requisitos ou o Figma não forem fornecidos na tarefa.

## Verificação mínima

Depois de uma alteração de código, execute o conjunto proporcional à mudança:

```sh
uv run python manage.py check
uv run python manage.py test
```

Se arquivos acompanhados pelo hook forem alterados, execute também:

```sh
uvx pre-commit run --all-files
```

Relate com clareza qualquer comando não executado e o motivo.
