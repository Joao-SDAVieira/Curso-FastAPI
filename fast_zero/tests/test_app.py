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


def test_create_user_user_exist(client, user):
    response = client.post(
        "/users/",
        json={
            "username": user.username,
            "email": "email@emaill.com",
            "password": "senha_teste",
        },
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_create_user_email_exist(client, user):
    response = client.post(
        "/users/",
        json={
            "username": "Joao",
            "email": user.email,
            "password": "senha_teste",
        },
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST


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


def test_get_single_user(client, user):
    url = "/users/" + str(user.id)
    response = client.get(url)
    assert response.json() == {
        "username": user.username,
        "email": user.email,
        "id": user.id,
    }
    assert response.status_code == HTTPStatus.OK


def test_get_single_user_not_found(client, user):
    response = client.get("/users/2")
    assert response.status_code == HTTPStatus.NOT_FOUND


def test_update_user(client, user, token):
    response = client.put(
        f"/users/{user.id}",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "password": "123",
            "username": "testeusername",
            "email": "test@test.com",
            "id": user.id,
        },
    )
    assert response.json() == {
        "username": "testeusername",
        "email": "test@test.com",
        "id": user.id,
    }


def test_update_user_return_enough_permissions(client, user, token):
    response = client.put("/users/2",
                          headers={"Authorization": f"Bearer {token}"},
                          json={
            "password": "123",
            "username": "testeusername",
            "email": "test@test.com",
            "id": "2",
        },)
    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_delete_user(client, user, token):
    response = client.delete(
        f"/users/{user.id}", headers={"Authorization": f"Bearer {token}"}
    )
    assert response.json() == {"message": "User deleted"}

    # def response_test(id):
    #     response_error = client.delete(f"/users/{id}")
    #     return response_error

    # response_error = response_test("2")
    # assert response_error.status_code == HTTPStatus.NOT_FOUND

    # response_error = response_test("0")
    # assert response_error.status_code == HTTPStatus.NOT_FOUND

    # def get_user_deleted():
    #     response = client.delete("/users/1")
    #     return response

    # response_user_not_exist = get_user_deleted()
    # assert response_user_not_exist.status_code == HTTPStatus.NOT_FOUND


def test_delete_user_return_enough_permissions(client, user, token):
    response = client.delete(
        "/users/2",
        headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_get_token(client, user):
    response = client.post(
        "/token",
        data={"username": user.email, "password": user.clean_password},
    )
    token = response.json()

    assert response.status_code == HTTPStatus.OK
    assert token["token_type"] == "Bearer"
    assert "access_token" in token


def test_credentials_exception(client, user, token):
    user.email = "outro@email.com"
    response = client.delete(
        f"/users/{user.id}", headers={"Authorization": f"Bearer {token}"}
    )
    # HTTPException(
    #     status_code=HTTPStatus.UNAUTHORIZED,
    #     detail="Could not validate credentials",
    #     headers={"WWW-Authenticate": "Bearer"},
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    # assert response.json() == {"message": "User deleted"}
