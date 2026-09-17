from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database.database import Base


class Movimentacao(Base):
    __tablename__ = "movimentacoes"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    produto_id: Mapped[int] = mapped_column(ForeignKey("produtos.id"))
    tipo: Mapped[str] = mapped_column(String(10))
    quantidade: Mapped[int]
    observacao: Mapped[str | None] = mapped_column(String(500), nullable=True)
