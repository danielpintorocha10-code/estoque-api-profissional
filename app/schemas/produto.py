from decimal import Decimal

from pydantic import BaseModel, Field, model_validator


class ProdutoCreate(BaseModel):
    nome: str = Field(min_length=3, max_length=120, strip_whitespace=True)
    descricao: str | None = Field(default=None, max_length=500)
    preco: Decimal = Field(gt=0, max_digits=10, decimal_places=2)
    estoque_minimo: int = Field(default=0, ge=0)


class ProdutoUpdate(BaseModel):
    nome: str | None = Field(default=None, min_length=3, max_length=120, strip_whitespace=True)
    descricao: str | None = Field(default=None, max_length=500)
    preco: Decimal | None = Field(default=None, gt=0, max_digits=10, decimal_places=2)
    estoque_minimo: int | None = Field(default=None, ge=0)
    ativo: bool | None = None

    @model_validator(mode="after")
    def validar_campos_nao_nulos(self):
        campos_obrigatorios = {"nome", "preco", "estoque_minimo", "ativo"}
        for campo in campos_obrigatorios.intersection(self.model_fields_set):
            if getattr(self, campo) is None:
                raise ValueError(f"O campo '{campo}' não pode ser nulo.")
        if "nome" in self.model_fields_set and self.nome is not None and not self.nome.strip():
            raise ValueError("O nome não pode ficar vazio.")
        return self


class ProdutoResponse(BaseModel):
    id: int
    nome: str
    descricao: str | None
    preco: Decimal
    estoque_atual: int
    estoque_minimo: int
    ativo: bool

    model_config = {"from_attributes": True}
