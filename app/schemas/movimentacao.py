from pydantic import BaseModel, Field


class MovimentacaoCreate(BaseModel):
    tipo: str = Field(pattern="^(entrada|saida)$")
    quantidade: int = Field(gt=0)
    observacao: str | None = Field(default=None, max_length=500)


class MovimentacaoResponse(BaseModel):
    id: int
    produto_id: int
    tipo: str
    quantidade: int
    observacao: str | None

    model_config = {"from_attributes": True}
