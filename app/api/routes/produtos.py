from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
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
    db.commit()
    db.refresh(produto)
    return produto


@router.get("", response_model=list[ProdutoResponse])
def listar_produtos(
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    return db.scalars(select(Produto).order_by(Produto.id)).all()


@router.get("/{produto_id}", response_model=ProdutoResponse)
def buscar_produto(
    produto_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    produto = db.get(Produto, produto_id)
    if not produto:
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
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado.")

    for campo, valor in data.model_dump(exclude_unset=True).items():
        setattr(produto, campo, valor)

    db.commit()
    db.refresh(produto)
    return produto


@router.delete("/{produto_id}", status_code=status.HTTP_204_NO_CONTENT)
def remover_produto(
    produto_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    produto = db.get(Produto, produto_id)
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado.")

    produto.ativo = False
    db.commit()
