from http import HTTPStatus

from fast_zero.schemas import UserPublic


def test_create_user(client):
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


def test_update_user_return_enough_permissions(client, other_user, token):
    response = client.put(
        f"/users/{other_user.id}",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "password": "123",
            "username": "testeusername",
            "email": "test@test.com",
            "id": "2",
        },
    )
    assert response.json() == {"detail": "Not enough permissions"}
    assert response.status_code == HTTPStatus.FORBIDDEN


def test_delete_user(client, user, token):
    response = client.delete(
        f"/users/{user.id}", headers={"Authorization": f"Bearer {token}"}
    )
    assert response.json() == {"message": "User deleted"}


def test_delete_user_return_enough_permissions(client, other_user, token):
    response = client.delete(
        f"/users/{other_user.id}", headers={"Authorization": f"Bearer {token}"}
    )
    assert response.json() == {"detail": "Not enough permissions"}
    assert response.status_code == HTTPStatus.FORBIDDEN


def test_credentials_exception_with_delete_user(client, user, token):
    user.email = "outro@email.com"
    response = client.delete(
        f"/users/{user.id}", headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {"detail": "Could not validate credentials"}
