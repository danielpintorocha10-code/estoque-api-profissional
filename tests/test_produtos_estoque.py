def criar_usuario_e_token(client):
    registro = client.post(
        "/auth/register",
        json={"email": "dev@example.com", "password": "SenhaSegura123"},
    )
    assert registro.status_code == 201
    login = client.post(
        "/auth/login",
        data={"username": "dev@example.com", "password": "SenhaSegura123"},
    )
    assert login.status_code == 200
    return {"Authorization": f"Bearer {login.json()['access_token']}"}


def criar_produto(client, headers, nome="Teclado", estoque_minimo=2):
    return client.post(
        "/produtos",
        headers=headers,
        json={"nome": nome, "descricao": "Produto de teste", "preco": "99.90", "estoque_minimo": estoque_minimo},
    )


def test_rotas_de_produto_exigem_autenticacao(client):
    resposta = client.get("/produtos")
    assert resposta.status_code == 401


def test_criar_listar_atualizar_e_excluir_produto(client):
    headers = criar_usuario_e_token(client)
    criado = criar_produto(client, headers)
    assert criado.status_code == 201
    produto_id = criado.json()["id"]

    lista = client.get("/produtos", headers=headers)
    assert lista.status_code == 200
    assert len(lista.json()) == 1

    atualizado = client.put(
        f"/produtos/{produto_id}", headers=headers, json={"nome": "Teclado mecânico"}
    )
    assert atualizado.status_code == 200
    assert atualizado.json()["nome"] == "Teclado mecânico"

    nulo = client.put(f"/produtos/{produto_id}", headers=headers, json={"preco": None})
    assert nulo.status_code == 422

    removido = client.delete(f"/produtos/{produto_id}", headers=headers)
    assert removido.status_code == 204
    assert client.get(f"/produtos/{produto_id}", headers=headers).status_code == 404
    assert client.get("/produtos", headers=headers).json() == []


def test_movimentacoes_atualizam_saldo_e_bloqueiam_saida_sem_saldo(client):
    headers = criar_usuario_e_token(client)
    produto = criar_produto(client, headers)
    produto_id = produto.json()["id"]

    entrada = client.post(
        f"/estoque/{produto_id}/movimentacoes",
        headers=headers,
        json={"tipo": "entrada", "quantidade": 5, "observacao": "Compra"},
    )
    assert entrada.status_code == 201

    saida = client.post(
        f"/estoque/{produto_id}/movimentacoes",
        headers=headers,
        json={"tipo": "saida", "quantidade": 2},
    )
    assert saida.status_code == 201

    detalhe = client.get(f"/produtos/{produto_id}", headers=headers)
    assert detalhe.json()["estoque_atual"] == 3

    insuficiente = client.post(
        f"/estoque/{produto_id}/movimentacoes",
        headers=headers,
        json={"tipo": "saida", "quantidade": 10},
    )
    assert insuficiente.status_code == 422

    historico = client.get(f"/estoque/{produto_id}/movimentacoes", headers=headers)
    assert historico.status_code == 200
    assert len(historico.json()) == 2


def test_movimentacao_rejeita_tipo_invalido_e_quantidade_zero(client):
    headers = criar_usuario_e_token(client)
    produto_id = criar_produto(client, headers).json()["id"]

    tipo_invalido = client.post(
        f"/estoque/{produto_id}/movimentacoes",
        headers=headers,
        json={"tipo": "ajuste", "quantidade": 1},
    )
    assert tipo_invalido.status_code == 422

    quantidade_zero = client.post(
        f"/estoque/{produto_id}/movimentacoes",
        headers=headers,
        json={"tipo": "entrada", "quantidade": 0},
    )
    assert quantidade_zero.status_code == 422
