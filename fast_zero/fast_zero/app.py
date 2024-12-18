from http import HTTPStatus

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from fast_zero.database import get_session
from fast_zero.models import User
from fast_zero.schemas import Message, UserList, UserPublic, UserSchema

app = FastAPI(docs_url="/docs", redoc_url="/redoc")

database = []  # meu fakedb temporario


@app.get("/", response_model=Message)  # response model é oq a api retorna
def read_root():
    return {"message": "Olar mundo!"}


@app.post("/users/", status_code=HTTPStatus.CREATED, response_model=UserPublic)
def create_user(user: UserSchema, session=Depends(get_session)):
    # dessa forma, o retorno é o responsemodel
    db_user = session.scalar(
        select(User).where(
            (User.username == user.username) | (User.email == user.email)
        )
    )
    if db_user:
        if db_user.username == user.username:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail="Username already exists",
            )
        if db_user.email == user.username:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail="Email already exists",
            )
    db_user = User(
        username=user.username, email=user.email, password=user.password
    )
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


@app.get("/users/", response_model=UserList)
def read_users(
    limit: int = 10, skip: int = 0, session: Session = Depends(get_session)
):
    users = session.scalars(select(User).limit(limit).offset(skip))
    return {"users": users}


@app.put("/users/{user_id}", response_model=UserPublic)
# o id do usuário a ser deletado passando por variável
def update_user(
    user_id: int, user: UserSchema, session: Session = Depends(get_session)
):
    # os parametros da função
    # são os parametros da api
    db_user = session.scalar(select(User).where(User.id == user_id))

    if not db_user:
        raise HTTPException(HTTPStatus.NOT_FOUND, detail="User not found")

    db_user.email = user.email
    db_user.username = user.username
    db_user.password = user.password

    session.commit()
    session.refresh(db_user)
    return db_user


@app.delete("/users/{user_id}", response_model=Message)
def delete_user(user_id: int, session: Session = Depends(get_session)):
    db_user = session.scalar(select(User).where(User.id == user_id))

    if not db_user:
        raise HTTPException(HTTPStatus.NOT_FOUND, detail="User not found")

    session.delete(db_user)
    session.commit
    return {"message": "User deleted"}  # return == response


@app.get("/users/{user_id}", response_model=UserPublic)
def get_single_user(user_id: int):
    if user_id < 1 or user_id > len(database):
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="User not found"
        )
    return database[user_id - 1]
