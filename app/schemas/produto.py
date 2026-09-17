from decimal import Decimal

from pydantic import BaseModel, Field


class ProdutoCreate(BaseModel):
    nome: str = Field(min_length=3, max_length=120)
    descricao: str | None = Field(default=None, max_length=500)
    preco: Decimal = Field(gt=0)
    estoque_minimo: int = Field(default=0, ge=0)


class ProdutoUpdate(BaseModel):
    nome: str | None = Field(default=None, min_length=3, max_length=120)
    descricao: str | None = Field(default=None, max_length=500)
    preco: Decimal | None = Field(default=None, gt=0)
    estoque_minimo: int | None = Field(default=None, ge=0)
    ativo: bool | None = None


class ProdutoResponse(BaseModel):
    id: int
    nome: str
    descricao: str | None
    preco: Decimal
    estoque_atual: int
    estoque_minimo: int
    ativo: bool

    model_config = {"from_attributes": True}
