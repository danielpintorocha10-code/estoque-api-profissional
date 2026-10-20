from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_user
from app.database.database import get_db
from app.models.produto import Produto
from app.models.user import User
from app.schemas.produto import ProdutoCreate, ProdutoResponse, ProdutoUpdate

router = APIRouter(prefix="/produtos", tags=["Produtos"])


@router.post("", response_model=ProdutoResponse, status_code=status.HTTP_201_CREATED)
def criar_produto(
    data: ProdutoCreate,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    produto = Produto(**data.model_dump())
    db.add(produto)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Não foi possível cadastrar o produto.") from None
    db.refresh(produto)
    return produto


@router.get("", response_model=list[ProdutoResponse])
def listar_produtos(
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    return db.scalars(
        select(Produto).where(Produto.ativo.is_(True)).order_by(Produto.id)
    ).all()


@router.get("/{produto_id}", response_model=ProdutoResponse)
def buscar_produto(
    produto_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    produto = db.get(Produto, produto_id)
    if not produto or not produto.ativo:
        raise HTTPException(status_code=404, detail="Produto não encontrado.")
    return produto


@router.put("/{produto_id}", response_model=ProdutoResponse)
def atualizar_produto(
    produto_id: int,
    data: ProdutoUpdate,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    produto = db.get(Produto, produto_id)
    if not produto or not produto.ativo:
        raise HTTPException(status_code=404, detail="Produto não encontrado.")

    atualizacoes = data.model_dump(exclude_unset=True)
    if not atualizacoes:
        raise HTTPException(status_code=422, detail="Informe ao menos um campo para atualizar.")

    for campo, valor in atualizacoes.items():
        setattr(produto, campo, valor)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=422, detail="Os dados informados não são válidos.") from None
    db.refresh(produto)
    return produto


@router.delete("/{produto_id}", status_code=status.HTTP_204_NO_CONTENT)
def remover_produto(
    produto_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    produto = db.get(Produto, produto_id)
    if not produto or not produto.ativo:
        raise HTTPException(status_code=404, detail="Produto não encontrado.")

    produto.ativo = False
    db.commit()
