from decimal import Decimal

from sqlalchemy import Numeric, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database.database import Base


class Produto(Base):
    __tablename__ = "produtos"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    nome: Mapped[str] = mapped_column(String(120), index=True)
    descricao: Mapped[str | None] = mapped_column(String(500), nullable=True)
    preco: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    estoque_atual: Mapped[int] = mapped_column(default=0)
    estoque_minimo: Mapped[int] = mapped_column(default=0)
    ativo: Mapped[bool] = mapped_column(default=True)
