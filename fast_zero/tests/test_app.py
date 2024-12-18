from http import HTTPStatus

from fast_zero.schemas import UserPublic


def test_read_root_deve_retornar_ok_ola_mundo(client):
    """o arquivo de teste, serve para simular o cliente testando a aplicação e
    vendo se haverá sucesso,
    principalmente se todos os códigos irão rodar"""
    # client = TestClient(app)  # Arrange (organização)
    response = client.get("/")  # ACT(ação)
    assert response.status_code == HTTPStatus.OK  # assert OK é 200
    assert response.json() == {"message": "Olar mundo!"}


def test_create_user(client):
    # client = TestClient(app)
    response = client.post(  # testando UserSchema
        "/users/",
        json={
            "username": "testeusername",
            "email": "test@test.com",
            "password": "1234",
        },
    )
    # validando o status code (deve ser 201)
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        "username": "testeusername",
        "email": "test@test.com",
        "id": 1,
    }


# esse teste possui uma falha, pois precisa que o teste acima execute primeiro
def test_read_users(client):
    response = client.get("/users/")
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"users": []}


def test_read_users_with_user(client, user):
    user_schema = UserPublic.model_validate(user).model_dump()

    response = client.get("/users/")

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"users": [user_schema]}


def test_get_single_user(client):
    response = client.get("/users/1")
    assert response.json() == {
        "username": "testeusername",
        "email": "test@test.com",
        "id": 1,
    }
    assert response.status_code == HTTPStatus.OK

    def response_error_test(id):
        response_error = client.get(f"/users/{id}")
        return response_error

    response_error = response_error_test("2")
    assert response_error.status_code == HTTPStatus.NOT_FOUND

    response_error = response_error_test("0")
    assert response_error.status_code == HTTPStatus.NOT_FOUND


def test_update_user(client, user):
    response = client.put(
        "/users/1",
        json={
            "password": "123",
            "username": "testeusername",
            "email": "test@test.com",
            "id": 1,
        },
    )
    assert response.json() == {
        "username": "testeusername",
        "email": "test@test.com",
        "id": 1,
    }

    def response_error_test(id):
        response_error = client.put(
            f"/users/{id}",
            json={
                "password": "123",
                "username": "testeusername",
                "email": "test@test.com",
            },
        )
        return response_error

    response_error = response_error_test("2")
    assert response_error.status_code == HTTPStatus.NOT_FOUND

    response_error = response_error_test("0")
    assert response_error.status_code == HTTPStatus.NOT_FOUND


def test_delete_user(client, user):
    response = client.delete("/users/1")
    assert response.json() == {"message": "User deleted"}

    def response_error_test(id):
        response_error = client.delete(f"/users/{id}")
        return response_error

    response_error = response_error_test("2")
    assert response_error.status_code == HTTPStatus.NOT_FOUND

    response_error = response_error_test("0")
    assert response_error.status_code == HTTPStatus.NOT_FOUND
