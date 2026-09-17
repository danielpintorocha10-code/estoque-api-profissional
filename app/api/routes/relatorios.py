from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_user
from app.database.database import get_db
from app.models.produto import Produto
from app.models.user import User

router = APIRouter(prefix="/relatorios", tags=["Relatórios"])


@router.get("/estoque-baixo")
def estoque_baixo(
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    produtos = db.scalars(
        select(Produto)
        .where(
            Produto.ativo.is_(True),
            Produto.estoque_atual <= Produto.estoque_minimo,
        )
        .order_by(Produto.estoque_atual)
    ).all()

    return {
        "total": len(produtos),
        "produtos": produtos,
    }
