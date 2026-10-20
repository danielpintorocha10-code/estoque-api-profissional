def test_health(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Estoque API funcionando!"}


def test_documentacao_disponivel(client):
    response = client.get("/openapi.json")
    assert response.status_code == 200
    assert "/produtos" in response.json()["paths"]
