from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_user
from app.database.database import get_db
from app.models.movimentacao import Movimentacao
from app.models.produto import Produto
from app.models.user import User
from app.schemas.movimentacao import MovimentacaoCreate, MovimentacaoResponse

router = APIRouter(prefix="/estoque", tags=["Estoque"])


@router.post("/{produto_id}/movimentacoes", response_model=MovimentacaoResponse, status_code=status.HTTP_201_CREATED)
def movimentar_estoque(
    produto_id: int,
    data: MovimentacaoCreate,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    # No PostgreSQL, bloqueia a linha durante a transação para reduzir disputas
    # entre saídas simultâneas do mesmo produto. SQLite ignora FOR UPDATE.
    produto = db.scalar(
        select(Produto).where(Produto.id == produto_id).with_for_update()
    )
    if not produto or not produto.ativo:
        raise HTTPException(status_code=404, detail="Produto não encontrado.")

    if data.tipo == "saida" and data.quantidade > produto.estoque_atual:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Estoque insuficiente para realizar a saída.",
        )

    if data.tipo == "entrada":
        produto.estoque_atual += data.quantidade
    else:
        produto.estoque_atual -= data.quantidade

    movimentacao = Movimentacao(
        produto_id=produto_id,
        tipo=data.tipo,
        quantidade=data.quantidade,
        observacao=data.observacao,
    )
    db.add(movimentacao)
    try:
        db.commit()
    except Exception:
        db.rollback()
        raise
    db.refresh(movimentacao)
    return movimentacao


@router.get("/{produto_id}/movimentacoes", response_model=list[MovimentacaoResponse])
def listar_movimentacoes(
    produto_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    produto = db.get(Produto, produto_id)
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado.")

    return db.scalars(
        select(Movimentacao)
        .where(Movimentacao.produto_id == produto_id)
        .order_by(Movimentacao.id.desc())
    ).all()
