# Relatório de revisão — Estoque API

## Alterações realizadas

- `app/core/config.py`: remove a chave JWT padrão insegura e exige `SECRET_KEY` com pelo menos 32 caracteres e rejeita o marcador de exemplo; valida tempo de expiração.
- `app/database/database.py`: configura conexão SQLite corretamente para uso em testes, mantendo PostgreSQL como padrão do projeto.
- `app/api/dependencies.py`: valida o formato do `sub` do JWT antes de consultar o usuário e mantém a rejeição de usuários inativos.
- `app/api/routes/auth.py`: normaliza e-mail, trata corrida de cadastro duplicado e impede login de usuário inativo.
- `app/schemas/produto.py`: valida valores monetários e impede `null` em campos que não aceitam nulo durante atualização.
- `app/schemas/movimentacao.py`: limita `tipo` a `entrada` ou `saida` usando `Literal`.
- `app/api/routes/produtos.py`: oculta produtos inativos na listagem/busca/atualização e melhora rollback de erros de integridade.
- `app/api/routes/estoque.py`: usa `SELECT ... FOR UPDATE` no PostgreSQL para proteger a atualização do saldo em movimentações concorrentes e executa rollback em falha.
- `app/api/routes/relatorios.py`: aplica resposta validada ao relatório de estoque baixo.
- `tests/`: substitui o teste placeholder por testes de health, documentação, cadastro/login, autenticação, CRUD, soft delete e movimentações.
- `.env.example`: documenta variáveis necessárias sem usar uma chave JWT operacional.
- `docker-compose.yml`: remove segredos fixos, exige senha/chave no `.env` e aguarda o healthcheck do PostgreSQL antes de iniciar a API.
- `Dockerfile`: usa Python 3.12 slim, copia somente a aplicação e define variáveis para execução mais previsível.
- `requirements.txt`: fixa versões para instalações reproduzíveis.

## Como validar localmente (Windows PowerShell)

1. Faça uma cópia de segurança do projeto atual.
2. Copie `.env.example` para `.env` e defina `SECRET_KEY` com uma chave aleatória de pelo menos 32 caracteres.
3. Crie/ative o ambiente virtual e instale as dependências: `pip install -r requirements.txt`.
4. Execute os testes: `pytest -q`.
5. Para usar Docker, confira as variáveis no `.env` e execute `docker compose up --build`.

## Observações importantes

- O pacote não inclui `.env` nem credenciais reais.
- `SELECT ... FOR UPDATE` tem efeito no PostgreSQL; SQLite não implementa o mesmo bloqueio.
- A API continua usando `Base.metadata.create_all` como procedimento manual descrito no README. Alembic/migrações continuam recomendados como próxima evolução.
- O token continua sendo JWT bearer; o projeto ainda não implementa papéis/permissões granulares.
- Os testes usam SQLite isolado para execução automatizada. Antes de publicar, valide também o fluxo completo com PostgreSQL local/Docker.
- Versões fixadas são um conjunto conservador; ao instalar, confira compatibilidade com a versão de Python disponível. O Docker usa Python 3.12 para uma base estável.
