# Estoque API

API REST para gerenciamento de produtos e movimentações de estoque, construída com Python, FastAPI e PostgreSQL.

## Funcionalidades

- Cadastro de usuários e autenticação JWT.
- CRUD de produtos com exclusão lógica (soft delete).
- Entradas e saídas de estoque com histórico de movimentações.
- Validação de dados e prevenção de saída acima do saldo disponível.
- Relatório de produtos com estoque baixo.
- Documentação OpenAPI com Swagger UI e ReDoc.

## Tecnologias

Python 3.12+, FastAPI, SQLAlchemy 2, PostgreSQL 16, Pydantic, JWT, Docker e Pytest.

## Configuração local (Windows PowerShell)

### 1. Criar e ativar ambiente virtual

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

### 2. Instalar dependências

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 3. Configurar variáveis de ambiente

```powershell
Copy-Item .env.example .env
```

Edite `.env` e configure `SECRET_KEY` com uma chave aleatória de pelo menos 32 caracteres. Não publique o arquivo `.env` no GitHub. Para gerar uma chave no Python:

```powershell
python -c "import secrets; print(secrets.token_urlsafe(48))"
```

### 4. Iniciar PostgreSQL

Com Docker, configure `POSTGRES_PASSWORD` no `.env` e execute:

```powershell
docker compose up -d db
```

A `DATABASE_URL` do `.env` deve apontar para `localhost:5432` quando a API roda fora do Docker.

### 5. Criar tabelas (configuração inicial)

```powershell
python -c "from app.database.database import Base, engine; import app.models; Base.metadata.create_all(engine)"
```

> Este comando é adequado para a configuração inicial deste projeto. Para evolução de schema em ambientes compartilhados/produção, implemente migrações com Alembic.

### 6. Executar API

```powershell
uvicorn app.main:app --reload
```

- API: http://127.0.0.1:8000
- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

## Executar com Docker Compose

Configure `SECRET_KEY` e `POSTGRES_PASSWORD` no `.env` antes de iniciar:

```powershell
docker compose up --build
```

A API fica disponível na porta 8000. O Compose aguarda o PostgreSQL passar no healthcheck antes de iniciar a aplicação.

## Testes automatizados

Os testes usam um banco SQLite isolado e não precisam de um PostgreSQL ativo:

```powershell
pytest -q
```

Eles cobrem health check, documentação OpenAPI, cadastro/login, autenticação, operações de produtos, exclusão lógica e movimentações de estoque.

## Principais endpoints

| Método | Endpoint | Descrição |
|---|---|---|
| `POST` | `/auth/register` | Cadastrar usuário |
| `POST` | `/auth/login` | Obter token JWT (formulário OAuth2: `username` = e-mail) |
| `GET` | `/auth/me` | Consultar usuário autenticado |
| `POST` | `/produtos` | Cadastrar produto |
| `GET` | `/produtos` | Listar produtos ativos |
| `GET` | `/produtos/{produto_id}` | Consultar produto ativo |
| `PUT` | `/produtos/{produto_id}` | Atualizar produto |
| `DELETE` | `/produtos/{produto_id}` | Desativar produto (soft delete) |
| `POST` | `/estoque/{produto_id}/movimentacoes` | Registrar entrada ou saída |
| `GET` | `/estoque/{produto_id}/movimentacoes` | Consultar histórico |
| `GET` | `/relatorios/estoque-baixo` | Listar produtos no limite mínimo |

As rotas de produtos, estoque e relatórios exigem `Authorization: Bearer <token>`.

## Limites e próximas evoluções

- Implementar migrações Alembic.
- Adicionar paginação e filtros.
- Criar permissões granulares por perfil.
- Adicionar CI com GitHub Actions e logs estruturados.
- Validar concorrência e transações também em testes de integração com PostgreSQL.
