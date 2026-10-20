def registrar_usuario(client, email="teste@example.com", password="SenhaSegura123"):
    return client.post("/auth/register", json={"email": email, "password": password})


def autenticar(client, email="teste@example.com", password="SenhaSegura123"):
    return client.post("/auth/login", data={"username": email, "password": password})


def test_registrar_usuario_e_impedir_email_duplicado(client):
    primeira = registrar_usuario(client)
    segunda = registrar_usuario(client)
    assert primeira.status_code == 201
    assert "password_hash" not in primeira.json()
    assert segunda.status_code == 409


def test_login_e_endpoint_me(client):
    assert registrar_usuario(client).status_code == 201
    login = autenticar(client)
    assert login.status_code == 200
    assert login.json()["token_type"] == "bearer"

    resposta = client.get(
        "/auth/me",
        headers={"Authorization": f"Bearer {login.json()['access_token']}"},
    )
    assert resposta.status_code == 200
    assert resposta.json()["email"] == "teste@example.com"


def test_login_com_senha_incorreta(client):
    registrar_usuario(client)
    resposta = autenticar(client, password="senha-errada")
    assert resposta.status_code == 401
