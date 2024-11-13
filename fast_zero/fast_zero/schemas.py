from pydantic import BaseModel, EmailStr


class Message(BaseModel):  # A partir daí a função deve retornar esse padrão
    message: str


class UserSchema(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserDB(UserSchema):  # esse schema será temporário, herda o UserSchema
    id: int


class UserPublic(BaseModel):
    id: int
    username: str
    email: EmailStr


class UserList(BaseModel):
    users: list[UserPublic]
