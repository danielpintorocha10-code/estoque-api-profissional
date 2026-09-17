# Estoque API

API REST para gerenciamento de produtos e movimentações de estoque.

## Tecnologias

- Python
- FastAPI
- PostgreSQL
- SQLAlchemy
- Pydantic
- JWT
- Docker
- Pytest
- Swagger/OpenAPI

## Funcionalidades

- Cadastro e login de usuários
- Autenticação JWT
- CRUD de produtos
- Entrada e saída de estoque
- Histórico de movimentações
- Relatório de estoque baixo
- Validação de dados
- Soft delete de produtos
- Documentação automática

## Como executar localmente

### 1. Criar ambiente virtual

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

### 2. Instalar dependências

```powershell
pip install -r requirements.txt
```

### 3. Configurar ambiente

Copie `.env.example` para `.env` e ajuste os valores.

### 4. Subir PostgreSQL

Com Docker:

```powershell
docker compose up -d db
```

### 5. Criar tabelas

Nesta versão inicial, execute:

```powershell
python -c "from app.database.database import Base, engine; import app.models; Base.metadata.create_all(engine)"
```

### 6. Executar API

```powershell
uvicorn app.main:app --reload
```

Acesse:

- API: http://127.0.0.1:8000
- Swagger: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

## Docker completo

```powershell
docker compose up --build
```

## Testes

```powershell
pytest
```

## Próximas evoluções

- Alembic para migrations
- Paginação e filtros
- Controle de permissões por usuário
- Testes completos de autenticação e estoque
- CI/CD com GitHub Actions
- Logs estruturados
- Auditoria
