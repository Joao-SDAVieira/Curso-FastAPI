from http import HTTPStatus

from fastapi.testclient import TestClient

from fast_zero.app import app


def test_read_root_deve_retornar_ok_ola_mundo():
    """o arquivo de teste, serve para simular o cliente testando a aplicação e
    vendo se haverá sucesso,
    principalmente se todos os códigos irão rodar"""
    client = TestClient(app)  # Arrange (organização)

    response = client.get('/')  # ACT(ação)
    assert response.status_code == HTTPStatus.OK  # assert OK é 200
    assert response.json() == {'message': 'Olar mundo!'}
