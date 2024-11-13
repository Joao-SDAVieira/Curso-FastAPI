from http import HTTPStatus

from fastapi import FastAPI, HTTPException

from fast_zero.schemas import Message, UserDB, UserList, UserPublic, UserSchema

app = FastAPI(docs_url="/docs", redoc_url="/redoc")

database = []  # meu fakedb temporario


@app.get("/", response_model=Message)  # response model é oq a api retorna
def read_root():
    return {"message": "Olar mundo!"}


@app.post("/users/", status_code=HTTPStatus.CREATED, response_model=UserPublic)
def create_user(user: UserSchema):  # dessa forma, o retorno é o model
    # UserSchema,sendo mais seguro
    # 'user' é o user do pydantic
    user_with_id = UserDB(
        id=len(database) + 1,
        **user.model_dump(),  # model_dump() transforma os atributos do obj em
        # dicionário, que é passado como kwargs para user_with_id
    )
    database.append(user_with_id)
    return user_with_id


@app.get("/users/", response_model=UserList)
def read_users():
    return {"users": database}


@app.put("/users/{user_id}", response_model=UserPublic)
# o id do usuário a ser deletado passando por variável
def update_user(user_id: int, user: UserSchema):  # os parametros da função
    # são os parametros da api
    if user_id < 1 or user_id > len(database):
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="User not found"
        )
        # raise/ergue uma excessão para caso insira um idx invalido

    user_with_id = UserDB(id=user_id, **user.model_dump())
    database[user_id - 1] = user_with_id  # substituindo o dicionário presente
    # no indice especifico da lista database
    return user_with_id  # é renderizado o user com id (sem a senha)


@app.delete("/users/{user_id}", response_model=Message)
def delete_user(user_id: int):
    if user_id < 1 or user_id > len(database):
        raise HTTPException(HTTPStatus.NOT_FOUND, detail="User not found")

    del database[user_id - 1]  # mesma coisa que .pop()
    return {"message": "User deleted"}  # return == response


@app.get("/users/{user_id}", response_model=UserPublic)
def get_single_user(user_id: int):
    if user_id < 1 or user_id > len(database):
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="User not found"
        )
    return database[user_id - 1]
