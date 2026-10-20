from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_user
from app.database.database import get_db
from app.models.produto import Produto
from app.models.user import User
from app.schemas.produto import ProdutoResponse

router = APIRouter(prefix="/relatorios", tags=["Relatórios"])


@router.get("/estoque-baixo", response_model=dict)
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
        .order_by(Produto.estoque_atual, Produto.id)
    ).all()

    return {
        "total": len(produtos),
        "produtos": [ProdutoResponse.model_validate(produto) for produto in produtos],
    }
