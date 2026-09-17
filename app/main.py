from fastapi import FastAPI
from app.api.routes import auth, produtos, estoque, relatorios

app = FastAPI(
    title="Estoque API",
    description="API REST profissional para gestão de produtos e movimentações de estoque.",
    version="1.0.0",
)

app.include_router(auth.router)
app.include_router(produtos.router)
app.include_router(estoque.router)
app.include_router(relatorios.router)


@app.get("/", tags=["Health"])
def root():
    return {"message": "Estoque API funcionando!"}
