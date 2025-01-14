from fastapi import FastAPI

from fast_zero.routers import auth, users
from fast_zero.schemas import Message

app = FastAPI(docs_url="/docs", redoc_url="/redoc")
app.include_router(users.router)
app.include_router(auth.router)

database = []  # meu fakedb temporario


@app.get("/", response_model=Message)  # response model é oq a api retorna
def read_root():
    return {"message": "Olar mundo!"}
